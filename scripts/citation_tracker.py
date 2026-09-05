#!/usr/bin/env python3
"""
citation_tracker.py — Local-first citation & brand visibility ledger for AEO/GEO.

Tracks visibility across 4 critical states:
  - both:    Cited (URL) AND Brand mentioned in text (Ideal state)
  - ghost:   Cited (URL) ONLY, Brand omitted from text (Ghost Citation)
  - mention: Brand mentioned, but no URL citation
  - neither: Query tested, neither brand nor URL appeared

Calculates:
  - Total citations & multi-LLM coverage
  - Ghost Citation Ratio (lost brand equity)
  - Citation velocity and cross-engine overlap

Stores entries locally in ~/.aeo-data/citations.json. Stdlib only.
"""

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, List, Optional


SUPPORTED_LLMS = ["chatgpt", "perplexity", "claude", "gemini", "mistral", "copilot", "brave", "you", "other"]
SUPPORTED_STATUSES = ["both", "ghost", "mention", "neither"]


def _data_dir() -> Path:
    d = Path.home() / ".aeo-data"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _ledger_path() -> Path:
    return _data_dir() / "citations.json"


def _load_ledger() -> dict:
    path = _ledger_path()
    if not path.exists():
        return {"schema_version": 2, "citations": []}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.stderr.write(f"[citation_tracker] WARN: ledger file corrupted ({e}); starting fresh\n")
        return {"schema_version": 2, "citations": []}


def _save_ledger(ledger: dict) -> Path:
    path = _ledger_path()
    path.write_text(json.dumps(ledger, indent=2), encoding="utf-8")
    return path


def add_citation(
    url: str,
    llm: str,
    query: str,
    status: str = "both",
    brand: str = "",
    date: str | None = None,
    notes: str = "",
    position: str = ""
) -> dict:
    """Add a citation entry with visibility status (both/ghost/mention/neither)."""
    if llm.lower() not in SUPPORTED_LLMS:
        sys.stderr.write(f"[citation_tracker] WARN: unknown LLM '{llm}' (allowed: {SUPPORTED_LLMS})\n")

    if status.lower() not in SUPPORTED_STATUSES:
        status = "both"

    entry = {
        "id": _make_id(),
        "url": url,
        "llm": llm.lower(),
        "query": query,
        "status": status.lower(),
        "brand": brand,
        "date": date or datetime.now(timezone.utc).date().isoformat(),
        "logged_at": datetime.now(timezone.utc).isoformat(),
        "notes": notes,
        "position": position,
    }
    ledger = _load_ledger()
    ledger["citations"].append(entry)
    _save_ledger(ledger)
    return entry


def _make_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S-%f")[:21]


def list_citations(
    url: str | None = None,
    llm: str | None = None,
    status: str | None = None,
    since: str | None = None
) -> list:
    """List citations matching filters."""
    ledger = _load_ledger()
    cits = ledger["citations"]
    if url:
        cits = [c for c in cits if c["url"] == url]
    if llm:
        cits = [c for c in cits if c["llm"] == llm.lower()]
    if status:
        cits = [c for c in cits if c.get("status", "both") == status.lower()]
    if since:
        cits = [c for c in cits if c["date"] >= since]
    return cits


