"""Input sanitization utilities for text fields."""

import re
import html


def sanitize_text(text: str, max_length: int = 5000) -> str:
    """Sanitize user-provided text to prevent injection attacks.

    - Escapes HTML entities (prevents XSS if rendered)
    - Strips null bytes
    - Truncates to max_length
    - Strips leading/trailing whitespace
    """
    if not text:
        return text
    # Remove null bytes
    text = text.replace("\x00", "")
    # Escape HTML entities
    text = html.escape(text, quote=True)
    # Truncate
    text = text[:max_length]
    # Strip whitespace
    return text.strip()


def sanitize_name(name: str, max_length: int = 200) -> str:
    """Sanitize a name field — alphanumeric, spaces, basic punctuation only."""
    if not name:
        return name
    name = sanitize_text(name, max_length)
    # Allow letters, numbers, spaces, dots, hyphens, accented chars
    name = re.sub(r'[^\w\s.\-àáâãéêíóôõúçÀÁÂÃÉÊÍÓÔÕÚÇ]', '', name)
    return name.strip()
