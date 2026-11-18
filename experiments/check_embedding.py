from ollama import embed

from pusulaflow.config import EMBEDDING_MODEL


def main():
    response = embed(
        model=EMBEDDING_MODEL,
        input="task: search result | query: bağlantı kontrolü",
        truncate=False,
        keep_alive=0,
        options={"num_gpu": 0},
    )

    vector = response["embeddings"][0]

    print("Model:", EMBEDDING_MODEL)
    print("Vektör boyutu:", len(vector))


if __name__ == "__main__":
    main()