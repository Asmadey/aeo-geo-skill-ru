#!/usr/bin/env python3
"""
aeo_audit.py — Answer Engine Optimization & Generative Engine Optimization Audit Tool.

Audits content for:
- E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) signals
- ChatGPT Instant 200-character grounding budget (post-H1 lede)
- Title self-containment & informativeness (for OpenAI labrador index)
- Image alt-text & OpenAI Markdown Cache survivability (data preservation when JSON-LD is stripped)
- Passage self-containment (zero dependent cross-references)
- Freshness / Recency (<30 day update frequency)
- Ghost Citation vulnerability (unbound statistics)
- Technical AI accessibility (size <4MB, llms.txt signals)

Stdlib only. No external deps. URL mode uses urllib.
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


INDUSTRIES = {
    "saas":       {"min_composite": 70, "critical": ["author_bio", "case_study_metrics"]},
    "healthcare": {"min_composite": 85, "critical": ["medical_reviewer", "peer_review_citations", "fda_disclosure"]},
    "finance":    {"min_composite": 85, "critical": ["credentials_cfa_cpa", "investment_disclaimer", "dated_examples"]},
    "legal":      {"min_composite": 85, "critical": ["jurisdiction", "attorney_bio", "legal_disclaimer"]},
    "ecommerce":  {"min_composite": 65, "critical": ["product_reviews", "return_policy", "schema_product"]},
    "b2b":        {"min_composite": 70, "critical": ["analyst_quotes", "customer_logos", "roi_data"]},
    "media":      {"min_composite": 70, "critical": ["editorial_policy", "fact_check_link", "original_reporting"]},
    "education":  {"min_composite": 75, "critical": ["instructor_bio", "learning_outcomes"]},
}

# ─────────────────────────────────────────────────────────────────────────
# Signal extraction patterns
# ─────────────────────────────────────────────────────────────────────────

EXPERIENCE_PATTERNS = [
    (r"\b(we|our|i|my)\s+(ran|tested|tried|built|launched|measured|implemented)\b", "first_person_evidence"),
    (r"\bin\s+(20\d{2})\b", "dated_example"),
    (r"\b(case\s+study|customer\s+story|results?:?)\b", "case_study_marker"),
    (r"\b(\$|usd|eur|€|£)\s*\d+[\d,.]*\b", "monetary_evidence"),
    (r"\b\d+%\s+(increase|decrease|growth|reduction|lift|drop)\b", "metric_evidence"),
]

EXPERTISE_PATTERNS = [
    (r"\b(ph\.?d|m\.?d|cfa|cpa|mba|esq|jd)\b", "credential_marker"),
    (r"\b(author|written\s+by|reviewed\s+by|by:?)\s+([A-Z][a-z]+\s+[A-Z][a-z]+)", "author_bio"),
    (r"\[\d+\]", "numbered_citation"),
    (r"\b(doi:\s*10\.\d+|pubmed|arxiv|ieee|iso\s+\d+)\b", "peer_reviewed_source"),
    (r"\bsource:?\s*https?://", "source_link"),
]

AUTHORITY_PATTERNS = [
    (r"https?://[^\s\)\]]+", "external_link"),
    (r'"@type"\s*:\s*"[A-Z][a-zA-Z]+"', "schema_org_jsonld"),
    (r"<script[^>]*application/ld\+json", "schema_script"),
    (r"\bschema\.org/[A-Z][a-zA-Z]+\b", "schema_inline"),
    (r"\bllms(?:\.txt|-full\.txt)\b", "llms_txt_reference"),
]

TRUST_PATTERNS = [
    (r"\bhttps://", "https"),
    (r"\b(contact|email|reach\s+us|get\s+in\s+touch)\b", "contact_marker"),
    (r"\b(corrections?|updated|edited|revised)\s+(on|policy|process)\b", "corrections_policy"),
    (r"\bdisclos(ure|ed?)\b", "disclosure"),
    (r"\b(privacy\s+policy|terms\s+of\s+service|gdpr|ccpa)\b", "policy_link"),
]

DEPENDENT_PASSAGE_PATTERNS = [
    (r"\b(as\s+mentioned\s+(above|earlier|previously)|in\s+the\s+previous\s+(section|chapter|paragraph))\b", "dependent_above"),
    (r"\b(as\s+we\s+(saw|discussed)\s+earlier|see\s+above)\b", "cross_ref_generic"),
    (r"\b(как\s+(сказано|отмечалось|упоминалось)\s+(выше|ранее)|в\s+предыдущ(ем|ей)\s+(разделе|главе))\b", "dependent_ru"),
]

UNBOUND_STAT_PATTERNS = [
    (r"\b(studies\s+show|research\s+indicates|data\s+suggests|surveys\s+reveal)\b", "unbound_passive_en"),
    (r"\b(исследования\s+показывают|по\s+данным\s+опросов|статистика\s+говорит)\b", "unbound_passive_ru"),
]


def count_signals(text: str, patterns: list) -> dict:
    """Count signal hits per pattern."""
    counts = {name: 0 for _, name in patterns}
    for pattern, name in patterns:
        hits = re.findall(pattern, text, flags=re.IGNORECASE)
        counts[name] = len(hits)
    return counts


def score_dimension(signals: dict, scale: int = 100) -> int:
    """Deterministic score calculation per dimension."""
    active = sum(1 for count in signals.values() if count > 0)
    density = sum(min(count, 3) for count in signals.values())
    total_slots = len(signals)
    breadth = (active / total_slots) * (scale * 0.6)
    depth = min(density / (total_slots * 1.5), 1.0) * (scale * 0.4)
    return int(round(breadth + depth))


def fetch_url(url: str, timeout: int = 10) -> str | None:
    """Fetch content from live URL."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (aeo_audit.py; stdlib urllib)"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        sys.stderr.write(f"[aeo_audit] URL fetch failed: {e}\n")
        return None


