from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone
from typing import Any, Iterable

WORD_RE = re.compile(r"[a-z0-9]+")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def normalize_text(value: object) -> str:
    """Return a stable search key for loose drug-name matching."""
    if value is None:
        return ""
    return " ".join(WORD_RE.findall(str(value).lower()))


def clean_list(values: object) -> list[str]:
    if values is None:
        return []
    if isinstance(values, str):
        values = [values]
    if not isinstance(values, Iterable):
        return []

    cleaned: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value is None:
            continue
        text = str(value).strip()
        key = normalize_text(text)
        if text and key not in seen:
            cleaned.append(text)
            seen.add(key)
    return cleaned


def parse_us_date(value: object) -> str | None:
    if not value:
        return None
    text = str(value).strip()
    for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            continue
    return text


def stable_id(parts: Iterable[object]) -> str:
    raw = "|".join(str(part or "").strip() for part in parts)
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def record_search_text(record: dict[str, Any]) -> str:
    searchable: list[object] = [
        record.get("generic_name"),
        record.get("status"),
        record.get("dosage_form"),
        record.get("presentation"),
        record.get("company_name"),
        record.get("related_info"),
        record.get("package_ndc"),
    ]
    searchable.extend(record.get("brand_names", []))
    searchable.extend(record.get("rxcuis", []))
    searchable.extend(record.get("therapeutic_categories", []))
    searchable.extend(record.get("product_ndcs", []))
    return normalize_text(" ".join(str(item) for item in searchable if item))


def public_shortage_record(raw: dict[str, Any]) -> dict[str, Any]:
    openfda = raw.get("openfda") or {}
    generic_name = str(raw.get("generic_name") or "").strip()
    package_ndc = str(raw.get("package_ndc") or "").strip()
    presentation = str(raw.get("presentation") or "").strip()
    status = str(raw.get("status") or "Unknown").strip()

    record: dict[str, Any] = {
        "id": stable_id(
            [
                package_ndc,
                generic_name,
                presentation,
                status,
                raw.get("initial_posting_date"),
            ]
        ),
        "generic_name": generic_name,
        "brand_names": clean_list(openfda.get("brand_name")),
        "status": status,
        "update_type": str(raw.get("update_type") or "").strip(),
        "update_date": parse_us_date(raw.get("update_date")),
        "initial_posting_date": parse_us_date(raw.get("initial_posting_date")),
        "discontinued_date": parse_us_date(raw.get("discontinued_date")),
        "package_ndc": package_ndc,
        "package_ndcs": clean_list(openfda.get("package_ndc")),
        "product_ndcs": clean_list(openfda.get("product_ndc")),
        "rxcuis": clean_list(openfda.get("rxcui")),
        "substances": clean_list(openfda.get("substance_name")),
        "routes": clean_list(openfda.get("route")),
        "therapeutic_categories": clean_list(raw.get("therapeutic_category")),
        "dosage_form": str(raw.get("dosage_form") or "").strip(),
        "presentation": presentation,
        "company_name": str(raw.get("company_name") or "").strip(),
        "related_info": str(raw.get("related_info") or "").strip(),
        "source_url": "https://api.fda.gov/drug/shortages.json",
    }
    record["search_text"] = record_search_text(record)
    return record


def status_counts(records: Iterable[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        status = str(record.get("status") or "Unknown")
        counts[status] = counts.get(status, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))
