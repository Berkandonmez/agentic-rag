"""Agent'ın yapılandırılmış karar biçimini tanımlar."""


def build_agent_schema(
    document_ids: set[str],
    allowed_sources: set[str],
) -> dict:
    actions = [
        {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "const": "search",
                },
                "query": {
                    "type": "string",
                    "minLength": 1,
                },
            },
            "required": ["action", "query"],
            "additionalProperties": False,
        }
    ]

    if document_ids:
        actions.append({
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "const": "read",
                },
                "document_id": {
                    "type": "string",
                    "enum": sorted(document_ids),
                },
            },
            "required": ["action", "document_id"],
            "additionalProperties": False,
        })

    if allowed_sources:
        actions.append({
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "const": "answer",
                },
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
            "required": ["action", "answer", "sources"],
            "additionalProperties": False,
        })

    return {"anyOf": actions}

def validate_agent_decision(
    decision: dict,
    document_ids: set[str],
    allowed_sources: set[str],
) -> dict:
    """Model kararının alanlarını ve erişebileceği kaynakları doğrular."""
    if not isinstance(decision, dict):
        raise ValueError("Karar bir JSON nesnesi olmalı.")

    action = decision.get("action")

    if action == "search":
        if set(decision) != {"action", "query"}:
            raise ValueError("Arama kararının alanları geçersiz.")

        query = decision["query"]

        if not isinstance(query, str) or not query.strip():
            raise ValueError("Arama sorgusu boş olamaz.")

    elif action == "read":
        if set(decision) != {"action", "document_id"}:
            raise ValueError("Okuma kararının alanları geçersiz.")

        document_id = decision["document_id"]

        if (
            not isinstance(document_id, str)
            or document_id not in document_ids
        ):
            raise ValueError("Bilinmeyen belge okunamaz.")

    elif action == "answer":
        if set(decision) != {"action", "answer", "sources"}:
            raise ValueError("Cevap kararının alanları geçersiz.")

        answer = decision["answer"]
        sources = decision["sources"]

        if not isinstance(answer, str) or not answer.strip():
            raise ValueError("Cevap boş olamaz.")

        if (
            not isinstance(sources, list)
            or not sources
            or not all(isinstance(source, str) for source in sources)
        ):
            raise ValueError("Kaynaklar boş olmayan bir metin listesi olmalı.")

        if len(sources) != len(set(sources)):
            raise ValueError("Kaynak kimlikleri tekrarlanmamalı.")

        if not set(sources).issubset(allowed_sources):
            raise ValueError("Getirilmemiş kaynak kullanılamaz.")

    else:
        raise ValueError(f"Bilinmeyen karar: {action}")

    return decision