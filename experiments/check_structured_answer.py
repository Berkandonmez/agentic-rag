"""Koşul eşleştirmeli yapılandırılmış cevap denemesi."""

import json
from time import perf_counter

from ollama import chat

from pusulaflow.agent import format_tool_result
from pusulaflow.citation_validation import (
    build_answer_schema,
    collect_source_ids,
)
from pusulaflow.config import (
    CHAT_MODEL,
    CHAT_KEEP_ALIVE,
    CHAT_OPTIONS,
    RAG_INDEX_NAME,
)
from pusulaflow.database import get_connection, get_index
from pusulaflow.prompts import SYSTEM_PROMPT
from pusulaflow.retrieval import HybridRetriever


def normalize(text: str) -> str:
    """Alıntı kontrolünde boşluk ve satır sonlarını eşitler."""
    return " ".join(text.split())


def main():
    question = input("Deneme sorusu: ").strip()

    if not question:
        print("Lütfen bir soru giriniz.")
        return

    with get_connection(autocommit=True) as connection:
        index = get_index(connection, RAG_INDEX_NAME)
        retriever = HybridRetriever(connection, index)
        results = retriever.search_documents(question)

    allowed_sources = collect_source_ids(
        "search_documents",
        results,
    )

    # Her kimlik için gerçekten getirilen metinleri saklıyoruz.
    source_texts = {}

    for item in results:
        for part in [item] + item.get("neighbor_chunks", []):
            for source_id in {part["id"], part["document_id"]}:
                source_texts.setdefault(source_id, []).append(
                    normalize(part["text"])
                )

    schema = build_answer_schema(allowed_sources)

    check_schema = {
        "type": "object",
        "properties": {
            "condition": {
                "type": "string",
                "minLength": 1,
            },
            "case_fact": {
                "type": "string",
                "minLength": 1,
            },
            "status": {
                "type": "string",
                "enum": ["met", "not_met", "unknown"],
            },
            "source": {
                "type": "string",
                "enum": sorted(allowed_sources),
            },
            "quote": {
                "type": "string",
                "minLength": 1,
            },
        },
        "required": [
            "condition",
            "case_fact",
            "status",
            "source",
            "quote",
        ],
        "additionalProperties": False,
    }

    schema["properties"] = {
        "checks": {
            "type": "array",
            "items": check_schema,
            "minItems": 1,
        },
        **schema["properties"],
    }
    schema["required"] = ["checks", "answer", "sources"]

    context = format_tool_result(
        "search_documents",
        results,
    )

    started = perf_counter()

    response = chat(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    SYSTEM_PROMPT
                    + "\nÇıktıyı verilen JSON şemasında üret. "
                    "checks alanında kararı belirleyen koşulları "
                    "kısa kayıtlar olarak göster. "
                    "condition kaynaktaki koşul, case_fact kullanıcının "
                    "verdiği ilgili bilgi olsun. "
                    "status: koşul sağlanıyorsa met, "
                    "sağlanmıyorsa not_met, bilgi eksikse unknown. "
                    "Her kayıt için source ve kaynaktan aynen alınmış "
                    "kısa bir quote ver. "
                    "Birlikte gereken koşulları ayrı kayıtlarla göster. "
                    "Kullanıcının vermediği olguları ekleme. "
                    "answer alanında bu eşleşmelerle tutarlı kısa "
                    "sonucu yaz; kayıtları tekrar anlatma. "
                    "Kullandığın kaynakları sources listesine yaz."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Soru:\n{question}\n\n"
                    f"Kaynak içerikleri:\n{context}"
                ),
            },
        ],
        format=schema,
        think=False,
        keep_alive=CHAT_KEEP_ALIVE,
        options=CHAT_OPTIONS,
    )

    print(
        "LLM süresi:",
        round(perf_counter() - started, 2),
        "sn",
    )
    print("Bitiş nedeni:", response.done_reason)

    if response.done_reason == "length":
        raise ValueError("Çıktı kesildi; kabul edilmedi.")

    result = json.loads(response.message.content or "")

    if (
        not isinstance(result, dict)
        or set(result) != {"checks", "answer", "sources"}
    ):
        raise ValueError("Cevap alanları geçersiz.")

    if (
        not isinstance(result["answer"], str)
        or not result["answer"].strip()
    ):
        raise ValueError("Cevap boş veya geçersiz.")

    sources = result["sources"]

    if (
        not isinstance(sources, list)
        or not sources
        or not all(isinstance(source, str) for source in sources)
    ):
        raise ValueError("Kaynak listesi geçersiz.")

    if (
        len(sources) != len(set(sources))
        or not set(sources).issubset(allowed_sources)
    ):
        raise ValueError("Tekrarlanan veya getirilmemiş kaynak var.")

    checks = result["checks"]

    if not isinstance(checks, list) or not checks:
        raise ValueError("Koşul kayıtları eksik.")

    expected_fields = {
        "condition", "case_fact", "status", "source", "quote"
    }

    for check in checks:
        if not isinstance(check, dict) or set(check) != expected_fields:
            raise ValueError("Koşul kaydının alanları geçersiz.")

        if not all(
            isinstance(value, str) and value.strip()
            for value in check.values()
        ):
            raise ValueError("Koşul kaydında boş veya geçersiz değer var.")

        if check["status"] not in {"met", "not_met", "unknown"}:
            raise ValueError("Eşleşme durumu geçersiz.")

        if check["source"] not in sources:
            raise ValueError("Koşul kaynağı cevap kaynaklarında yok.")

        quote = normalize(check["quote"])

        if not any(
            quote in text
            for text in source_texts.get(check["source"], [])
        ):
            raise ValueError("Alıntı belirtilen kaynak metninde bulunamadı.")

    labels = {
        "met": "Sağlanıyor",
        "not_met": "Sağlanmıyor",
        "unknown": "Bilinmiyor",
    }

    for number, check in enumerate(checks, start=1):
        print(f"\nKoşul {number}: {check['condition']}")
        print("Kullanıcı bilgisi:", check["case_fact"])
        print("Eşleşme:", labels[check["status"]])
        print("Alıntı:", check["quote"])
        print("Kaynak:", check["source"])

    print("\nCevap:", result["answer"])
    print("Kaynaklar:", ", ".join(sources))


if __name__ == "__main__":
    main()