"""Processor layer: deduplicate and normalize raw collected records."""

from __future__ import annotations

from dataclasses import asdict
from typing import Iterable


def normalize_records(raw_items: Iterable[object]) -> list[dict]:
    seen: set[tuple[str, str]] = set()
    normalized: list[dict] = []

    for item in raw_items:
        row = asdict(item)
        key = (row["content"], row["link"])

        if key in seen:
            continue

        seen.add(key)
        row["content"] = " ".join(row["content"].split())
        row["importance_hint"] = _score_hint(row["content"])
        normalized.append(row)

    return normalized


def _score_hint(text: str) -> int:
    keywords = ("leak", "breach", "exploit", "malware", "alert", "ransomware")
    lowered = text.lower()
    return sum(1 for kw in keywords if kw in lowered)
