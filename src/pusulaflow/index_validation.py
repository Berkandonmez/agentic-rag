"""Kaynak belgelerle kayıtlı indeksin tutarlılığını kontrol eder."""
#kodun amacı diskteki belgelerle veritabanındaki indeks aynı içeriği temsil ediyor mu? sorusunu cevaplamak
import hashlib

from pusulaflow.database import get_chunk_hashes
from pusulaflow.documents import chunk_documents


def validate_sources(connection, index: dict, documents: list[dict]) -> None:
    chunks = chunk_documents(
        documents,
        chunk_size=index["chunk_size"],
        overlap=index["chunk_overlap"],
    )

    current_hashes = {}

    for chunk in chunks:
        embedding_text = index["document_prefix"].format(
            document_id=chunk["document_id"],
            text=chunk["text"],
        )

        current_hashes[chunk["id"]] = hashlib.sha256(
            embedding_text.encode("utf-8")
        ).hexdigest()

    stored_hashes = get_chunk_hashes(connection, index["id"])

    if current_hashes != stored_hashes:
        raise ValueError(
            "Kaynak belgeler ile kayıtlı indeks uyuşmuyor. "
            "Önce python scripts/index_documents.py çalıştır."
        )