from collections import Counter


def normalize_tokens(text: str) -> Counter:
    """Split text by whitespace and normalize words for case-insensitive counting."""

    tokens = [token.strip().lower() for token in text.split() if token.strip()]
    return Counter(tokens)