def report(url: str | None = None) -> dict:
    """Generate aggregate report with 4-status matrix and Ghost Citation Ratio."""
    cits = list_citations(url=url) if url else _load_ledger()["citations"]
    if not cits:
        return {
            "url": url,
            "total_records": 0,
            "total_citations": 0,
            "llms_covered": [],
            "verdict": "NO_DATA",
        }

    by_llm = {}
    by_query = {}
    by_date = {}
    by_status = {"both": 0, "ghost": 0, "mention": 0, "neither": 0}

    for c in cits:
        st = c.get("status", "both")
        by_status[st] = by_status.get(st, 0) + 1

        if st in ("both", "ghost"):
            by_llm[c["llm"]] = by_llm.get(c["llm"], 0) + 1
            by_query[c["query"]] = by_query.get(c["query"], 0) + 1
            by_date[c["date"]] = by_date.get(c["date"], 0) + 1

    total_actual_citations = by_status["both"] + by_status["ghost"]
    ghost_ratio = round((by_status["ghost"] / max(total_actual_citations, 1)) * 100, 1)

    top_queries = sorted(by_query.items(), key=lambda kv: -kv[1])[:10]
    dates = sorted(by_date.keys())

    velocity = 0.0
    if len(dates) >= 2:
        first = datetime.fromisoformat(dates[0])
        last = datetime.fromisoformat(dates[-1])
        days = max((last - first).days, 1)
        velocity = round(total_actual_citations / days, 2)

    verdict = "STRONG" if len(by_llm) >= 3 and total_actual_citations >= 10 else \
              "EMERGING" if total_actual_citations >= 3 else \
              "EARLY"

    return {
        "url": url,
        "total_records_tested": len(cits),
        "total_url_citations": total_actual_citations,
        "status_breakdown": by_status,
        "ghost_citation_ratio_pct": ghost_ratio,
        "llms_covered": sorted(by_llm.keys()),
        "llm_coverage_count": len(by_llm),
        "citations_per_llm": by_llm,
        "top_queries": top_queries,
        "first_citation_date": dates[0] if dates else None,
        "last_citation_date": dates[-1] if dates else None,
        "velocity_per_day": velocity,
        "verdict": verdict,
        "interpretation": {
            "STRONG":   "Cited by 3+ LLMs with steady volume — content has established citation moat",
            "EMERGING": "Cited multiple times but cross-engine overlap is still low — expand UGC and entity signals",
            "EARLY":    "Few or no citations — verify crawler access, enrich 200-char lede, and update within 30 days",
            "NO_DATA":  "No records logged yet",
        }.get(verdict, ""),
    }


def export_csv(output_path: str) -> int:
    """Export the full citation ledger as CSV."""
    ledger = _load_ledger()
    cits = ledger["citations"]
    fieldnames = ["id", "url", "llm", "query", "status", "brand", "date", "logged_at", "notes", "position"]
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for c in cits:
            w.writerow({k: c.get(k, "") for k in fieldnames})
    return len(cits)


def render_human(action: str, data: Any) -> str:
    """Render results as human-readable text."""
    if action == "add":
        status_icon = {"both": "🟢 Both (Cited+Named)", "ghost": "👻 Ghost (Cited only)", "mention": "💬 Mention only", "neither": "⚪ Neither"}.get(data.get("status", "both"), "")
        return (f"✅ Logged citation check:\n"
                f"   URL:    {data['url']}\n"
                f"   LLM:    {data['llm']}\n"
                f"   Query:  {data['query']}\n"
                f"   Status: {status_icon}\n"
                f"   Date:   {data['date']}\n"
                f"   ID:     {data['id']}")

    if action == "list":
        if not data:
            return "(no citations match the filters)"
        lines = [f"Found {len(data)} record(s):"]
        for c in data:
            st = c.get("status", "both")
            icon = "🟢" if st == "both" else ("👻" if st == "ghost" else ("💬" if st == "mention" else "⚪"))
            lines.append(f"  [{c['date']}] {icon} {c['llm']:10s} [{st:7s}] ← {c['url']}")
            lines.append(f"             query: {c['query']}")
            if c.get("notes"):
                lines.append(f"             notes: {c['notes']}")
        return "\n".join(lines)

    if action == "report":
        if data.get("total_records_tested", 0) == 0:
            return f"📊 Report ({data.get('url') or 'all'}):\n   No records logged yet."

        sb = data["status_breakdown"]
        lines = [
            f"📊 AEO & GEO Visibility Report — {data.get('url') or 'ALL URLs'}",
            "",
            f"   Total Queries Tested:    {data['total_records_tested']}",
            f"   Total URL Citations:     {data['total_url_citations']}",
            f"   LLM Coverage:            {data['llm_coverage_count']} ({', '.join(data['llms_covered']) or 'None'})",
            f"   Velocity:                {data['velocity_per_day']} citations/day",
            f"   Verdict:                 {data['verdict']}",
            "",
            "   4-State Visibility Breakdown:",
            f"     🟢 Both (Cited + Named):  {sb.get('both', 0)}",
            f"     👻 Ghost (Cited Only):    {sb.get('ghost', 0)}",
            f"     💬 Mentioned Only:        {sb.get('mention', 0)}",
            f"     ⚪ Neither:               {sb.get('neither', 0)}",
            f"   Ghost Citation Ratio:     {data['ghost_citation_ratio_pct']}%",
        ]

        if data['ghost_citation_ratio_pct'] > 30:
            lines.append("   ⚠️ WARNING: High Ghost Citation Ratio. Bind brand names directly to statistics in sentences.")

        lines.extend([
            "",
            "   Citations per LLM:",
        ])
        for llm, n in sorted(data["citations_per_llm"].items(), key=lambda kv: -kv[1]):
            lines.append(f"     {llm:12s} {n}")

        if data["top_queries"]:
            lines.append("\n   Top cited queries:")
            for q, n in data["top_queries"]:
                lines.append(f"     ({n:2d}) {q}")

        return "\n".join(lines)

    if action == "export":
        return f"✅ Exported {data['count']} records to {data['output']}"

    return str(data)


