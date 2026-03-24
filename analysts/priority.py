"""Analyst layer: convert normalized records into alert objects."""

from __future__ import annotations

from collections import Counter


def build_report(records: list[dict]) -> dict:
    source_counts = Counter(item["source"] for item in records)

    alerts = []
    for item in records:
        score = item.get("importance_hint", 0)
        if score >= 2:
            priority = "HIGH"
            confidence = 0.85
        elif score == 1:
            priority = "MEDIUM"
            confidence = 0.65
        else:
            priority = "LOW"
            confidence = 0.45

        alerts.append(
            {
                "priority": priority,
                "summary": item["content"],
                "entities": [item["source"]],
                "confidence": confidence,
                "link": item["link"],
                "timestamp": item["timestamp"],
            }
        )

    return {
        "total_records": len(records),
        "source_breakdown": dict(source_counts),
        "alerts": alerts,
    }


def format_telegram_message(report: dict, top_n: int = 5) -> str:
    lines = [
        "OSINT Monitor Report",
        f"Total records: {report['total_records']}",
        f"Sources: {report['source_breakdown']}",
        "",
        "Top alerts:",
    ]

    for idx, alert in enumerate(report["alerts"][:top_n], start=1):
        lines.append(f"{idx}. [{alert['priority']}] {alert['summary']}")
        lines.append(f"   Link: {alert['link']}")

    if not report["alerts"]:
        lines.append("No alerts generated.")

    return "\n".join(lines)
