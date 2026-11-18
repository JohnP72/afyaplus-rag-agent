"""Check masking, restoration, and conversation separation."""

import unittest

from src.privacy import PrivacyMasker


class TestPrivacyMasker(unittest.TestCase):

    def test_kenyan_phone_formats(self):
        numbers = [
            "0712345678",
            "0112345678",
            "+254712345678",
            "+254 712 345 678",
            "254712345678",
            "0712-345-678",
        ]

        for number in numbers:
            with self.subTest(number=number):
                masker = PrivacyMasker()
                original = f"Call me on {number}."
                masked = masker.mask(original)

                self.assertNotIn(number, masked)
                self.assertIn("[PHONE_", masked)
                self.assertEqual(masker.restore(masked), original)

    def test_email_followed_by_full_stop(self):
        masker = PrivacyMasker()
        original = "Email peter.john+test@example.co.ke."
        masked = masker.mask(original)

        self.assertNotIn("peter.john+test@example.co.ke", masked)
        self.assertIn("[EMAIL_", masked)
        self.assertTrue(masked.endswith("."))
        self.assertEqual(masker.restore(masked), original)

    def test_ordinary_text_is_preserved(self):
        masker = PrivacyMasker()
        text = "Does my insurance cover a consultation?"
        self.assertEqual(masker.mask(text), text)

    def test_repeated_value_uses_same_placeholder(self):
        masker = PrivacyMasker()
        first = masker.mask("0712345678")
        second = masker.mask("0712345678")
        self.assertEqual(first, second)

    def test_sessions_are_separate(self):
        first_session = PrivacyMasker()
        second_session = PrivacyMasker()
        token = first_session.mask("0712345678")

        self.assertEqual(second_session.restore(token), token)

    def test_clear_discards_original_values(self):
        masker = PrivacyMasker()
        token = masker.mask("0712345678")
        masker.clear()

        self.assertEqual(masker.restore(token), token)

    def test_invalid_input_is_rejected(self):
        masker = PrivacyMasker()

        with self.assertRaises(TypeError):
            masker.mask(None)


if __name__ == "__main__":
    unittest.main()

    