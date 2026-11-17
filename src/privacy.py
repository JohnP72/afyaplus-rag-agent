"""Mask emails and Kenyan mobile numbers before model processing."""

import re
from uuid import uuid4


EMAIL_PATTERN = re.compile(
    r"(?<![\w.+-])"
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    r"(?![\w-])"
)

PHONE_PATTERN = re.compile(
    r"(?<!\w)"
    r"(?:\+254|254|0)[ -]?[17](?:[ -]?\d){8}"
    r"(?!\w)"
)


class PrivacyMasker:
    """Keep a private placeholder mapping for one conversation session."""

    def __init__(self) -> None:
        self._originals: dict[str, str] = {}
        self._session_tag = uuid4().hex

    def _placeholder(self, value: str, category: str) -> str:
        """Reuse a placeholder when the same value appears again."""
        for token, original in self._originals.items():
            if original == value:
                return token

        number = len(self._originals) + 1
        token = f"[{category}_{self._session_tag}_{number}]"
        self._originals[token] = value
        return token

    def mask(self, text: str) -> str:
        """Replace supported email and phone patterns with placeholders."""
        if not isinstance(text, str):
            raise TypeError("Input must be text.")

        masked = EMAIL_PATTERN.sub(
            lambda match: self._placeholder(match.group(), "EMAIL"),
            text,
        )

        return PHONE_PATTERN.sub(
            lambda match: self._placeholder(match.group(), "PHONE"),
            masked,
        )

    def restore(self, approved_text: str) -> str:
        """Restore this session's placeholders in an approved final answer."""
        if not isinstance(approved_text, str):
            raise TypeError("Output must be text.")

        if not self._originals:
            return approved_text

        token_pattern = re.compile(
            "|".join(re.escape(token) for token in self._originals)
        )

        return token_pattern.sub(
            lambda match: self._originals[match.group()],
            approved_text,
        )

    def clear(self) -> None:
        """Discard the private mapping when the session ends."""
        self._originals.clear()

