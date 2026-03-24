#!/usr/bin/env python3
"""End-to-end OSINT pipeline runner.

Pipeline:
SOURCE -> Collector -> Processor -> Analyst -> Dispatcher
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysts.priority import build_report, format_telegram_message
from collectors.public_sources import collect_seed_items
from dispatcher.telegram import send_message
from processors.normalize import normalize_records

OUTPUT_DIR = ROOT / "output"
SOURCES_FILE = ROOT / "sources" / "sources.json"


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw_items = collect_seed_items(SOURCES_FILE)
    normalized = normalize_records(raw_items)
    report = build_report(normalized)
    telegram_text = format_telegram_message(report)

    (OUTPUT_DIR / "raw.json").write_text(
        json.dumps([item.__dict__ for item in raw_items], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (OUTPUT_DIR / "processed.json").write_text(
        json.dumps(normalized, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (OUTPUT_DIR / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUTPUT_DIR / "telegram_message.txt").write_text(telegram_text, encoding="utf-8")

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if bot_token and chat_id:
        response = send_message(bot_token=bot_token, chat_id=chat_id, text=telegram_text)
        (OUTPUT_DIR / "telegram_response.json").write_text(
            json.dumps(response, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print("Telegram message sent.")
    else:
        print("Telegram credentials are not set. Wrote local output only.")

    print(f"Report generated at: {OUTPUT_DIR / 'report.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
