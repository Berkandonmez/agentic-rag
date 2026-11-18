import unittest

from pusulaflow.documents import chunk_documents


class ChunkDocumentsTests(unittest.TestCase):
    def test_overlap_preserves_boundary_words(self):
        documents = [{
            "id": "example.md",
            "source": "example.md",
            "text": "bir iki üç dört beş altı yedi",
        }]

        chunks = chunk_documents(
            documents,
            chunk_size=4,
            overlap=1,
        )

        self.assertEqual(
            [chunk["text"] for chunk in chunks],
            [
                "bir iki üç dört",
                "dört beş altı yedi",
            ],
        )

    def test_different_documents_are_not_combined(self):
        documents = [
            {"id": "a.md", "source": "a.md", "text": "bir iki"},
            {"id": "b.md", "source": "b.md", "text": "üç dört"},
        ]

        chunks = chunk_documents(documents, chunk_size=4, overlap=1)

        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[0]["document_id"], "a.md")
        self.assertEqual(chunks[0]["text"], "bir iki")
        self.assertEqual(chunks[1]["document_id"], "b.md")
        self.assertEqual(chunks[1]["text"], "üç dört")

    def test_invalid_settings_are_rejected(self):
        for chunk_size, overlap in [(0, 0), (4, 4), (4, -1)]:
            with self.subTest(chunk_size=chunk_size, overlap=overlap):
                with self.assertRaises(ValueError):
                    chunk_documents(
                        [],
                        chunk_size=chunk_size,
                        overlap=overlap,
                    )


if __name__ == "__main__":
    unittest.main()