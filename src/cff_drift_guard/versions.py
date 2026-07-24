"""Version normalization functions used by the benchmark."""

from __future__ import annotations

import re


def exact_version(value: str) -> str:
    """Normalize only whitespace and one leading v/V."""
    normalized = value.strip()
    if len(normalized) > 1 and normalized[0].lower() == "v" and normalized[1].isdigit():
        normalized = normalized[1:]
    return normalized


def core_version(value: str) -> str:
    """Return a conservative release core for sensitivity analysis.

    Build/local metadata and common pre-release suffixes are removed. Numeric
    trailing zero components are removed, but at least one component remains.
    Non-numeric cores are returned lower-cased after exact normalization.
    """
    normalized = exact_version(value).split("+", 1)[0]
    normalized = re.sub(r"[._-](?:dev|alpha|a|beta|b|rc|pre|post)\.?\d*$", "", normalized, flags=re.I)
    parts = normalized.split(".")
    if all(part.isdigit() for part in parts) and all(part != "" for part in parts):
        while len(parts) > 1 and int(parts[-1]) == 0:
            parts.pop()
        return ".".join(parts)
    return normalized.lower()
