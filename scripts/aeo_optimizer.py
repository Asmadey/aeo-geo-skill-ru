#!/usr/bin/env python3
"""
aeo_optimizer.py — Generate AEO & GEO Optimized Content Variants.

Restructures content to maximize LLM extractability:
- Enforces ChatGPT Instant 200-character grounding lede immediately under H1
- Binds stats to brand/proprietary assets to prevent Ghost Citations
- Converts dependent phrases into isolated, self-contained passages
- Injects Schema.org JSON-LD (Article + FAQPage) and editorial transparency notes

Modes:
  conservative — touch <10% of text; add schema + citations + corrections footer
  balanced     — touch <30%; clean cross-refs, H3 restructure, fact-density lede
  aggressive   — full restructure for maximum AEO/GEO passage extraction
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, List, Optional, Tuple


MODES = ["conservative", "balanced", "aggressive"]


def extract_title(text: str) -> str:
    """Extract H1 or first non-empty line."""
    h1_match = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    if h1_match:
        return h1_match.group(1).strip()
    for line in text.splitlines():
        if line.strip():
            return line.strip()[:120]
    return "Untitled"


def extract_headings(text: str) -> list:
    """Return list of (level, text) for H2-H6."""
    headings = []
    for m in re.finditer(r"^(#{2,6})\s+(.+)$", text, flags=re.MULTILINE):
        headings.append((len(m.group(1)), m.group(2).strip()))
    return headings


def generate_jsonld(title: str, headings: list, industry: str, brand: Optional[str] = None, url: str | None = None) -> str:
    """Generate schema.org JSON-LD for Article + FAQPage."""
    publisher_name = brand or "{{PUBLISHER}}"
    author_name = f"{brand} Research Team" if brand else "{{AUTHOR_NAME}}"

    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "datePublished": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "dateModified": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "author": {"@type": "Person", "name": author_name},
        "publisher": {"@type": "Organization", "name": publisher_name},
    }
    if url:
        article["url"] = url
        article["mainEntityOfPage"] = {"@type": "WebPage", "@id": url}

    # Detect question-style H2s for FAQPage schema
    question_h2s = [h[1] for h in headings if h[0] == 2 and (
        h[1].endswith("?") or re.match(r"^(what|why|how|when|where|who|which|is|are|does|do|can|как|что|почему)\b", h[1], re.IGNORECASE)
    )]
    blocks = [json.dumps(article, indent=2)]
    if len(question_h2s) >= 2:
        faq = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": "{{ANSWER_" + str(i) + "}}"},
                }
                for i, q in enumerate(question_h2s, 1)
            ],
        }
        blocks.append(json.dumps(faq, indent=2))

    return "\n\n".join(f'<script type="application/ld+json">\n{b}\n</script>' for b in blocks)


def clean_dependent_phrases(text: str) -> tuple[str, int]:
    """Replace dependent cross-references with direct statements for isolated passage extraction."""
    replacements = [
        (r"\bAs mentioned above,?\s*", ""),
        (r"\bAs discussed earlier,?\s*", ""),
        (r"\bIn the previous section,?\s*", ""),
        (r"\bКак сказано выше,?\s*", ""),
        (r"\bКак отмечалось ранее,?\s*", ""),
    ]
    changes = 0
    res = text
    for pat, rep in replacements:
        res, count = re.subn(pat, rep, res, flags=re.IGNORECASE)
        changes += count
    return res, changes


def bind_brand_to_stats(text: str, brand: str) -> tuple[str, int]:
    """Bind passive statistical claims to the brand to prevent Ghost Citations."""
    replacements = [
        (r"\b(studies show|research indicates|surveys reveal)\b", f"the {brand} 2026 Research Report revealed"),
        (r"\b(исследования показывают|по данным опросов)\b", f"согласно исследованию {brand} 2026 года"),
    ]
    changes = 0
    res = text
    for pat, rep in replacements:
        res, count = re.subn(pat, rep, res, flags=re.IGNORECASE)
        changes += count
    return res, changes


def ensure_chatgpt_grounding_hook(text: str, title: str) -> tuple[str, bool]:
    """Ensure the text immediately following H1 has a definitive 1-sentence answer without navigation noise."""
    lines = text.splitlines()
    h1_idx = -1
    for i, line in enumerate(lines):
        if line.startswith("# "):
            h1_idx = i
            break

    if h1_idx == -1:
        return text, False

    # Check the next non-empty line
    next_idx = h1_idx + 1
    while next_idx < len(lines) and not lines[next_idx].strip():
        next_idx += 1

    if next_idx >= len(lines):
        return text, False

    next_line = lines[next_idx].strip()

    # If it starts with navigation or breadcrumbs, clean it
    if any(k in next_line.lower() for k in ["table of contents", "breadcrumbs", "home >", "оглавление"]):
        lines.pop(next_idx)
        return "\n".join(lines), True

    return text, False


def add_citation_markers(text: str, density: int = 3) -> tuple[str, int]:
    """Insert [N]-style citation markers after factual-looking sentences."""
    word_count = len(text.split())
    max_insertions = max(density, word_count // 250)
    insertions = 0

    def replace_fact(m):
        nonlocal insertions
        if insertions >= max_insertions:
            return m.group(0)
        sentence = m.group(0)
        if re.search(r"\b(\d+(\.\d+)?%|\$\d|20\d{2}|\d{2,})\b", sentence) and "[" not in sentence:
            insertions += 1
            return sentence.rstrip(".") + f" [{insertions}]."
        return sentence

    new = re.sub(r"[^.!?]*[.!?]", replace_fact, text)
    return new, insertions


def add_corrections_footer(text: str, industry: str) -> str:
    """Append a corrections + disclosure footer."""
    footer = "\n\n---\n\n## Editorial Notes\n\n"
    footer += "- **Corrections & Updates:** This documentation is reviewed monthly. Contact editorial@example.com for verified updates.\n"
    if industry in ("healthcare", "finance", "legal"):
        footer += f"- **{industry.title()} Disclaimer:** Informational purposes only. Consult a licensed professional.\n"
    footer += "- **Disclosure:** {{INSERT_DISCLOSURE: affiliations, sponsorships, conflicts of interest}}\n"
    return text.rstrip() + footer


def restructure_headings(text: str) -> str:
    """Promote bold-then-paragraph to H3, and ensure question-style H2 formatting where applicable."""
    pattern = re.compile(r"^\*\*([A-Z][^*]+)\*\*\s*$", re.MULTILINE)
    text = pattern.sub(r"### \1", text)
    return text


def optimize_title_for_labrador(title: str, text: str, brand: Optional[str] = None) -> tuple[str, bool]:
    """
    Generate an expanded, self-contained title (up to 250 chars) for OpenAI's 'labrador' retriever.
    Unlike Google/Bing which truncate at 60-75 chars, labrador preserves up to 289 chars.
    A complete sentence title rich in entities and year dramatically increases retrieval probability.
    """
    if len(title) >= 70:
        return title, False

    # Extract primary topic and key entities
    first_p = ""
    for line in text.splitlines():
        line_clean = line.strip()
        if line_clean and not line_clean.startswith("#") and not line_clean.startswith("<"):
            first_p = line_clean
            break

    brand_str = f" by {brand}" if brand else ""
    current_year = datetime.now(timezone.utc).year

    # If title is too brief, formulate a descriptive entity-rich sentence
    clean_t = title.rstrip(".?!")
    new_title = f"{clean_t}: The Complete {current_year} Strategic Guide & Architecture{brand_str}"
    
    # If still short, append core premise if available
    if len(new_title) < 90 and first_p:
        snippet = re.sub(r"\[\d+\]", "", first_p)[:90].rstrip(",. ")
        new_title = f"{new_title} — How {snippet.lower()}"

    return new_title[:250], True


def enrich_image_alt_texts(text: str, brand: Optional[str] = None) -> tuple[str, int]:
    """
    Enrich markdown and HTML image alt attributes with factual denotations.
    In OpenAI's Markdown Reading Cache, all JSON-LD scripts are stripped out;
    only visible text and image alt text survive in the markdown conversion.
    Additionally, Google's Image-First matching patent extracts context around validated images.
    """
    brand_prefix = f"{brand}: " if brand else ""
    count = 0

    def md_img_repl(m):
        nonlocal count
        current_alt = m.group(1).strip()
        url = m.group(2).strip()

        # If alt text is empty or generic, enrich it
        generic_alts = {"image", "img", "chart", "diagram", "screenshot", "graphic", "photo", "pic", "рисунок", "график", "картинка"}
        if not current_alt or current_alt.lower() in generic_alts or len(current_alt) < 15:
            count += 1
            enriched_alt = f"{brand_prefix}Architecture diagram and benchmark data visualization demonstrating core mechanics"
            return f"![{enriched_alt}]({url})"
        return m.group(0)

    # Markdown images: ![alt](url)
    enriched_text = re.sub(r"!\[(.*?)\]\((.*?)\)", md_img_repl, text)

    # HTML images: <img ... alt="..." ...>
    def html_img_repl(m):
        nonlocal count
        tag = m.group(0)
        alt_m = re.search(r'alt=["\'](.*?)["\']', tag, re.IGNORECASE)
        if not alt_m or len(alt_m.group(1).strip()) < 15 or alt_m.group(1).lower() in {"image", "img", "chart", "рисунок"}:
            count += 1
            enriched_alt = f"{brand_prefix}Verified benchmark visualization and reference diagram"
            if alt_m:
                return re.sub(r'alt=["\'].*?["\']', f'alt="{enriched_alt}"', tag, flags=re.IGNORECASE)
            else:
                return tag.replace("<img ", f'<img alt="{enriched_alt}" ')
        return tag

    enriched_text = re.sub(r"<img\s+[^>]*>", html_img_repl, enriched_text, flags=re.IGNORECASE)
    return enriched_text, count


def optimize(
    text: str,
    mode: str,
    industry: str,
    brand: Optional[str] = None,
    url: str | None = None
) -> dict:
    """Apply optimizations based on mode. Returns dict with optimized text + changelog."""
    title = extract_title(text)
    headings = extract_headings(text)
    changelog = []

    result_text = text

    # Optimize title for OpenAI labrador index if under 70 chars
    new_title, title_changed = optimize_title_for_labrador(title, result_text, brand=brand)
    if title_changed:
        # Update H1 in text
        result_text = re.sub(r"^#\s+.+$", f"# {new_title}", result_text, count=1, flags=re.MULTILINE)
        changelog.append(f"Optimized H1 for OpenAI 'labrador' retriever (extended to {len(new_title)} chars): '{new_title}'")
        title = new_title

    # All modes: add schema JSON-LD
    jsonld = generate_jsonld(title, headings, industry, brand=brand, url=url)
    schema_block = f"\n\n---\n\n<!-- AEO & GEO Schema.org markup -->\n{jsonld}\n"

    # Always ensure clean post-H1 grounding hook
    result_text, hook_cleaned = ensure_chatgpt_grounding_hook(result_text, title)
    if hook_cleaned:
        changelog.append("Cleaned navigation noise from ChatGPT Instant 200-char grounding budget under H1")

    if brand:
        result_text, bound_count = bind_brand_to_stats(result_text, brand)
        if bound_count > 0:
            changelog.append(f"Bound {bound_count} statistical claims to '{brand}' to prevent Ghost Citations")

    # Enrich image alt-texts (essential for OpenAI Markdown Cache where JSON-LD is stripped)
    result_text, img_alts_enriched = enrich_image_alt_texts(result_text, brand=brand)
    if img_alts_enriched > 0:
        changelog.append(f"Enriched {img_alts_enriched} image alt texts for OpenAI Markdown Cache & Google Image-First retrieval")

    if mode == "conservative":
        result_text = add_corrections_footer(result_text, industry)
        result_text = result_text.rstrip() + schema_block
        changelog.append("Added schema.org JSON-LD (Article + FAQPage)")
        changelog.append("Added editorial notes & monthly review footer")

    elif mode == "balanced":
        result_text, dep_cleaned = clean_dependent_phrases(result_text)
        if dep_cleaned > 0:
            changelog.append(f"Converted {dep_cleaned} dependent cross-references into self-contained passages")
        result_text = restructure_headings(result_text)
        result_text, insertions = add_citation_markers(result_text, density=5)
        result_text = add_corrections_footer(result_text, industry)
        result_text = result_text.rstrip() + schema_block
        changelog.append("Promoted bold-paragraph patterns to H3 for LLM parsability")
        changelog.append(f"Added {insertions} citation markers at factual claims")
        changelog.append("Added schema.org JSON-LD")
        changelog.append("Added editorial notes & review footer")

    elif mode == "aggressive":
        result_text, dep_cleaned = clean_dependent_phrases(result_text)
        if dep_cleaned > 0:
            changelog.append(f"Converted {dep_cleaned} dependent cross-references into self-contained passages")
        result_text = restructure_headings(result_text)
        result_text, insertions = add_citation_markers(result_text, density=10)
        result_text = add_corrections_footer(result_text, industry)
        result_text = result_text.rstrip() + schema_block
        changelog.append("Aggressive restructure: optimized passages, self-containment, and primary citations")

    return {
        "mode": mode,
        "industry": industry,
        "title": title,
        "optimized_at": datetime.now(timezone.utc).isoformat(),
        "original_word_count": len(text.split()),
        "optimized_word_count": len(result_text.split()),
        "changelog": changelog,
        "optimized_content": result_text,
    }


SAMPLE_CONTENT = """# Why AEO Matters

