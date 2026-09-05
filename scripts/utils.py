#!/usr/bin/env python3
"""
utils.py — Core utility functions for AEO skill.

Provides helper functions for URL validation, text processing,
readability scoring, and data persistence using Python standard library only.
"""

import json
import logging
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("aeo.utils")


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning default if denominator is zero."""
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (TypeError, ZeroDivisionError):
        return default


def validate_url(url: str) -> bool:
    """Validate if a string is a valid HTTP/HTTPS URL."""
    try:
        result = urlparse(url)
        return all([result.scheme in ["http", "https"], result.netloc])
    except Exception:
        return False


def load_json_file(file_path: Union[str, Path], default: Any = None) -> Any:
    """Safely load data from a JSON file."""
    path = Path(file_path)
    if not path.exists():
        return default if default is not None else {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading JSON from {file_path}: {e}")
        return default if default is not None else {}


def save_json_file(file_path: Union[str, Path], data: Any, indent: int = 2) -> bool:
    """Safely save data to a JSON file."""
    path = Path(file_path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"Error saving JSON to {file_path}: {e}")
        return False


def count_syllables(word: str) -> int:
    """Heuristic syllable count for English words."""
    word = word.lower().strip()
    if not word:
        return 0
    if len(word) <= 3:
        return 1
    word = re.sub(r"(?:[^laeiouy]|ed|es|e)$", "", word)
    word = re.sub(r"^y", "", word)
    matches = re.findall(r"[aeiouy]{1,2}", word)
    return max(1, len(matches))


def calculate_readability(text: str) -> Dict[str, Union[float, str]]:
    """
    Calculate readability metrics including Flesch Reading Ease.
    Score ranges:
      90-100: Very Easy (5th grade)
      60-70: Standard (8th-9th grade)
      30-50: Difficult (college)
      0-30: Very Difficult (graduate)
    """
    clean = re.sub(r"[#*_`\[\]\(\)<>]", " ", text)
    sentences = [s.strip() for s in re.split(r"[.!?]+", clean) if s.strip()]
    words = [w.strip() for w in re.findall(r"\b\w+\b", clean) if w.strip()]

    sentence_count = max(1, len(sentences))
    word_count = max(1, len(words))
    syllable_count = sum(count_syllables(w) for w in words)

    asl = word_count / sentence_count
    asw = syllable_count / word_count
    flesch = 206.835 - (1.015 * asl) - (84.6 * asw)
    flesch_clamped = max(0.0, min(100.0, flesch))

    if flesch_clamped >= 80:
        grade = "Easy (General Audience)"
    elif flesch_clamped >= 60:
        grade = "Standard (High School / General Web)"
    elif flesch_clamped >= 40:
        grade = "Fairly Difficult (Professional / Tech)"
    else:
        grade = "Academic / Research Level"

    return {
        "flesch_reading_ease": round(flesch_clamped, 1),
        "reading_level": grade,
        "avg_sentence_length": round(asl, 1),
        "total_words": word_count,
        "total_sentences": sentence_count,
    }


def clean_markdown(text: str) -> str:
    """Strip markdown formatting for pure text analysis."""
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = re.sub(r"`.*?`", "", text)
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"[*_~>]", "", text)
    return text.strip()


def get_iso_timestamp() -> str:
    """Return current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()