def main():
    parser = argparse.ArgumentParser(description="AEO & GEO Citation & Brand Visibility Tracker")
    subparsers = parser.add_subparsers(dest="action")

    # Command: add
    add_p = subparsers.add_parser("add", help="Log observed citation/mention")
    add_p.add_argument("--url", required=True, help="URL to track")
    add_p.add_argument("--llm", required=True, choices=SUPPORTED_LLMS, help="LLM where tested")
    add_p.add_argument("--query", required=True, help="Exact user prompt")
    add_p.add_argument("--status", choices=SUPPORTED_STATUSES, default="both", help="Visibility state: both, ghost, mention, neither")
    add_p.add_argument("--brand", default="", help="Brand name checked")
    add_p.add_argument("--date", help="Date observed (YYYY-MM-DD)")
    add_p.add_argument("--position", help="Citation position (e.g. 'source pill #1', 'footnote 3')")
    add_p.add_argument("--notes", default="", help="Qualitative observation notes")

    # Command: list
    list_p = subparsers.add_parser("list", help="List recorded citations")
    list_p.add_argument("--url", help="Filter by URL")
    list_p.add_argument("--llm", help="Filter by LLM")
    list_p.add_argument("--status", choices=SUPPORTED_STATUSES, help="Filter by status")
    list_p.add_argument("--since", help="Filter since date (YYYY-MM-DD)")

    # Command: report
    rep_p = subparsers.add_parser("report", help="Generate visibility & Ghost Citation report")
    rep_p.add_argument("--url", help="Filter report by URL")
    rep_p.add_argument("--output", choices=["human", "json"], default="human", help="Output format")

    # Command: export
    exp_p = subparsers.add_parser("export", help="Export ledger to CSV")
    exp_p.add_argument("--output", default="citations.csv", help="Output CSV path")

    # Command: sample
    subparsers.add_parser("sample", help="Run self-contained demonstration")

    args = parser.parse_args()

    if args.action == "add":
        entry = add_citation(
            url=args.url,
            llm=args.llm,
            query=args.query,
            status=args.status,
            brand=args.brand,
            date=args.date,
            notes=args.notes,
            position=args.position or ""
        )
        print(render_human("add", entry))

    elif args.action == "list":
        res = list_citations(url=args.url, llm=args.llm, status=args.status, since=args.since)
        print(render_human("list", res))

    elif args.action == "report":
        res = report(url=args.url)
        if args.output == "json":
            print(json.dumps(res, indent=2, ensure_ascii=False))
        else:
            print(render_human("report", res))

    elif args.action == "export":
        cnt = export_csv(args.output)
        print(render_human("export", {"count": cnt, "output": args.output}))

    elif args.action == "sample":
        demo_url = "https://example.com/blog/aeo-guide"
        print("=== Demo: Logging 4-State Visibility Checks ===")
        add_citation(demo_url, "perplexity", "what is answer engine optimization", status="both", brand="Acme")
        add_citation(demo_url, "chatgpt", "how to optimize for search in 2026", status="ghost", brand="Acme", notes="Cited as link #2 but Acme not named")
        add_citation(demo_url, "claude", "enterprise search benchmarks", status="both", brand="Acme")
        add_citation(demo_url, "gemini", "best AEO practices", status="neither", brand="Acme")

        rep = report(demo_url)
        print("\n" + render_human("report", rep))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