# ─────────────────────────────────────────────────────────────────────────
# Specialized GEO & Passage checks
# ─────────────────────────────────────────────────────────────────────────

def check_title_self_containment(text: str) -> Dict[str, Any]:
    """Check if title is an informative, self-contained statement (ideal for labrador)."""
    title_match = re.search(r"<title>(.+?)</title>|^#\s+(.+)$", text, flags=re.MULTILINE | re.IGNORECASE)
    if not title_match:
        return {"found": False, "title": "", "length_chars": 0, "verdict": "NO_TITLE", "score": 0}
    title = (title_match.group(1) or title_match.group(2)).strip()
    length = len(title)

    if length < 25:
        score = 40
        verdict = "TOO_SHORT_GENERIC"
    elif 40 <= length <= 250:
        score = 100
        verdict = "EXCELLENT_SELF_CONTAINED"
    else:
        score = 80
        verdict = "ACCEPTABLE"

    return {
        "found": True,
        "title": title,
        "length_chars": length,
        "score": score,
        "verdict": verdict,
    }


def check_image_alt_text(text: str) -> Dict[str, Any]:
    """Audit images for factual alt-text (critical because OpenAI strips JSON-LD in Markdown cache)."""
    md_images = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    html_images = re.findall(r"<img[^>]+alt=[\"'](.*?)[\"']", text, flags=re.IGNORECASE)
    all_alts = [alt.strip() for alt, _ in md_images] + [alt.strip() for alt in html_images]
    total_imgs = len(md_images) + len(re.findall(r"<img\b", text, flags=re.IGNORECASE))

    if total_imgs == 0:
        return {
            "total_images": 0,
            "images_with_alt": 0,
            "factual_alts_count": 0,
            "verdict": "NO_IMAGES_PRESENT",
            "score": 75,
        }

    factual_alts = sum(1 for alt in all_alts if len(alt.split()) >= 4 and not re.match(r"^(image|photo|screenshot|icon|logo)\b", alt, re.IGNORECASE))
    score = int(round((len(all_alts) / total_imgs) * 50 + (factual_alts / max(len(all_alts), 1)) * 50))

    return {
        "total_images": total_imgs,
        "images_with_alt": len(all_alts),
        "factual_alts_count": factual_alts,
        "score": min(score, 100),
        "verdict": "GOOD_SURVIVABILITY" if factual_alts >= 1 else "WEAK_ALT_TEXT",
    }


