"""Kaynak araçlarını kullanan etkileşimli agent döngüsü."""
import json
import logging
from time import perf_counter

from ollama import chat

from pusulaflow.config import CHAT_MODEL, CHAT_KEEP_ALIVE, CHAT_OPTIONS, MAX_STEPS
from pusulaflow.prompts import SYSTEM_PROMPT
from pusulaflow.citation_validation import collect_source_ids
from pusulaflow.agent_protocol import build_agent_schema, validate_agent_decision


logger = logging.getLogger("agentic_rag")


def format_tool_result(tool_name: str, result) -> str:
    """Araç sonuçlarını modele okunabilir kaynak bloklarıyla sunar."""
    if tool_name == "search_documents" and isinstance(result, list):
        blocks = []
        seen_ids = set()

        for item in result:
            parts = [item] + item.get("neighbor_chunks", [])

            for part in parts:
                chunk_id = part["id"]

                if chunk_id in seen_ids:
                    continue

                seen_ids.add(chunk_id)

                blocks.append(
                    f"Kaynak: {chunk_id}\n"
                    f"Belge kimliği: {part['document_id']}\n"
                    f"Metin:\n{part['text']}"
                )

        if not blocks:
            return "Aramada belge parçası bulunamadı."

        return "\n\n---\n\n".join(blocks)

    if (
        tool_name == "read_document"
        and isinstance(result, dict)
        and "error" not in result
    ):
        return (
            f"Kaynak: {result['id']}\n"
            f"Metin:\n{result['text']}"
        )

    return json.dumps(result, ensure_ascii=False)

def run_cli(available_tools: dict) -> None:
    """Soruları alır ve yapılandırılmış agent kararlarını yürütür."""
    document_list = available_tools["list_documents"]()
    document_ids = {
        document["id"]
        for document in document_list
    }

    protocol_prompt = (
        "\n\nKarar protokolü:\n"
        "Her turda JSON şemasına uygun tek karar ver.\n"
        "search: Eksik bilgi için sorguyu query alanına yaz.\n"
        "read: Tamamını okuyacağın bilinen belgeyi document_id alanına yaz.\n"
        "answer: Cevabı answer alanına, kullandığın kaynak "
        "kimliklerini sources listesine yaz. "
        "answer içinde ayrıca kaynak listesi oluşturma.\n"
        "İlk arama Python tarafından yapılmıştır. "
        "Kaynaklar yeterliyse cevap ver; yetersizse search veya read seç. "
        "Aynı işlemi gereksiz yere tekrarlama."
    )

    while True:
        question = input("\nSorunuz (çıkış: /exit): ").strip()

        if question.lower() == "/exit":
            break

        if not question:
            print("Lütfen bir soru giriniz.")
            continue

        answer_started = perf_counter()

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT + protocol_prompt,
            },
            {
                "role": "user",
                "content": question,
            },
        ]

        print("İlk belge araması yapılıyor...")

        initial_result = available_tools["search_documents"](
            query=question
        )

        allowed_sources = collect_source_ids(
            "search_documents",
            initial_result,
        )

        initial_context = format_tool_result(
            "search_documents",
            initial_result,
        )

        logger.debug(
            "Soru: %s\nİlk arama kaynakları:\n%s",
            question,
            initial_context,
        )

        messages.append({
            "role": "user",
            "content": (
                "Bilinen belgeler — bu liste içeriklerinin "
                "okunduğu anlamına gelmez:\n"
                + json.dumps(document_list, ensure_ascii=False)
                + "\n\nPython tarafından yapılan ilk aramanın sonucu:\n"
                + initial_context
            ),
        })

        for step in range(MAX_STEPS):
            print(f"\nStep: {step + 1}")

            schema = build_agent_schema(
                document_ids=document_ids,
                allowed_sources=allowed_sources,
            )

            llm_started = perf_counter()

            response = chat(
                model=CHAT_MODEL,
                messages=messages,
                format=schema,
                think=False,
                keep_alive=CHAT_KEEP_ALIVE,
                options=CHAT_OPTIONS,
            )

            print(
                f"LLM çağrısı: {perf_counter() - llm_started:.2f} sn",
                flush=True,
            )
            print(
                f"Model yükleme: "
                f"{(response.load_duration or 0) / 1e9:.2f} sn"
            )
            print(
                f"Girdi işleme: "
                f"{(response.prompt_eval_duration or 0) / 1e9:.2f} sn"
            )
            print(
                f"Üretim: {(response.eval_duration or 0) / 1e9:.2f} sn"
            )
            print("Bitiş nedeni:", response.done_reason)
            print("Üretilen token:", response.eval_count)

            if response.done_reason == "length":
                print(
                    "Model çıktısı tamamlanmadan kesildi. "
                    "Eksik cevap gösterilmedi."
                )
                break

            try:
                decision = validate_agent_decision(
                    json.loads(response.message.content or ""),
                    document_ids=document_ids,
                    allowed_sources=allowed_sources,
                )
            except ValueError as error:
                logger.warning(
                    "Geçersiz agent kararı: %s | Çıktı: %s",
                    error,
                    response.message.content,
                )
                print(
                    "Model kararı biçim veya kaynak kontrolünü geçmedi. "
                    "Cevap gösterilmedi."
                )
                break

            logger.debug("Doğrulanmış agent kararı: %s", decision)

            messages.append({
                "role": "assistant",
                "content": json.dumps(
                    decision,
                    ensure_ascii=False,
                ),
            })

            if decision["action"] == "answer":
                print("Nihai yanıt:", decision["answer"])
                print("Kaynaklar:", ", ".join(decision["sources"]))
                break

            if decision["action"] == "search":
                tool_name = "search_documents"
                arguments = {"query": decision["query"]}
            else:
                tool_name = "read_document"
                arguments = {
                    "document_id": decision["document_id"]
                }

            print("Araç:", tool_name)
            print("Parametreler:", arguments)

            result = available_tools[tool_name](**arguments)

            allowed_sources.update(
                collect_source_ids(tool_name, result)
            )

            logger.debug(
                "Araç: %s | Sonuç: %s",
                tool_name,
                result,
            )

            messages.append({
                "role": "user",
                "content": (
                    f"Python tarafından gerçekleştirilen "
                    f"{tool_name} işleminin sonucu:\n"
                    + format_tool_result(tool_name, result)
                ),
            })

        else:
            print(
                "Maksimum adım sayısına ulaşıldı. "
                "Nihai yanıt alınamadı."
            )

        print(
            f"Sorudan yanıta toplam: "
            f"{perf_counter() - answer_started:.2f} sn"
        )
        print("--------------------------------------------------")