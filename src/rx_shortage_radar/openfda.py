from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from .normalize import public_shortage_record, status_counts, utc_now_iso

OPENFDA_SHORTAGES_URL = "https://api.fda.gov/drug/shortages.json"
DEFAULT_PAGE_LIMIT = 1000


class OpenFDAError(RuntimeError):
    """Raised when openFDA returns an unexpected response."""


def _build_url(params: dict[str, object]) -> str:
    api_key = os.getenv("OPENFDA_API_KEY")
    if api_key:
        params = {**params, "api_key": api_key}
    return f"{OPENFDA_SHORTAGES_URL}?{urllib.parse.urlencode(params)}"


def request_json(url: str, *, timeout: int = 45, attempts: int = 3) -> dict[str, Any]:
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            request = urllib.request.Request(
                url,
                headers={
                    "Accept": "application/json",
                    "User-Agent": "rx-shortage-radar/0.1 (+https://github.com/zzddddzz/rx-shortage-radar)",
                },
            )
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt == attempts:
                break
            time.sleep(1.5 * attempt)
    raise OpenFDAError(f"Could not fetch openFDA data from {url}: {last_error}") from last_error


def fetch_shortage_page(*, skip: int = 0, limit: int = DEFAULT_PAGE_LIMIT) -> dict[str, Any]:
    return request_json(_build_url({"skip": skip, "limit": limit}))


def fetch_shortages(*, max_records: int | None = None, page_limit: int = DEFAULT_PAGE_LIMIT) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    first_page = fetch_shortage_page(skip=0, limit=min(page_limit, max_records or page_limit))
    meta = first_page.get("meta") or {}
    result_info = meta.get("results") or {}
    total = int(result_info.get("total") or len(first_page.get("results") or []))
    target_total = min(total, max_records) if max_records else total

    records: list[dict[str, Any]] = list(first_page.get("results") or [])
    while len(records) < target_total:
        page = fetch_shortage_page(skip=len(records), limit=min(page_limit, target_total - len(records)))
        page_results = page.get("results") or []
        if not page_results:
            break
        records.extend(page_results)

    return meta, records[:target_total]


def build_payload(meta: dict[str, Any], raw_records: list[dict[str, Any]]) -> dict[str, Any]:
    records = [public_shortage_record(record) for record in raw_records]
    records.sort(
        key=lambda record: (
            record.get("status") != "Current",
            record.get("generic_name") or "",
            record.get("package_ndc") or "",
        )
    )
    return {
        "schema_version": 1,
        "generated_at": utc_now_iso(),
        "source": {
            "name": "openFDA Drug Shortages",
            "api_url": OPENFDA_SHORTAGES_URL,
            "docs_url": "https://open.fda.gov/apis/drug/drugshortages/",
            "terms_url": meta.get("terms"),
            "license_url": meta.get("license"),
            "last_updated": meta.get("last_updated"),
            "disclaimer": meta.get("disclaimer"),
        },
        "summary": {
            "total_records": len(records),
            "status_counts": status_counts(records),
        },
        "records": records,
    }


def write_payload(payload: dict[str, Any], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path

