"""Test calculation boundaries and knowledge-search failure handling."""

import json
import unittest
from unittest.mock import patch

from src.tools import calculate_medication_volume, search_knowledge


class TestCalculationTool(unittest.TestCase):

    def calculate(self, dose, concentration):
        return json.loads(calculate_medication_volume.invoke({
            "prescribed_dose_mg": dose,
            "concentration_mg_per_ml": concentration,
        }))

    def test_valid_volume(self):
        result = self.calculate(250, 50)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["volume_ml"], 5.0)

    def test_fractional_volume(self):
        result = self.calculate(125, 50)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["volume_ml"], 2.5)

    def test_zero_concentration(self):
        result = self.calculate(250, 0)
        self.assertEqual(result["status"], "invalid_input")

    def test_negative_inputs(self):
        for dose, concentration in [(-250, 50), (250, -50)]:
            with self.subTest(dose=dose, concentration=concentration):
                result = self.calculate(dose, concentration)
                self.assertEqual(result["status"], "invalid_input")

    def test_nonfinite_inputs(self):
        for value in [float("inf"), float("-inf"), float("nan")]:
            with self.subTest(value=value):
                result = self.calculate(value, 50)
                self.assertEqual(result["status"], "invalid_input")


class TestKnowledgeTool(unittest.TestCase):

    def test_empty_question(self):
        result = json.loads(search_knowledge.invoke({"query": " "}))
        self.assertEqual(result["status"], "invalid_input")

    def test_oversized_question(self):
        result = json.loads(search_knowledge.invoke({
            "query": "x" * 1501,
        }))
        self.assertEqual(result["status"], "invalid_input")

    @patch("src.tools.get_retriever")
    def test_search_failure_is_handled(self, mock_retriever):
        mock_retriever.side_effect = RuntimeError("private diagnostic")
        result = json.loads(search_knowledge.invoke({
            "query": "What is covered?",
        }))

        self.assertEqual(result["status"], "error")
        self.assertNotIn("private diagnostic", result["message"])


if __name__ == "__main__":
    unittest.main()

    