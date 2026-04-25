from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Iterable

CSV_COLUMNS = [
    "generic_name",
    "status",
    "package_ndc",
    "update_date",
    "company_name",
    "rxcuis",
    "brand_names",
    "product_ndcs",
    "therapeutic_categories",
    "dosage_form",
    "source_url",
]


def _cell(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return "; ".join(str(item) for item in value if item is not None)
    return str(value)


def csv_rows(records: Iterable[dict[str, Any]], *, status: str | None = None) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for record in records:
        if status and record.get("status") != status:
            continue
        rows.append({column: _cell(record.get(column)) for column in CSV_COLUMNS})
    return rows


def write_csv(payload: dict[str, Any], output_path: str | Path, *, status: str | None = None) -> tuple[Path, int]:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = csv_rows(payload.get("records") or [], status=status)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    return path, len(rows)