def check_chatgpt_instant_budget(text: str) -> Dict[str, Any]:
    """
    Evaluate the 200-character grounding budget immediately following H1.
    ChatGPT Instant extracts title + first ~200 characters directly under H1.
    """
    h1_match = re.search(r"^#\s+(.+)$|<h1[^>]*>(.+?)</h1>", text, flags=re.MULTILINE | re.IGNORECASE)
    if not h1_match:
        return {
            "h1_found": False,
            "first_200_chars": "",
            "has_noise": True,
            "score": 0,
            "verdict": "CRITICAL: No H1 found. ChatGPT Instant cannot establish category anchor.",
        }

    h1_end = h1_match.end()
    post_h1 = text[h1_end:].strip()
    first_block = post_h1[:250].strip()
    first_200 = first_block[:200]

    noise_patterns = [
        (r"\b(table\s+of\s+contents|оглавление|содержание)\b", "table_of_contents"),
        (r"\b(home\s*>\s*blog|breadcrumbs?)\b", "breadcrumbs"),
        (r"^\s*(\*|_)?Published\s+on\s+[\w\s\d,]+(\*|_)?$", "bare_date_line"),
    ]
    detected_noise = []
    for pat, name in noise_patterns:
        if re.search(pat, first_200, flags=re.IGNORECASE | re.MULTILINE):
            detected_noise.append(name)

    has_substance = bool(re.search(r"\b(is|are|means|refers\s+to|measures|provides|allows|это|является)\b", first_200, flags=re.IGNORECASE))

    score = 100
    if detected_noise:
        score -= len(detected_noise) * 35
    if not has_substance:
        score -= 40
    score = max(0, min(100, score))

    verdict = "EXCELLENT" if score >= 80 else ("NEEDS_IMPROVEMENT" if score >= 50 else "POOR_GROUNDING")

    return {
        "h1_found": True,
        "first_200_chars": first_200.replace("\n", " "),
        "has_noise": len(detected_noise) > 0,
        "noise_types": detected_noise,
        "score": score,
        "verdict": verdict,
    }


def check_self_contained_passages(text: str) -> Dict[str, Any]:
    """Check for dependent cross-references that break isolated passage extraction."""
    hits = []
    for pat, name in DEPENDENT_PASSAGE_PATTERNS:
        matches = re.findall(pat, text, flags=re.IGNORECASE)
        if matches:
            hits.extend([m[0] if isinstance(m, tuple) else m for m in matches])

    score = 100 - (len(hits) * 20)
    score = max(0, min(100, score))
    return {
        "dependent_phrase_count": len(hits),
        "examples": hits[:5],
        "score": score,
        "verdict": "CLEAN" if len(hits) == 0 else "CONTAINS_DEPENDENT_CROSS_REFS",
    }


def check_ghost_citation_risk(text: str) -> Dict[str, Any]:
    """Identify statistics without explicit attribution to a named study or brand."""
    unbound_hits = []
    for pat, name in UNBOUND_STAT_PATTERNS:
        matches = re.findall(pat, text, flags=re.IGNORECASE)
        if matches:
            unbound_hits.extend(matches)

    stats_count = len(re.findall(r"\b\d+%\b|\$\d+", text))
    has_named_source = bool(re.search(r"\b(survey|index|report|study|benchmark)\b", text, flags=re.IGNORECASE))

    risk = "LOW"
    if len(unbound_hits) > 0:
        risk = "HIGH"
    elif stats_count > 0 and not has_named_source:
        risk = "MEDIUM"

    return {
        "unbound_claim_phrases": len(unbound_hits),
        "total_stats_found": stats_count,
        "has_named_study_anchor": has_named_source,
        "ghost_citation_risk": risk,
    }


