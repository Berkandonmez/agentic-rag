"""Uygulamanın başlangıç noktası."""
from pusulaflow.agent import run_cli
from pusulaflow.config import DATA_DIR, RAG_INDEX_NAME, EMBEDDING_MODEL
from pusulaflow.database import get_connection, get_index, validate_index_model
from pusulaflow.documents import load_documents
from pusulaflow.retrieval import HybridRetriever
from pusulaflow.tools import create_tools
from pusulaflow.index_validation import validate_sources
import psycopg
from pusulaflow.logging_config import setup_logging


def main() -> None:
    setup_logging()
    
    documents = load_documents(DATA_DIR)

    with get_connection(autocommit=True) as connection:
        index = get_index(connection, RAG_INDEX_NAME)

        validate_index_model(index, EMBEDDING_MODEL)
        validate_sources(connection, index, documents)

        retriever = HybridRetriever(connection, index)

        available_tools = create_tools(documents, retriever)

        run_cli(available_tools)


if __name__ == "__main__":
    try:
        main()
    except psycopg.OperationalError:
        print(
            "PostgreSQL bağlantısı kurulamadı veya kesildi. "
            "Hizmetin çalıştığını ve .env bağlantı ayarlarını kontrol et. "
            "Ardından uygulamayı yeniden başlat."
        )
    except (KeyboardInterrupt, EOFError):
        print("\nUygulama kapatıldı.")