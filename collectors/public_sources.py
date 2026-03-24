"""Collector layer for public OSINT data sources.

This module intentionally avoids private or authenticated data collection.
It only demonstrates safe pulls from open RSS feeds and static source lists.
"""

from __future__ import annotations

import json
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


@dataclass
class RawItem:
    source: str
    timestamp: str
    content: str
    link: str


def _now_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def _read_sources_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def collect_rss_items(rss_urls: Iterable[str], max_items_per_feed: int = 5) -> list[RawItem]:
    items: list[RawItem] = []

    for url in rss_urls:
        try:
            with urllib.request.urlopen(url, timeout=20) as response:
                xml_bytes = response.read()
        except Exception as exc:
            items.append(
                RawItem(
                    source="rss",
                    timestamp=_now_iso(),
                    content=f"RSS fetch failed for {url}: {exc}",
                    link=url,
                )
            )
            continue

        try:
            root = ET.fromstring(xml_bytes)
        except ET.ParseError:
            items.append(
                RawItem(
                    source="rss",
                    timestamp=_now_iso(),
                    content=f"RSS parse failed for {url}",
                    link=url,
                )
            )
            continue

        channel_items = root.findall(".//item")[:max_items_per_feed]
        for item in channel_items:
            title = (item.findtext("title") or "(no title)").strip()
            link = (item.findtext("link") or url).strip()
            pub_date = (item.findtext("pubDate") or _now_iso()).strip()

            items.append(
                RawItem(
                    source="rss",
                    timestamp=pub_date,
                    content=title,
                    link=link,
                )
            )

    return items


def collect_seed_items(sources_path: Path) -> list[RawItem]:
    cfg = _read_sources_config(sources_path)

    static_items = [
        RawItem(
            source="telegram",
            timestamp=_now_iso(),
            content=f"Monitoring public Telegram preview: {channel}",
            link=channel,
        )
        for channel in cfg.get("telegram_channels", [])
    ]

    static_items.extend(
        RawItem(
            source="github",
            timestamp=_now_iso(),
            content=f"Planned GitHub search query: {query}",
            link="https://github.com/search?q=" + query.replace(" ", "+"),
        )
        for query in cfg.get("github_queries", [])
    )

    static_items.extend(collect_rss_items(cfg.get("rss_feeds", [])))
    return static_items