def analyze_structure(text: str) -> dict:
    """Score structural readiness for passage extraction."""
    h2_count = len(re.findall(r"^##\s+|^<h2\b", text, flags=re.MULTILINE | re.IGNORECASE))
    h3_count = len(re.findall(r"^###\s+|^<h3\b", text, flags=re.MULTILINE | re.IGNORECASE))
    list_items = len(re.findall(r"^\s*[-*+]\s+|<li\b", text, flags=re.MULTILINE | re.IGNORECASE))
    table_count = len(re.findall(r"^\|.*\|\s*$|<table\b", text, flags=re.MULTILINE | re.IGNORECASE))
    word_count = len(text.split())

    h2_lines = re.findall(r"^##\s+(.+)$|<h2[^>]*>(.+?)</h2>", text, flags=re.MULTILINE | re.IGNORECASE)
    question_h2s = sum(
        1 for line in h2_lines
        if any(w in (line[0] or line[1]).lower() for w in ["?", "what", "how", "why", "when", "как", "что", "почему"])
    )

    structure_score = 0
    if h2_count >= 3: structure_score += 20
    elif h2_count >= 1: structure_score += 10
    if h3_count >= 3: structure_score += 15
    if question_h2s >= 1: structure_score += 15
    if list_items >= 5: structure_score += 15
    if table_count >= 1: structure_score += 20
    if word_count >= 600: structure_score += 15

    return {
        "h2_count": h2_count,
        "h2_question_count": question_h2s,
        "h3_count": h3_count,
        "list_items": list_items,
        "table_count": table_count,
        "word_count": word_count,
        "structure_score": min(structure_score, 100),
    }


# ─────────────────────────────────────────────────────────────────────────
# Main audit logic
# ─────────────────────────────────────────────────────────────────────────

def audit(text: str, url: str | None, industry: str) -> dict:
    """Run full audit across E-E-A-T, ChatGPT Grounding, and GEO criteria."""
    exp_signals = count_signals(text, EXPERIENCE_PATTERNS)
    expert_signals = count_signals(text, EXPERTISE_PATTERNS)
    auth_signals = count_signals(text, AUTHORITY_PATTERNS)
    trust_signals = count_signals(text, TRUST_PATTERNS)

    exp_score = score_dimension(exp_signals)
    expert_score = score_dimension(expert_signals)
    auth_score = score_dimension(auth_signals)
    trust_score = score_dimension(trust_signals)

    structure = analyze_structure(text)
    chatgpt_instant = check_chatgpt_instant_budget(text)
    self_contained = check_self_contained_passages(text)
    ghost_risk = check_ghost_citation_risk(text)
    title_eval = check_title_self_containment(text)
    image_eval = check_image_alt_text(text)

    # Technical Payload Check (< 4 MB)
    raw_size_bytes = len(text.encode("utf-8"))
    payload_status = "PASS"
    if raw_size_bytes > 4 * 1024 * 1024:
        payload_status = "CRITICAL_EXCEEDS_4MB"
    elif raw_size_bytes > 2.5 * 1024 * 1024:
        payload_status = "WARNING_HEAVY"

    composite = int(round(
        (exp_score + expert_score + auth_score + trust_score) * 0.15
        + structure["structure_score"] * 0.15
        + chatgpt_instant["score"] * 0.15
        + title_eval["score"] * 0.05
        + image_eval["score"] * 0.05
    ))

    cfg = INDUSTRIES.get(industry.lower(), INDUSTRIES["saas"])
    threshold = cfg["min_composite"]
    verdict = "PASS" if composite >= threshold else "BELOW_THRESHOLD"

    top_fixes = []
    if chatgpt_instant["score"] < 70:
        top_fixes.append(("ChatGPT Instant Budget", "Place direct 1-sentence answer in first 200 chars under H1; remove breadcrumbs/TOC from lede"))
    if title_eval["score"] < 70:
        top_fixes.append(("Title Informativeness", "Write Title as an informative self-contained sentence (labrador index does not truncate up to 289 chars)"))
    if image_eval["score"] < 70 and image_eval["total_images"] > 0:
        top_fixes.append(("Markdown Cache Survivability", "Enrich image alt-text with factual numbers/findings (survives when OpenAI strips JSON-LD)"))
    if auth_signals.get("schema_org_jsonld", 0) == 0 and auth_signals.get("schema_script", 0) == 0:
        top_fixes.append(("Authoritativeness", "Add schema.org JSON-LD markup for Article + FAQPage + Author"))
    if auth_signals.get("llms_txt_reference", 0) == 0:
        top_fixes.append(("Authoritativeness", "Publish an llms.txt at domain root and link to it in documentation"))
    if self_contained["dependent_phrase_count"] > 0:
        top_fixes.append(("Passage Independence", "Remove dependent cross-references ('as mentioned above') so passages extract cleanly"))
    if ghost_risk["ghost_citation_risk"] == "HIGH":
        top_fixes.append(("Anti-Ghost Citation", "Bind stats to your brand name ('[Brand] Study revealed...') instead of 'Studies show'"))
    if structure["table_count"] == 0:
        top_fixes.append(("Structure", "Add comparison table for options/features (tables have highest citation rate in AI Overviews)"))

    return {
        "url": url,
        "industry": industry,
        "audited_at": datetime.now(timezone.utc).isoformat(),
        "composite_score": composite,
        "verdict": verdict,
        "threshold": threshold,
        "letter_grade": _letter_grade(composite),
        "dimensions": {
            "experience": {"score": exp_score, "signals": exp_signals},
            "expertise": {"score": expert_score, "signals": expert_signals},
            "authoritativeness": {"score": auth_score, "signals": auth_signals},
            "trustworthiness": {"score": trust_score, "signals": trust_signals},
            "structure": structure,
        },
        "geo_readiness": {
            "title_evaluation": title_eval,
            "chatgpt_instant_budget": chatgpt_instant,
            "image_alt_survivability": image_eval,
            "passage_self_containment": self_contained,
            "ghost_citation_risk": ghost_risk,
            "payload_size_bytes": raw_size_bytes,
            "payload_status": payload_status,
        },
        "top_fixes": top_fixes[:5],
        "audit_trail": {
            "patterns_evaluated": len(EXPERIENCE_PATTERNS) + len(EXPERTISE_PATTERNS) + len(AUTHORITY_PATTERNS) + len(TRUST_PATTERNS),
            "text_length_chars": len(text),
            "text_length_words": structure["word_count"],
        },
    }


