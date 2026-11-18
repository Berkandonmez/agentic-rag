from pusulaflow.config import RAG_INDEX_NAME
from pusulaflow.database import get_connection, get_index


def main():
    with get_connection() as connection:
        index = get_index(connection, RAG_INDEX_NAME)

        for key, value in index.items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()