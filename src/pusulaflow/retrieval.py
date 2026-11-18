"""BM25, kosinüs benzerliği, RRF ve komşu parça genişletmesi."""
import re
from time import perf_counter
from pusulaflow.database import load_index_chunks, search_chunks

import numpy as np
from ollama import embed
from rank_bm25 import BM25Okapi

from pusulaflow.config import (
    EMBEDDING_MODEL, QUERY_EMBEDDING_OPTIONS, RETRIEVAL_CANDIDATES,
    RETRIEVAL_TOP_K, RRF_CONSTANT,
)

def tokenize(text: str) -> list[str]:
    """Metni küçük harfe çevirip sözcüklerine ayırır."""
    return re.findall('\\w+', text.lower())


class HybridRetriever:

    def __init__(self, connection, index: dict):
        self.connection = connection
        self.index = index
        self.embedding_model = index["embedding_model"]

        self.chunks = load_index_chunks(
            connection,
            index_id=index["id"],
        )

        if not self.chunks:
            raise ValueError(
                "İndekste belge parçası bulunamadı. "
                "Önce python scripts/index_documents.py çalıştır."
            )

        self.tokenized_chunks = [
            tokenize(chunk["text"])
            for chunk in self.chunks
        ]

        self.bm25_index = BM25Okapi(self.tokenized_chunks)

        print("Veritabanından yüklenen parça:", len(self.chunks))

    def bm25_search(self, query: str, top_k: int=3) -> list[dict]:
        """Sorguyla sözcük eşleşmesi olan parçaları BM25 ile sıralar."""
        query_tokens = tokenize(query)
        query_words = set(query_tokens)
        scores = self.bm25_index.get_scores(query_tokens)
        matching_indices = [
            index
            for index, tokens in enumerate(self.tokenized_chunks)
            if query_words.intersection(tokens)
        ]
        ranked_indices = sorted(
            matching_indices,
            key=lambda index: float(scores[index]),
            reverse=True,
        )[:top_k]
        return [
            {**self.chunks[index], 'bm25_score': float(scores[index])}
            for index in ranked_indices
        ]

    def vector_search(self, query: str, top_k: int = 3) -> list[dict]:
        """Sorguya en yakın parçaları PostgreSQL'den getirir."""
        embedding_query = self.index["query_prefix"].format(
            query=query
        )

        query_started = perf_counter()

        response = embed(
            model=self.embedding_model,
            input=embedding_query,
            truncate=False,
            keep_alive=0,
            options=QUERY_EMBEDDING_OPTIONS,
        )

        print(
            f"Sorgu embedding: {perf_counter() - query_started:.2f} sn",
            flush=True,
        )

        query_vector = np.array(
            response["embeddings"][0],
            dtype=np.float32,
        )

        if len(query_vector) != self.index["embedding_dimension"]:
            raise ValueError("Sorgu vektörünün boyutu indeksle uyuşmuyor.")

        return search_chunks(
            self.connection,
            index_id=self.index["id"],
            query_vector=query_vector,
            top_k=top_k,
        )

    def search_documents(self, query: str) -> list[dict]:
        """BM25 ve vektör aramasıyla ilgili belge parçalarını getirir.

        Sonuçlara aynı belgedeki komşu parçaları ek bağlam olarak ekler.
        Tam belgeyi okumak için sonuçtaki document_id kullanılabilir.

        Args:
            query: Bilgi ihtiyacını ifade eden arama sorgusu.
        """
        bm25_results = self.bm25_search(query, top_k=RETRIEVAL_CANDIDATES)
        vector_results = self.vector_search(query, top_k=RETRIEVAL_CANDIDATES)
        combined = {}
        rrf_constant = RRF_CONSTANT
        for results in [bm25_results, vector_results]:
            for rank, item in enumerate(results, start=1):
                chunk_id = item['id']
                if chunk_id not in combined:
                    combined[chunk_id] = {**item, 'rrf_score': 0.0}
                combined[chunk_id]['rrf_score'] += 1.0 / (rrf_constant + rank)
        ranked_results = sorted(
            combined.values(),
            key=lambda item: item['rrf_score'],
            reverse=True,
        )
        selected_results = ranked_results[:RETRIEVAL_TOP_K]
        positions = {chunk['id']: index for index, chunk in enumerate(self.chunks)}
        included_ids = {
            item["id"]
            for item in selected_results
        }
        expanded_results = []
        for item in selected_results:
            position = positions[item['id']]
            neighbors = []
            for offset in [-1, 1]:
                neighbor_position = position + offset
                if 0 <= neighbor_position < len(self.chunks):
                    neighbor = self.chunks[neighbor_position]
                    if (
                        neighbor["document_id"] == item["document_id"]
                        and neighbor["id"] not in included_ids
                    ):
                        neighbors.append(neighbor)
                        included_ids.add(neighbor["id"])
            expanded_results.append({**item, 'neighbor_chunks': neighbors})
        return expanded_results