def _letter_grade(score: int) -> str:
    if score >= 90: return "A"
    if score >= 85: return "A-"
    if score >= 80: return "B+"
    if score >= 75: return "B"
    if score >= 70: return "B-"
    if score >= 65: return "C+"
    if score >= 60: return "C"
    if score >= 50: return "D"
    return "F"


def format_markdown_report(res: dict) -> str:
    gr = res["geo_readiness"]
    lines = [
        f"# AEO & GEO Audit Report — {res['url'] or 'Document'}",
        "",
        f"**URL / Input:** `{res['url'] or 'Local Document'}`  ",
        f"**Date:** {res['audited_at']}  ",
        f"**Industry:** {res['industry']}  ",
        f"**Composite Score:** **{res['composite_score']}/100** ({res['letter_grade']})  ",
        f"**Threshold Verdict:** `{res['verdict']}` (Threshold: {res['threshold']})",
        "",
        "## 1. Dimension Breakdown",
        "",
        "| Dimension | Score | Verdict |",
        "|---|---|---|",
        f"| Experience | {res['dimensions']['experience']['score']}/100 | {'🟢 Healthy' if res['dimensions']['experience']['score'] >= 70 else '🟡 Low'} |",
        f"| Expertise | {res['dimensions']['expertise']['score']}/100 | {'🟢 Healthy' if res['dimensions']['expertise']['score'] >= 70 else '🟡 Low'} |",
        f"| Authoritativeness | {res['dimensions']['authoritativeness']['score']}/100 | {'🟢 Healthy' if res['dimensions']['authoritativeness']['score'] >= 70 else '🟡 Low'} |",
        f"| Trustworthiness | {res['dimensions']['trustworthiness']['score']}/100 | {'🟢 Healthy' if res['dimensions']['trustworthiness']['score'] >= 70 else '🟡 Low'} |",
        f"| Structure & Extraction | {res['dimensions']['structure']['structure_score']}/100 | {'🟢 Healthy' if res['dimensions']['structure']['structure_score'] >= 70 else '🟡 Low'} |",
        "",
        "## 2. GEO & AI Engine Readiness (Playbook V2)",
        "",
        f"- **Title Self-Containment (labrador):** `{gr['title_evaluation']['verdict']}` ({gr['title_evaluation']['length_chars']} chars)",
        f"- **ChatGPT Instant Grounding (200 chars):** `{gr['chatgpt_instant_budget']['verdict']}` ({gr['chatgpt_instant_budget']['score']}/100)",
        f"  *Post-H1 Hook:* \"{gr['chatgpt_instant_budget']['first_200_chars'][:120]}...\"",
        f"- **Image Alt-Text / Markdown Cache Survivability:** `{gr['image_alt_survivability']['verdict']}` ({gr['image_alt_survivability']['factual_alts_count']} factual alts out of {gr['image_alt_survivability']['total_images']} images)",
        f"- **Passage Self-Containment:** `{gr['passage_self_containment']['verdict']}` ({gr['passage_self_containment']['dependent_phrase_count']} dependent phrases found)",
        f"- **Ghost Citation Risk:** `{gr['ghost_citation_risk']['ghost_citation_risk']}`",
        f"- **Technical Payload Size:** {gr['payload_size_bytes']} bytes (`{gr['payload_status']}`)",
        "",
        "## 3. Top Actionable Fixes (Priority Order)",
        "",
    ]

    for i, (dim, fix) in enumerate(res["top_fixes"], 1):
        lines.append(f"{i}. **[{dim}]** {fix}")

    lines.extend([
        "",
        "## 4. Extraction Signal Counts",
        "",
        f"- H2 Count: {res['dimensions']['structure']['h2_count']} (Question-phrased: {res['dimensions']['structure']['h2_question_count']})",
        f"- Tables Found: {res['dimensions']['structure']['table_count']}",
        f"- Lists Found: {res['dimensions']['structure']['list_items']}",
        f"- Total Words: {res['dimensions']['structure']['word_count']}",
    ])

    return "\n".join(lines)


