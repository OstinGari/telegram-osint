"""Dispatcher layer for Telegram delivery."""

from __future__ import annotations

import json
import urllib.parse
import urllib.request


def send_message(bot_token: str, chat_id: str, text: str) -> dict:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode("utf-8")

    req = urllib.request.Request(url, data=payload, method="POST")
    with urllib.request.urlopen(req, timeout=20) as response:
        response_text = response.read().decode("utf-8", errors="replace")

    return json.loads(response_text)