Answer Engine Optimization helps content get cited by LLMs.

In today's fast-paced digital world, research indicates that 47% of discovery queries originate in AI engines. As mentioned above, vector databases play a huge role.

## Key trends in 2026
The industry has seen 47% growth in LLM citations vs 2024.

## Tactical recommendations
Add schema, dated examples, and author credentials.
"""


def main():
    parser = argparse.ArgumentParser(description="AEO & GEO Content Optimizer")
    parser.add_argument("--input", help="Path to input markdown file")
    parser.add_argument("--mode", default="balanced", choices=MODES, help="Optimization mode")
    parser.add_argument("--industry", default="saas", help="Target industry")
    parser.add_argument("--brand", help="Brand name to bind to claims (prevents Ghost Citations)")
    parser.add_argument("--url", help="Canonical URL of content")
    parser.add_argument("--output", help="Path to output file")
    parser.add_argument("--sample", action="store_true", help="Run with sample content")
    args = parser.parse_args()

    if args.sample:
        text = SAMPLE_CONTENT
    elif args.input:
        p = Path(args.input)
        if not p.exists():
            sys.stderr.write(f"Error: file not found: {args.input}\n")
            sys.exit(1)
        text = p.read_text(encoding="utf-8")
    else:
        parser.print_help()
        sys.exit(0)

    res = optimize(text=text, mode=args.mode, industry=args.industry, brand=args.brand, url=args.url)

    if args.output:
        out_p = Path(args.output)
        out_p.write_text(res["optimized_content"], encoding="utf-8")
        print(f"[aeo_optimizer] wrote {out_p} ({len(res['changelog'])} improvements applied)")
    else:
        print(res["optimized_content"])


if __name__ == "__main__":
    main()
