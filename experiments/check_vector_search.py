import numpy as np
from ollama import embed

from pusulaflow.config import RAG_INDEX_NAME
from pusulaflow.database import get_connection, get_index, search_chunks


def main():
    question = "Askıya alınmış hesaplar kullanıcı kotasına dahil mi?"

    with get_connection() as connection:
        index = get_index(connection, RAG_INDEX_NAME)

        query_text = index["query_prefix"].format(query=question)

        response = embed(
            model=index["embedding_model"],
            input=query_text,
            truncate=False,
            keep_alive=0,
            options={"num_gpu": 0},
        )

        query_vector = np.array(
            response["embeddings"][0],
            dtype=np.float32,
        )

        results = search_chunks(
            connection,
            index_id=index["id"],
            query_vector=query_vector,
            top_k=3,
        )

        for result in results:
            print("\nParça:", result["id"])
            print("Benzerlik:", round(result["vector_score"], 4))
            print("Metin:", result["text"])


if __name__ == "__main__":
    main()