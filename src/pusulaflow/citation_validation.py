"""Cevaptaki Markdown kaynak kimliklerini kontrol eder."""
import re


def check_citations(
    answer: str,
    allowed_sources: set[str],
) -> dict:
    cited_sources = set(
        re.findall(
            r"[\w.-]+\.md(?:#chunk-\d+)?",
            answer,
        )
    )

    unknown_sources = cited_sources - allowed_sources

    return {
        "missing": not cited_sources,
        "cited_sources": sorted(cited_sources),
        "unknown_sources": sorted(unknown_sources),
    }

def collect_source_ids(tool_name: str, result) -> set[str]:
    source_ids = set()

    if tool_name == "search_documents" and isinstance(result, list):
        for item in result:
            parts = [item] + item.get("neighbor_chunks", [])

            for part in parts:
                source_ids.add(part["id"])
                source_ids.add(part["document_id"])

    elif (
        tool_name == "read_document"
        and isinstance(result, dict)
        and "error" not in result
    ):
        source_ids.add(result["id"])

    return source_ids

def build_answer_schema(allowed_sources: set[str]) -> dict:
    if not allowed_sources:
        raise ValueError(
            "Kaynak olmadan kaynaklı cevap şeması oluşturulamaz."
        )

    return {
        "type": "object",
        "properties": {
            "answer": {
                "type": "string",
                "minLength": 1,
            },
            "sources": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": sorted(allowed_sources),
                },
                "minItems": 1,
                "uniqueItems": True,
            },
        },
        "required": ["answer", "sources"],
        "additionalProperties": False,
    }