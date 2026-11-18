import io
import json
import unittest
from contextlib import redirect_stdout
from types import SimpleNamespace
from unittest.mock import Mock, patch

from pusulaflow.agent import run_cli


def make_response(decision):
    return SimpleNamespace(
        message=SimpleNamespace(
            content=json.dumps(decision, ensure_ascii=False),
        ),
        load_duration=0,
        prompt_eval_duration=0,
        eval_duration=0,
        done_reason="stop",
        eval_count=1,
    )


class AgentCitationTests(unittest.TestCase):
    def setUp(self):
        self.tools = {
            "list_documents": Mock(return_value=[
                {"id": "example.md", "preview": "Örnek belge"},
            ]),
            "search_documents": Mock(return_value=[
                {
                    "id": "example.md#chunk-1",
                    "document_id": "example.md",
                    "text": "Örnek kaynak metni.",
                    "neighbor_chunks": [],
                },
            ]),
            "read_document": Mock(return_value={
                "id": "example.md",
                "text": "Belgenin tam içeriği.",
            }),
        }

    def run_case(self, decisions):
        output = io.StringIO()

        with (
            patch(
                "pusulaflow.agent.chat",
                side_effect=[
                    make_response(decision)
                    for decision in decisions
                ],
            ) as chat_mock,
            patch(
                "builtins.input",
                side_effect=["Test sorusu", "/exit"],
            ),
            patch("pusulaflow.agent.logger"),
            redirect_stdout(output),
        ):
            run_cli(self.tools)

        return output.getvalue(), chat_mock

    def test_valid_answer_needs_one_call(self):
        output, chat_mock = self.run_case([
            {
                "action": "answer",
                "answer": "Kaynaklı cevap.",
                "sources": ["example.md#chunk-1"],
            },
        ])

        self.assertEqual(chat_mock.call_count, 1)
        self.assertIn("Nihai yanıt: Kaynaklı cevap.", output)
        self.assertIn("Kaynaklar: example.md#chunk-1", output)
        self.tools["read_document"].assert_not_called()

    def test_missing_sources_blocks_answer(self):
        output, chat_mock = self.run_case([
            {
                "action": "answer",
                "answer": "GÖSTERİLMEMELİ",
                "sources": [],
            },
        ])

        self.assertEqual(chat_mock.call_count, 1)
        self.assertNotIn("GÖSTERİLMEMELİ", output)
        self.assertNotIn("Nihai yanıt:", output)
        self.assertIn("Cevap gösterilmedi.", output)

    def test_unknown_source_blocks_answer(self):
        output, _ = self.run_case([
            {
                "action": "answer",
                "answer": "GÖSTERİLMEMELİ",
                "sources": ["unknown.md"],
            },
        ])

        self.assertNotIn("GÖSTERİLMEMELİ", output)
        self.assertNotIn("Nihai yanıt:", output)

    def test_read_decision_reads_document_before_answer(self):
        output, chat_mock = self.run_case([
            {
                "action": "read",
                "document_id": "example.md",
            },
            {
                "action": "answer",
                "answer": "Tam belgeden cevap.",
                "sources": ["example.md"],
            },
        ])

        self.tools["read_document"].assert_called_once_with(
            document_id="example.md"
        )
        self.assertEqual(chat_mock.call_count, 2)
        self.assertIn("Nihai yanıt: Tam belgeden cevap.", output)

        second_messages = chat_mock.call_args_list[1].kwargs["messages"]
        self.assertTrue(any(
            "Belgenin tam içeriği." in message.get("content", "")
            for message in second_messages
        ))

    def test_search_decision_runs_targeted_search(self):
        # İlk arama boş; sonraki arama kaynak getiriyor.
        self.tools["search_documents"].side_effect = [
            [],
            [
                {
                    "id": "example.md#chunk-2",
                    "document_id": "example.md",
                    "text": "Hedefli aramayla bulunan bilgi.",
                    "neighbor_chunks": [],
                },
            ],
        ]

        output, chat_mock = self.run_case([
            {
                "action": "search",
                "query": "Eksik bilgi için sorgu",
            },
            {
                "action": "answer",
                "answer": "Yeni kaynaktan cevap.",
                "sources": ["example.md#chunk-2"],
            },
        ])

        self.assertEqual(chat_mock.call_count, 2)
        self.assertEqual(
            self.tools["search_documents"].call_count,
            2,
        )
        self.tools["search_documents"].assert_called_with(
            query="Eksik bilgi için sorgu"
        )
        self.assertIn("Nihai yanıt: Yeni kaynaktan cevap.", output)


if __name__ == "__main__":
    unittest.main()