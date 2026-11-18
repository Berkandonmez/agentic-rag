 #Sırasıyla:
# 1. data klasöründeki belgeleri okuyor.
#2. Belgeleri küçük parçalara ayırıyor.
#3. Hash’leri karşılaştırıp yeni, değişmiş ve silinmiş parçaları belirliyor.
#4. Yeni/değişmiş parçaların embedding’lerini üretiyor.
#5. Metinleri ve vektörleri PostgreSQL’e kaydedip eski parçaları temizliyor.
from pusulaflow.config import DATA_DIR, RAG_INDEX_NAME, EMBEDDING_MODEL 
from pusulaflow.database import (
    get_connection,
    get_index,
    get_chunk_hashes,
    save_chunks,
    delete_chunks,
    validate_index_model
)
from pusulaflow.documents import load_documents, chunk_documents
import numpy as np
from ollama import embed

import hashlib


def main():
    with get_connection() as connection:
        index = get_index(connection, RAG_INDEX_NAME)
        validate_index_model(index, EMBEDDING_MODEL)

        documents = load_documents(DATA_DIR)

        chunks = chunk_documents(
            documents,
            chunk_size=index["chunk_size"],
            overlap=index["chunk_overlap"],
        )
        document_positions = {}

        for chunk in chunks:
            document_id = chunk["document_id"]
            position = document_positions.get(document_id, 0)
            chunk["chunk_position"] = position
            document_positions[document_id] = position + 1

            embedding_text = index["document_prefix"].format(
                document_id=chunk["document_id"],
                text=chunk["text"],
            )

            chunk["embedding_text"] = embedding_text
            chunk["content_hash"] = hashlib.sha256(
                embedding_text.encode("utf-8")
            ).hexdigest()
        stored_hashes = get_chunk_hashes(connection, index["id"])
        if not chunks and stored_hashes:
            raise ValueError(
                "Kaynaklardan hiç parça yüklenmedi. "
                "Yanlışlıkla bütün indeksi silmemek için işlem durduruldu."
            )

        current_ids = {
            chunk["id"]
            for chunk in chunks
        }

        removed_ids = sorted(
            set(stored_hashes) - current_ids
        )

        changed_chunks = [
            chunk
            for chunk in chunks
            if stored_hashes.get(chunk["id"]) != chunk["content_hash"]
        ]

        print("Yeni veya değişmiş parça:", len(changed_chunks))
        print("Değişmeyen parça:", len(chunks) - len(changed_chunks))
        if changed_chunks:
            response = embed(
                model=index["embedding_model"],
                input=[
                    chunk["embedding_text"]
                    for chunk in changed_chunks
                ],
                truncate=False,
                keep_alive=0,
                options={"num_gpu": 0},
            )

            vectors = response["embeddings"]

            if len(vectors) != len(changed_chunks):
                raise ValueError("Parça ve embedding sayıları eşleşmiyor.")

            for chunk, vector in zip(changed_chunks, vectors):
                if len(vector) != index["embedding_dimension"]:
                    raise ValueError(
                        f"Vektör boyutu uyuşmuyor: {chunk['id']}"
                    )

                chunk["embedding"] = np.array(
                    vector,
                    dtype=np.float32,
                )

            save_chunks(connection, index["id"], changed_chunks)
            print("Veritabanına yazılan parça:", len(changed_chunks))
        deleted_count = delete_chunks(
            connection,
            index["id"],
            removed_ids,
        )

        print("Silinen eski parça:", deleted_count)
        print("İndeks:", index["name"])
        print("Belge sayısı:", len(documents))
        print("Parça sayısı:", len(chunks))


if __name__ == "__main__":
    main()