SAMPLE_CONTENT = """# How to Optimize Modern Enterprise Search Architectures for LLM Citations in 2026

Answer Engine Optimization helps content get cited by LLMs. In 2026, 47% of discovery queries originate in AI engines.

![Comparison benchmark chart showing 42ms vector search latency on AWS](https://example.com/chart.png)

## What is the difference between SEO and AEO?
SEO optimizes for human click-through rankings, whereas AEO optimizes for machine citation.

| Strategy | Goal | Metric |
|---|---|---|
| SEO | SERP Position | Clicks |
| AEO | AI Citation | Mention Count |

In our test of 120 client queries, AEO increased referral traffic by $14,000 in Q1 2026 [1].

## Next Steps
Contact our team at team@example.com for our corrections policy and disclosures.
"""


def main():
    parser = argparse.ArgumentParser(description="AEO & GEO Content Auditor")
    parser.add_argument("--input", help="Path to markdown/text file")
    parser.add_argument("--url", help="Live HTTP/HTTPS URL to audit")
    parser.add_argument("--industry", default="saas", choices=list(INDUSTRIES.keys()), help="Target industry")
    parser.add_argument("--output", choices=["markdown", "json"], default="markdown", help="Output format")
    parser.add_argument("--sample", action="store_true", help="Run audit on built-in sample content")
    args = parser.parse_args()

    if args.sample:
        text = SAMPLE_CONTENT
        target = "sample://builtin/aeo-guide"
    elif args.input:
        p = Path(args.input)
        if not p.exists():
            sys.stderr.write(f"Error: file not found: {args.input}\n")
            sys.exit(1)
        text = p.read_text(encoding="utf-8")
        target = str(p)
    elif args.url:
        text = fetch_url(args.url)
        if text is None:
            sys.exit(1)
        target = args.url
    else:
        parser.print_help()
        sys.exit(0)

    result = audit(text=text, url=target, industry=args.industry)

    if args.output == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_markdown_report(result))


if __name__ == "__main__":
    main()
