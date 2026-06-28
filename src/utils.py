"""General utility functions for the AI Failure Observatory."""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from typing import Any


def ensure_dir(path: str) -> str:
    """Create a directory (and parents) if it doesn't exist. Returns the path."""
    os.makedirs(path, exist_ok=True)
    return path


def save_json(data: Any, filepath: str, *, indent: int = 2) -> str:
    """Serialize *data* to a JSON file and return the path."""
    ensure_dir(os.path.dirname(filepath))
    with open(filepath, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=indent, default=str)
    return filepath


def load_json(filepath: str) -> Any:
    """Load and return JSON data from *filepath*."""
    with open(filepath, encoding="utf-8") as fh:
        return json.load(fh)


def utc_now_iso() -> str:
    """Return the current UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


def slugify(text: str) -> str:
    """Convert *text* into a lowercase slug suitable for filenames."""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def truncate(text: str, max_length: int = 200) -> str:
    """Truncate *text* to *max_length* characters, appending '...' if needed."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def word_count(text: str) -> int:
    """Return the number of whitespace-delimited words in *text*."""
    return len(text.split())


def contains_hedging(text: str) -> bool:
    """Heuristic check for hedging language often seen in uncertain responses."""
    hedging_phrases = [
        "i'm not sure",
        "i think",
        "it might be",
        "possibly",
        "it's possible that",
        "i believe",
        "to the best of my knowledge",
        "i could be wrong",
        "approximately",
        "roughly",
    ]
    lower = text.lower()
    return any(phrase in lower for phrase in hedging_phrases)


def contains_confidence_markers(text: str) -> bool:
    """Heuristic check for strong confidence markers."""
    confidence_phrases = [
        "i am certain",
        "without a doubt",
        "definitely",
        "absolutely",
        "there is no question",
        "certainly",
        "it is clear that",
        "undeniably",
        "it is well established",
    ]
    lower = text.lower()
    return any(phrase in lower for phrase in confidence_phrases)


def detect_repetition(text: str, *, window: int = 50) -> float:
    """Return a ratio (0-1) indicating how repetitive *text* is.

    Splits the text into chunks of *window* characters and measures
    the fraction of duplicated chunks.
    """
    if len(text) < window:
        return 0.0
    chunks = [text[i : i + window] for i in range(0, len(text) - window + 1, window)]
    if not chunks:
        return 0.0
    unique = set(chunks)
    return 1.0 - (len(unique) / len(chunks))
