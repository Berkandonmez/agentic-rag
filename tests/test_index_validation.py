import hashlib
import unittest
from unittest.mock import patch

from pusulaflow.index_validation import validate_sources


class SourceValidationTests(unittest.TestCase):
    def setUp(self):
        self.index = {
            "id": 1,
            "chunk_size": 100,
            "chunk_overlap": 20,
            "document_prefix": "title: {document_id} | text: {text}",
        }

        self.original_document = {
            "id": "example.md",
            "source": "example.md",
            "text": "ilk metin",
        }

        self.stored_hashes = {
            "example.md#chunk-1": hashlib.sha256(
                b"title: example.md | text: ilk metin"
            ).hexdigest()
        }

    def test_unchanged_source_is_accepted(self):
        with patch(
            "pusulaflow.index_validation.get_chunk_hashes",
            return_value=self.stored_hashes,
        ):
            validate_sources(
                None,
                self.index,
                [self.original_document],
            )

    def test_source_changes_require_reindexing(self):
        changed_document = {
            **self.original_document,
            "text": "yeni metin",
        }

        added_document = {
            "id": "other.md",
            "source": "other.md",
            "text": "başka belge",
        }

        cases = {
            "content_changed": [changed_document],
            "document_added": [self.original_document, added_document],
            "document_removed": [],
        }

        for case_name, documents in cases.items():
            with self.subTest(case=case_name):
                with patch(
                    "pusulaflow.index_validation.get_chunk_hashes",
                    return_value=self.stored_hashes,
                ):
                    with self.assertRaises(ValueError):
                        validate_sources(None, self.index, documents)


if __name__ == "__main__":
    unittest.main()