from __future__ import annotations

import argparse
import json
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from typing import Any

from .openfda import build_payload, fetch_shortages, write_payload
from .normalize import normalize_text


def load_payload(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def cmd_refresh(args: argparse.Namespace) -> int:
    meta, raw_records = fetch_shortages(max_records=args.max_records, page_limit=args.page_limit)
    payload = build_payload(meta, raw_records)
    output_path = write_payload(payload, args.output)
    counts = ", ".join(f"{status}: {count}" for status, count in payload["summary"]["status_counts"].items())
    print(f"Wrote {payload['summary']['total_records']} records to {output_path}")
    print(f"Status counts: {counts}")
    print(f"openFDA last_updated: {payload['source'].get('last_updated')}")
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    payload = load_payload(args.data)
    query = normalize_text(args.query)
    query_terms = query.split()
    records = payload.get("records") or []
    matches = []
    for record in records:
        if args.status and record.get("status") != args.status:
            continue
        search_text = record.get("search_text") or ""
        if all(term in search_text for term in query_terms):
            matches.append(record)
    for record in matches[: args.limit]:
        brands = ", ".join(record.get("brand_names") or []) or "no brand listed"
        print(
            f"{record.get('status', 'Unknown'):>18}  "
            f"{record.get('generic_name') or '(unnamed)'} | {brands} | "
            f"NDC {record.get('package_ndc') or 'unknown'} | updated {record.get('update_date') or 'unknown'}"
        )
    if len(matches) > args.limit:
        print(f"... {len(matches) - args.limit} more matches")
    print(f"{len(matches)} match(es)")
    return 0


def cmd_serve(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    handler_class = lambda *handler_args, **handler_kwargs: SimpleHTTPRequestHandler(  # noqa: E731
        *handler_args,
        directory=str(root),
        **handler_kwargs,
    )
    server = ThreadingHTTPServer((args.host, args.port), handler_class)
    print(f"Serving {root} at http://{args.host}:{args.port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped")
    finally:
        server.server_close()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rx-shortage-radar",
        description="Fetch, search, and publish public FDA drug-shortage data.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    refresh = subparsers.add_parser("refresh", help="Fetch openFDA shortages and write dashboard JSON.")
    refresh.add_argument("--output", default="site/data/shortages.json", help="Output JSON path.")
    refresh.add_argument("--max-records", type=int, default=None, help="Limit records for quick demos/tests.")
    refresh.add_argument("--page-limit", type=int, default=1000, help="openFDA page size.")
    refresh.set_defaults(func=cmd_refresh)

    search = subparsers.add_parser("search", help="Search generated shortage data.")
    search.add_argument("query", help="Medication, RxCUI, NDC, company, or category search text.")
    search.add_argument("--data", default="site/data/shortages.json", help="Generated JSON data path.")
    search.add_argument("--status", default=None, help="Optional exact status filter.")
    search.add_argument("--limit", type=int, default=20, help="Maximum rows to print.")
    search.set_defaults(func=cmd_search)

    serve = subparsers.add_parser("serve", help="Serve the static dashboard locally.")
    serve.add_argument("--root", default="site", help="Static site root.")
    serve.add_argument("--host", default="127.0.0.1", help="Bind host.")
    serve.add_argument("--port", type=int, default=8765, help="Bind port.")
    serve.set_defaults(func=cmd_serve)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))

