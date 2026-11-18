"""Model, arama ve çalışma ayarları."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
CHAT_MODEL = "qwen3.5:9b"
EMBEDDING_MODEL = "embeddinggemma:300m"
CHAT_KEEP_ALIVE = "30m"
CHAT_OPTIONS = {
    "num_ctx": 8192,
    "num_predict": 1024,
    "temperature": 0,
}
QUERY_EMBEDDING_OPTIONS = {"num_gpu": 0}
CHUNK_SIZE = 100
CHUNK_OVERLAP = 20
RETRIEVAL_CANDIDATES = 10
RETRIEVAL_TOP_K = 5
RRF_CONSTANT = 60
MAX_STEPS = 7
RAG_INDEX_NAME = "company_docs_v1"