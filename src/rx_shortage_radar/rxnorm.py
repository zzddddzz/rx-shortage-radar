from __future__ import annotations

import json
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any

RXNORM_APPROXIMATE_URL = "https://rxnav.nlm.nih.gov/REST/approximateTerm.json"


@dataclass(frozen=True)
class RxNormCandidate:
    rxcui: str
    name: str
    score: float
    rank: int
    source: str


def _request_json(url: str, *, timeout: int = 30) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "rx-shortage-radar/0.1 (+https://github.com/zzddddzz/rx-shortage-radar)",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def parse_approximate_candidates(payload: dict[str, Any]) -> list[RxNormCandidate]:
    candidates = payload.get("approximateGroup", {}).get("candidate") or []
    results: list[RxNormCandidate] = []
    seen: set[str] = set()
    for candidate in candidates:
        rxcui = str(candidate.get("rxcui") or "").strip()
        if not rxcui or rxcui in seen:
            continue
        seen.add(rxcui)
        name = str(candidate.get("name") or "").strip()
        source = str(candidate.get("source") or "").strip()
        try:
            score = float(candidate.get("score") or 0)
        except ValueError:
            score = 0.0
        try:
            rank = int(candidate.get("rank") or 0)
        except ValueError:
            rank = 0
        results.append(RxNormCandidate(rxcui=rxcui, name=name, score=score, rank=rank, source=source))
    results.sort(key=lambda item: (item.rank or 9999, -item.score, item.name or item.rxcui))
    return results


def approximate_term(term: str, *, max_entries: int = 8) -> list[RxNormCandidate]:
    params = urllib.parse.urlencode({"term": term, "maxEntries": max_entries})
    payload = _request_json(f"{RXNORM_APPROXIMATE_URL}?{params}")
    return parse_approximate_candidates(payload)

