#!/usr/bin/env python3
"""
query_researcher.py — Query Research & Targeting Module for AEO.

Researches query opportunities, categorizes query intent (factual, comparison,
statistical, procedural), and generates prioritized prompt targets that
trigger citations in AI answer engines (ChatGPT, Perplexity, Claude, Gemini).
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


class QueryResearcher:
    """
    Analyzes topics for Answer Engine citation opportunities.
    """

    INTENT_TEMPLATES = {
        "definition_overview": {
            "funnel": "ToFU (Problem Discovery)",
            "templates": [
                ("what is {topic}", "High", "Triggers definition snippet + authoritative glossary citation"),
                ("how does {topic} work", "High", "Triggers technical process description"),
                ("{topic} architecture explained", "Medium", "Technical deep-dive query"),
            ],
        },
        "comparative_evaluation": {
            "funnel": "MoFU (Solution Comparison)",
            "templates": [
                ("{topic} vs {alt}", "Very High", "LLMs consistently cite comparison matrices and tradeoff tables"),
                ("top alternatives to {topic}", "High", "Triggers listicle citation and feature matrices"),
                ("best {topic} tools for {audience}", "High", "Recommendation roundups cite benchmark sources"),
            ],
        },
        "data_and_statistics": {
            "funnel": "MoFU (Benchmark Verification)",
            "templates": [
                ("{topic} statistics 2026", "Critical", "LLMs MUST cite sources for hard statistical figures"),
                ("{topic} market size and growth rate", "Critical", "Financial / industry report citation guaranteed"),
                ("{topic} benchmarks and performance", "Very High", "Quantitative benchmarks demand primary source citations"),
            ],
        },
        "procedural_howto": {
            "funnel": "MoFU (Technical Evaluation)",
            "templates": [
                ("how to implement {topic} step by step", "High", "Numbered procedure blocks are directly extracted"),
                ("{topic} best practices checklist", "High", "Checklist formats are favoured by Perplexity & Gemini"),
                ("how to troubleshoot {topic} issues", "Medium", "Technical solutions and forum/doc citations"),
            ],
        },
        "purchase_decision": {
            "funnel": "BoFU (Vendor Selection & ROI)",
            "templates": [
                ("{topic} pricing models and total cost of ownership", "Very High", "Directly extracted for enterprise procurement queries"),
                ("is {topic} worth it: implementation ROI case studies", "High", "Synthesizes customer evidence and verified case numbers"),
                ("migrating from {alt} to {topic} checklist", "Very High", "Step-by-step migration guide triggering high-intent citations"),
            ],
        },
    }

    def __init__(self, region: str = "US"):
        self.region = region

    def research(
        self,
        topic: str,
        audience: str = "enterprises",
        competitors: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        competitors = competitors or []
        queries: List[Dict[str, Any]] = []

        # Default alternate if none provided
        alt = f"traditional alternatives"

        for intent_cat, data in self.INTENT_TEMPLATES.items():
            funnel = data["funnel"]
            for tmpl, potential, rationale in data["templates"]:
                q_text = tmpl.format(topic=topic, alt=alt, audience=audience)
                queries.append({
                    "query": q_text,
                    "category": intent_cat,
                    "funnel_stage": funnel,
                    "citation_potential": potential,
                    "rationale": rationale,
                    "recommended_format": self._recommended_format(intent_cat),
                })

        # Calculate score
        high_critical_count = sum(1 for q in queries if q["citation_potential"] in ["Critical", "Very High", "High"])
        total_queries = len(queries)
        potential_score = int((high_critical_count / total_queries) * 100)

        competitor_analysis = []
        for comp in competitors:
            comp_domain = comp.replace("https://", "").replace("http://", "").split("/")[0]
            competitor_analysis.append({
                "url": comp,
                "domain": comp_domain,
                "likely_citable_assets": [
                    f"https://{comp_domain}/research/benchmark-report",
                    f"https://{comp_domain}/compare/{topic}-alternatives",
                    f"https://{comp_domain}/docs/how-to-guide",
                ],
                "recommended_counter_strategy": f"Publish original quantitative data or primary research exceeding {comp_domain}'s depth.",
            })

        return {
            "topic": topic,
            "region": self.region,
            "researched_at": datetime.now(timezone.utc).isoformat(),
            "overall_citation_potential_score": potential_score,
            "target_queries": queries,
            "competitor_benchmarks": competitor_analysis,
            "content_gap_recommendations": [
                f"Create a dedicated, citable statistics page: '{topic.title()} Key Statistics (2026 Update)' with downloadable data.",
                f"Publish a comparison table with verifiable metrics between {topic} and common alternatives.",
                f"Implement JSON-LD FAQPage and Article schema on all top-level guides for {topic}.",
                "Set up GA4 Text Fragment tracking (`#:~:text=`) to recover 22.4% Dark Funnel AI traffic mistakenly classified as Direct.",
            ],
            "dark_funnel_guidance": {
                "ga4_custom_dimension": "Track `location.hash` containing `#:~:text=` to isolate Google AI Overview clicks",
                "referrer_regex": r"android-app:\/\/com\.google\.android\.googlequicksearchbox|chatgpt\.com|perplexity\.ai",
                "mitigation": "Ensure canonical URLs and branded anchor texts are placed near text fragments to secure brand attribution"
            }
        }

    def _recommended_format(self, intent: str) -> str:
        formats = {
            "definition_overview": "30-50 word bold definition sentence immediately following H2",
            "comparative_evaluation": "Markdown comparison table with columns: Feature, Metric, Source, Verification",
            "data_and_statistics": "Numbered list with specific years, dollar figures, and bracketed citations [1]",
            "procedural_howto": "Ordered list with bold action verbs at the start of each step",
            "purchase_decision": "Transparent pricing breakdown table + ROI metric summary block",
        }
        return formats.get(intent, "Structured markdown with clear headings")

    def format_markdown(self, report: Dict[str, Any]) -> str:
        lines = [
            f"# AEO Query Research Report — {report['topic'].title()}",
            "",
            f"**Target Topic:** {report['topic']}  ",
            f"**Region:** {report['region']}  ",
            f"**Researched:** {report['researched_at']}  ",
            f"**Citation Potential:** {report['overall_citation_potential_score']}/100",
            "",
            "## High-Value Citation Targets (Funnel-Mapped)",
            "",
            "| Funnel Stage | Query | Intent Category | Citation Potential | Optimal Extraction Format |",
            "|---|---|---|---|---|",
        ]

        for q in report["target_queries"]:
            lines.append(f"| {q.get('funnel_stage', 'ToFU')} | `{q['query']}` | {q['category']} | **{q['citation_potential']}** | {q['recommended_format']} |")

        lines.extend([
            "",
            "## Content Gaps & Tactical Recommendations",
            "",
        ])
        for i, rec in enumerate(report["content_gap_recommendations"], 1):
            lines.append(f"{i}. {rec}")

        df = report.get("dark_funnel_guidance")
        if df:
            lines.extend([
                "",
                "## Dark Funnel Attribution Guide (Google AI Overviews & ChatGPT)",
                f"- **GA4 Text Fragment Isolation:** {df['ga4_custom_dimension']}",
                f"- **Referrer Pattern:** `{df['referrer_regex']}`",
                f"- **Mitigation Strategy:** {df['mitigation']}",
            ])

        if report["competitor_benchmarks"]:
            lines.extend([
                "",
                "## Competitor Analysis",
                "",
            ])
            for comp in report["competitor_benchmarks"]:
                lines.append(f"### Competitor: `{comp['domain']}`")
                lines.append(f"- **Strategy:** {comp['recommended_counter_strategy']}")
                lines.append("- **Typical Citable URLs:**")
                for u in comp["likely_citable_assets"]:
                    lines.append(f"  - `{u}`")

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="AEO Query Researcher & Topic Targeting")
    parser.add_argument("--topic", required=True, help="Topic or keyword phrase to analyze")
    parser.add_argument("--region", default="US", help="Target geographic region (default: US)")
    parser.add_argument("--audience", default="enterprises", help="Target audience persona")
    parser.add_argument("--competitors", help="Comma-separated competitor URLs")
    parser.add_argument("--output", choices=["markdown", "json"], default="markdown", help="Output format")
    args = parser.parse_args()

    competitor_list = [c.strip() for c in args.competitors.split(",") if c.strip()] if args.competitors else []
    researcher = QueryResearcher(region=args.region)
    data = researcher.research(topic=args.topic, audience=args.audience, competitors=competitor_list)

    if args.output == "json":
        print(json.dumps(data, indent=2))
    else:
        print(researcher.format_markdown(data))


if __name__ == "__main__":
    main()
