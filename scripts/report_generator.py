#!/usr/bin/env python3
"""
report_generator.py — AEO Strategic Report & Deliverable Generator.

Combines audit findings, optimization results, and citation tracking into
executive summaries, before/after diff reports, and client-ready dashboards.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


class ReportGenerator:
    """Generates structured markdown and JSON reports for AEO workflows."""

    def __init__(self, project_name: str = "AEO Project"):
        self.project_name = project_name

    def generate_executive_summary(
        self,
        audit_data: Optional[Dict[str, Any]] = None,
        tracker_data: Optional[Dict[str, Any]] = None,
        query_data: Optional[Dict[str, Any]] = None,
    ) -> str:
        lines = [
            f"# AEO Executive Summary — {self.project_name}",
            "",
            f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}  ",
            "**Focus:** AI Search Citation Readiness & Performance",
            "",
            "---",
            "",
            "## 1. Executive Scorecard",
            "",
        ]

        if audit_data:
            comp = audit_data.get("composite_score", "N/A")
            grade = audit_data.get("letter_grade", "N/A")
            verdict = audit_data.get("verdict", "N/A")
            lines.extend([
                f"- **Current AEO Composite Readiness:** **{comp}/100** (Grade: {grade})",
                f"- **Industry Threshold Status:** `{verdict}`",
                "",
                "### Core Dimensions Breakdown",
                "| Dimension | Score | Status |",
                "|---|---|---|",
            ])
            dims = audit_data.get("dimensions", {})
            for d_name, d_val in dims.items():
                score = d_val.get("score", d_val.get("structure_score", 0)) if isinstance(d_val, dict) else d_val
                status = "🟢 Healthy" if score >= 70 else ("🟡 Needs Polish" if score >= 50 else "🔴 Critical Gap")
                lines.append(f"| {d_name.capitalize()} | {score}/100 | {status} |")
            lines.append("")

        if tracker_data:
            summary = tracker_data.get("summary", {})
            lines.extend([
                "## 2. LLM Citation Visibility",
                f"- **Observed Citations:** {summary.get('total_citations', 0)}",
                f"- **Active LLM Coverage:** {summary.get('llm_count', 0)} engines ({', '.join(summary.get('llms', [])) or 'None'})",
                f"- **Citation Velocity:** {summary.get('velocity', '0 citations/day')}",
                f"- **Maturity Verdict:** `{summary.get('verdict', 'INITIAL')}`",
                "",
            ])

        lines.extend([
            "## 3. Immediate Action Plan",
            "",
        ])

        if audit_data and "top_fixes" in audit_data:
            for i, (dim, fix) in enumerate(audit_data["top_fixes"], 1):
                lines.append(f"{i}. **[{dim}]** {fix}")
        else:
            lines.extend([
                "1. Audit high-traffic articles with `aeo_audit.py` to identify E-E-A-T gaps.",
                "2. Inject JSON-LD FAQPage & Article schemas into key documentation.",
                "3. Verify bot access: ensure robots.txt permits `GPTBot`, `PerplexityBot`, and `ClaudeBot`.",
            ])

        lines.extend([
            "",
            "---",
            "*Report produced by AEO Skill System.*",
        ])

        return "\n".join(lines)

    def generate_before_after_comparison(
        self,
        before_audit: Dict[str, Any],
        after_audit: Dict[str, Any],
    ) -> str:
        b_score = before_audit.get("composite_score", 0)
        a_score = after_audit.get("composite_score", 0)
        diff = a_score - b_score
        sign = "+" if diff >= 0 else ""

        lines = [
            "# AEO Content Optimization — Before vs After",
            "",
            f"**Audit Subject:** {before_audit.get('url', 'Document')}  ",
            f"**Evaluation Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d')}  ",
            "",
            f"## Overall Score Delta: **{b_score}/100** ➔ **{a_score}/100** (`{sign}{diff}` points)",
            "",
            "| Metric | Before Optimization | After Optimization | Delta |",
            "|---|---|---|---|",
            f"| **Composite Score** | {b_score}/100 | {a_score}/100 | **{sign}{diff}** |",
        ]

        b_dims = before_audit.get("dimensions", {})
        a_dims = after_audit.get("dimensions", {})
        all_keys = set(b_dims.keys()).union(set(a_dims.keys()))

        for k in sorted(all_keys):
            b_val = b_dims.get(k, {})
            a_val = a_dims.get(k, {})
            b_s = b_val.get("score", b_val.get("structure_score", 0)) if isinstance(b_val, dict) else b_val
            a_s = a_val.get("score", a_val.get("structure_score", 0)) if isinstance(a_val, dict) else a_val
            d = a_s - b_s
            s_str = f"+{d}" if d >= 0 else str(d)
            lines.append(f"| {k.capitalize()} | {b_s}/100 | {a_s}/100 | {s_str} |")

        return "\n".join(lines)


    def generate_refresh_matrix(self, pages: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        Generate a Keep / Fix / Remove / Add Refresh Matrix based on 56-day GSC baseline
        and the 3-Step Page Independence Test from Playbook V2.
        """
        sample_pages = [
            {
                "url": "/blog/what-is-aeo-guide",
                "action": "FIX",
                "gsc_56d_trend": "Clicks -18%, Impressions Flat",
                "independence_test": "PASSED (Unique core intent)",
                "rationale": "High impression base but losing clicks. Restructure H1 for labrador index, bind stats to brand, enrich image alts for OpenAI Markdown Cache.",
            },
            {
                "url": "/resources/aeo-statistics-2024",
                "action": "REMOVE (301)",
                "gsc_56d_trend": "Clicks -72%, cannibalizing /blog/what-is-aeo-guide",
                "independence_test": "FAILED (Intent overlap >60%)",
                "rationale": "Outdated 2024 figures. Migrate surviving unique data points into primary AEO guide and issue 301 redirect.",
            },
            {
                "url": "/tools/aeo-audit-checklist",
                "action": "KEEP",
                "gsc_56d_trend": "Clicks +12%, Top 3 in Google AI Overviews",
                "independence_test": "PASSED (Standalone procedural asset)",
                "rationale": "Strong citation performance. DO NOT touch URL slug or H1 title. Perform subtle date bumps and freshness checks.",
            },
            {
                "url": "/solutions/enterprise-aeo-framework",
                "action": "ADD",
                "gsc_56d_trend": "N/A (New target cluster)",
                "independence_test": "PASSED (Fills MoFU/BoFU vendor comparison gap)",
                "rationale": "Target high-value MoFU/BoFU comparison queries with downloadable benchmark datasets and Schema.org FAQPage.",
            },
        ]
        active_pages = pages if pages is not None else sample_pages

        lines = [
            f"# AEO Page Refresh & Migration Matrix — {self.project_name}",
            "",
            f"**Evaluation Horizon:** 56-Day GSC Baseline Analysis  ",
            f"**Protocol:** Keep / Fix / Remove (301) / Add Framework  ",
            f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
            "",
            "## 1. Refresh Action Matrix",
            "",
            "| Target URL | Action | 56-Day GSC Trend | Independence Test | Strategic Remediation |",
            "|---|---|---|---|---|",
        ]

        for p in active_pages:
            badge = "🟢 **KEEP**" if p["action"] == "KEEP" else (
                "🟡 **FIX**" if p["action"] == "FIX" else (
                    "🔴 **REMOVE (301)**" if "REMOVE" in p["action"] else "🔵 **ADD**"
                )
            )
            lines.append(f"| `{p['url']}` | {badge} | {p['gsc_56d_trend']} | {p['independence_test']} | {p['rationale']} |")

        lines.extend([
            "",
            "## 2. Cannibalization & URL Safety Guardrails",
            "- **Rule 1 (URL Immutability):** Never alter the URL slug or primary H1 title on performing pages (KEEP). Changing slugs resets LLM retrieval history and cache trust.",
            "- **Rule 2 (3-Step Independence Test):** If two pages share >40% identical cited prompts in Perplexity/Google AI Overviews, merge into the stronger URL with 301 redirect.",
            "- **Rule 3 (Stale-While-Revalidate):** OpenAI Markdown Cache may hold pages for up to 30 days. Send fresh HTTP `Last-Modified` headers and submit IndexNow upon deploying updates.",
            "- **Rule 4 (Dark Funnel Preservation):** When fixing pages, preserve existing text fragments and anchors to maintain AI Overview deep links.",
        ])

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="AEO Report Generator")
    parser.add_argument("--project", default="Client Website", help="Project name")
    parser.add_argument("--audit-json", help="Path to JSON file from aeo_audit.py")
    parser.add_argument("--refresh-matrix", action="store_true", help="Generate Keep/Fix/Remove/Add refresh matrix")
    parser.add_argument("--output", help="Save output to file (default: print stdout)")
    args = parser.parse_args()

    audit_data = None
    if args.audit_json:
        p = Path(args.audit_json)
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                audit_data = json.load(f)

    gen = ReportGenerator(project_name=args.project)
    
    if args.refresh_matrix:
        report_md = gen.generate_refresh_matrix()
    else:
        report_md = gen.generate_executive_summary(audit_data=audit_data)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report_md)
        print(f"✅ Report saved to {args.output}")
    else:
        print(report_md)


if __name__ == "__main__":
    main()
