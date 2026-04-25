from __future__ import annotations

from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from typing import Any
from urllib.parse import quote
from xml.etree import ElementTree as ET

SITE_URL = "https://zzddddzz.github.io/rx-shortage-radar/"
STATUS_FEEDS = {
    "Current": "feed-current.xml",
    "Resolved": "feed-resolved.xml",
    "To Be Discontinued": "feed-discontinued.xml",
}


def _date_key(record: dict[str, Any]) -> str:
    return str(record.get("update_date") or record.get("initial_posting_date") or "")


def _rss_date(value: str | None) -> str:
    if value:
        text = value.replace("Z", "+00:00")
        try:
            parsed = datetime.fromisoformat(text)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return format_datetime(parsed.astimezone(timezone.utc), usegmt=True)
        except ValueError:
            pass
        try:
            parsed = datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            return format_datetime(parsed, usegmt=True)
        except ValueError:
            pass
    return format_datetime(datetime.now(timezone.utc), usegmt=True)


def _record_link(record: dict[str, Any]) -> str:
    query = record.get("package_ndc") or record.get("generic_name") or record.get("id") or ""
    return f"{SITE_URL}?q={quote(str(query))}"


def _record_description(record: dict[str, Any]) -> str:
    lines = [
        record.get("presentation"),
        f"Status: {record.get('status') or 'Unknown'}",
        f"Updated: {record.get('update_date') or 'Unknown'}",
        f"Company: {record.get('company_name') or 'None listed'}",
        record.get("related_info"),
    ]
    return "\n".join(str(line) for line in lines if line)


def build_rss(payload: dict[str, Any], *, limit: int = 100, status: str | None = None) -> ET.ElementTree:
    records = list(payload.get("records") or [])
    if status:
        records = [record for record in records if record.get("status") == status]
    records.sort(key=_date_key, reverse=True)

    rss = ET.Element("rss", {"version": "2.0"})
    channel = ET.SubElement(rss, "channel")
    title = "Rx Shortage Radar" if not status else f"Rx Shortage Radar - {status}"
    description = "Latest public FDA drug shortage records from openFDA."
    if status:
        description = f"Latest public FDA drug shortage records with status {status} from openFDA."
    ET.SubElement(channel, "title").text = title
    ET.SubElement(channel, "link").text = SITE_URL
    ET.SubElement(channel, "description").text = description
    ET.SubElement(channel, "language").text = "en-us"
    ET.SubElement(channel, "lastBuildDate").text = _rss_date(payload.get("generated_at"))

    source = payload.get("source") or {}
    if source.get("docs_url"):
        ET.SubElement(channel, "docs").text = source["docs_url"]

    for record in records[:limit]:
        title = f"{record.get('status') or 'Unknown'}: {record.get('generic_name') or 'Unnamed drug'}"
        if record.get("package_ndc"):
            title = f"{title} ({record['package_ndc']})"
        link = _record_link(record)
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = title
        ET.SubElement(item, "link").text = link
        ET.SubElement(item, "guid", {"isPermaLink": "false"}).text = str(record.get("id") or link)
        ET.SubElement(item, "pubDate").text = _rss_date(record.get("update_date"))
        ET.SubElement(item, "description").text = _record_description(record)

    return ET.ElementTree(rss)


def write_rss(payload: dict[str, Any], output_path: str | Path, *, limit: int = 100, status: str | None = None) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tree = build_rss(payload, limit=limit, status=status)
    ET.indent(tree, space="  ")
    tree.write(path, encoding="utf-8", xml_declaration=True)
    path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    return path


def write_status_feeds(payload: dict[str, Any], output_dir: str | Path, *, limit: int = 100) -> dict[str, Path]:
    directory = Path(output_dir)
    return {
        status: write_rss(payload, directory / filename, limit=limit, status=status)
        for status, filename in STATUS_FEEDS.items()
    }
