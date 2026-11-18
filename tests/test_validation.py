"""Test citation checks without making API requests."""

import json
import unittest
from unittest.mock import patch

from src.validation import (
    FALLBACK,
    approve_answer,
    citations_match_evidence,
)


class TestCitationValidation(unittest.TestCase):

    def setUp(self):
        self.evidence = [json.dumps({
            "status": "candidate_passages",
            "passages": [{
                "source": "insurance_policy.md",
                "section": "Outpatient consultations",
                "text": "The patient pays 20%.",
            }],
        })]

    def test_matching_citation(self):
        answer = (
            "The patient pays 20% "
            "[insurance_policy.md | Outpatient consultations]."
        )
        self.assertTrue(
            citations_match_evidence(answer, self.evidence)
        )

    def test_invented_filename(self):
        answer = "Covered [invented.md | Outpatient consultations]."
        self.assertFalse(
            citations_match_evidence(answer, self.evidence)
        )

    def test_invented_section(self):
        answer = "Covered [insurance_policy.md | Dental benefits]."
        self.assertFalse(
            citations_match_evidence(answer, self.evidence)
        )

    def test_citation_without_separator(self):
        answer = "Covered [insurance_policy.md]."
        self.assertFalse(
            citations_match_evidence(answer, self.evidence)
        )

    def test_citation_without_evidence(self):
        answer = (
            "The patient pays 20% "
            "[insurance_policy.md | Outpatient consultations]."
        )
        self.assertFalse(citations_match_evidence(answer, []))

    def test_privacy_placeholder_is_not_a_citation(self):
        answer = "Your email is [EMAIL_example_1]."
        self.assertTrue(citations_match_evidence(answer, []))

    def test_malformed_evidence(self):
        self.assertFalse(
            citations_match_evidence("An answer.", ["invalid JSON"])
        )

    @patch("src.validation.ChatOpenAI")
    def test_invalid_citation_blocks_model_review(self, mock_model):
        answer = "Covered [invented.md | Invented section]."
        result = approve_answer(answer, self.evidence)

        self.assertEqual(result, FALLBACK)
        mock_model.assert_not_called()


if __name__ == "__main__":
    unittest.main()
    