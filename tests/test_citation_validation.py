import unittest

from pusulaflow.citation_validation import check_citations


class CitationValidationTests(unittest.TestCase):
    def setUp(self):
        self.allowed_sources = {
            "packets.md",
            "packets.md#chunk-2",
        }

    def test_retrieved_source_is_accepted(self):
        result = check_citations(
            "Kaynak: `packets.md#chunk-2`",
            self.allowed_sources,
        )

        self.assertFalse(result["missing"])
        self.assertEqual(
            result["cited_sources"],
            ["packets.md#chunk-2"],
        )
        self.assertEqual(result["unknown_sources"], [])

    def test_missing_source_is_detected(self):
        result = check_citations(
            "Askıya alınmış hesaplar kotaya dahildir.",
            self.allowed_sources,
        )

        self.assertTrue(result["missing"])
        self.assertEqual(result["cited_sources"], [])

    def test_unretrieved_source_is_detected(self):
        result = check_citations(
            "Kaynak: packets.md#chunk-99",
            self.allowed_sources,
        )

        self.assertFalse(result["missing"])
        self.assertEqual(
            result["unknown_sources"],
            ["packets.md#chunk-99"],
        )


if __name__ == "__main__":
    unittest.main()