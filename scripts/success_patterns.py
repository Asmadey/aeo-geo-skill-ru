#!/usr/bin/env python3
"""
success_patterns.py — Adaptive Learning & Proven Citation Patterns Library.

Tracks successful optimizations, logs which content patterns get cited by LLMs,
and maintains a local library of industry-proven citation formats.
Stores data in ~/.aeo-data/success_patterns.json.
"""

import argparse
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("aeo.success_patterns")

DEFAULT_PATTERNS_DB = Path.home() / ".aeo-data" / "success_patterns.json"

BUILTIN_PROVEN_PATTERNS = {
    "definition_block": {
        "description": "Bold single-sentence answer directly under H2 followed by quantitative proof",
        "citation_lift": "+40% in Perplexity and Gemini",
        "recommended_for": ["glossary", "concept guides", "industry overviews"],
        "example": "### What is AEO?\n**Answer Engine Optimization (AEO) is the process of structuring content to be cited by LLMs.** In 2026, 45% of discovery queries originate in AI engines [1].",
    },
    "comparison_table": {
        "description": "Side-by-side comparison table with clear column criteria and explicit trade-offs",
        "citation_lift": "+55% in ChatGPT and Claude",
        "recommended_for": ["tool comparisons", "technology alternatives", "pricing evaluations"],
        "example": "| Feature | Tool A | Tool B | Source |\n|---|---|---|---|\n| Latency | 45ms | 120ms | [2] |",
    },
    "numbered_methodology": {
        "description": "5-7 sequential steps with bold action imperative verbs and timing/tool requirements",
        "citation_lift": "+35% in Perplexity and Claude",
        "recommended_for": ["how-to guides", "implementation runbooks", "standard operating procedures"],
        "example": "1. **Inspect robots.txt** for AI crawler user-agents (5 mins).\n2. **Run schema validation** via JSON-LD linter.",
    },
    "attributed_statistic": {
        "description": "Hard number or percentage paired with year, sample size, and bracketed primary citation",
        "citation_lift": "+65% across all LLMs",
        "recommended_for": ["all industry content", "benchmarks", "case studies"],
        "example": "According to the 2026 Enterprise Search Survey (n=1,200), 62% of executives consult Perplexity weekly [3].",
    },
}


class SuccessPatternManager:
    """Manages adaptive learning and local citation patterns database."""

    def __init__(self, db_path: Path = DEFAULT_PATTERNS_DB):
        self.db_path = db_path
        self.data = self._load_data()

    def _load_data(self) -> Dict[str, Any]:
        if not self.db_path.exists():
            return {
                "version": "1.0",
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "total_recorded_successes": 0,
                "custom_patterns": {},
                "optimization_history": [],
            }
        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load patterns DB: {e}")
            return {"version": "1.0", "custom_patterns": {}, "optimization_history": []}

    def _save_data(self):
        try:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self.data["last_updated"] = datetime.now(timezone.utc).isoformat()
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save patterns DB: {e}")

    def record_success(
        self,
        pattern_name: str,
        url: str,
        llm: str,
        query: str,
        notes: str = "",
    ):
        record = {
            "id": f"rec_{int(datetime.now(timezone.utc).timestamp())}",
            "pattern_name": pattern_name,
            "url": url,
            "llm": llm,
            "query": query,
            "notes": notes,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
        }
        self.data.setdefault("optimization_history", []).append(record)
        self.data["total_recorded_successes"] = len(self.data["optimization_history"])

        # Update pattern citation count
        patterns = self.data.setdefault("custom_patterns", {})
        if pattern_name not in patterns:
            patterns[pattern_name] = {"total_citations": 0, "llms": []}
        patterns[pattern_name]["total_citations"] += 1
        if llm not in patterns[pattern_name]["llms"]:
            patterns[pattern_name]["llms"].append(llm)

        self._save_data()
        return record

    def get_stats(self) -> Dict[str, Any]:
        return {
            "builtin_patterns_count": len(BUILTIN_PROVEN_PATTERNS),
            "custom_patterns_count": len(self.data.get("custom_patterns", {})),
            "total_recorded_successes": len(self.data.get("optimization_history", [])),
            "db_path": str(self.db_path),
        }


def main():
    parser = argparse.ArgumentParser(description="AEO Success Patterns & Adaptive Learning Manager")
    parser.add_argument("--list", action="store_true", help="List proven AEO patterns")
    parser.add_argument("--stats", action="store_true", help="Show learning database statistics")
    parser.add_argument("--record", action="store_true", help="Log a successful citation pattern")
    parser.add_argument("--pattern", default="attributed_statistic", help="Pattern name")
    parser.add_argument("--url", help="URL that got cited")
    parser.add_argument("--llm", default="perplexity", help="LLM that cited the pattern")
    parser.add_argument("--query", default="", help="Query triggering citation")
    parser.add_argument("--notes", default="", help="Observations")
    args = parser.parse_args()

    manager = SuccessPatternManager()

    if args.list:
        print("=== Proven AEO Content Patterns ===")
        for name, p in BUILTIN_PROVEN_PATTERNS.items():
            print(f"\n📦 [{name}]")
            print(f"   Impact: {p['citation_lift']}")
            print(f"   Recommended for: {', '.join(p['recommended_for'])}")
            print(f"   Description: {p['description']}")
            print(f"   Example snippet:\n   {p['example']}")
        return

    if args.record:
        if not args.url:
            print("Error: --url is required when recording success.")
            sys.exit(1)
        rec = manager.record_success(
            pattern_name=args.pattern,
            url=args.url,
            llm=args.llm,
            query=args.query,
            notes=args.notes,
        )
        print(f"✅ Recorded successful pattern citation! (ID: {rec['id']})")
        return

    # Default: stats
    stats = manager.get_stats()
    print("=== AEO Adaptive Pattern Library Stats ===")
    print(f"Built-in proven patterns: {stats['builtin_patterns_count']}")
    print(f"Custom patterns logged:   {stats['custom_patterns_count']}")
    print(f"Total successes recorded: {stats['total_recorded_successes']}")
    print(f"Storage path:             {stats['db_path']}")


if __name__ == "__main__":
    main()
