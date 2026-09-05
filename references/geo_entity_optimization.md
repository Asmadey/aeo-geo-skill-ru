# Generative Engine Optimization (GEO) & Entity Signals

Generative Engine Optimization (GEO) focuses on positioning your brand, data, and perspectives within the generative knowledge synthesis layer of modern AI engines (Google AI Overviews, Perplexity Answers, ChatGPT Search, Claude).

---

## 1. The 5-Layer AI Visibility Framework

Visibility in AI-driven search is built on five stacked layers that compound:

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 5: Real-World Entity Signals (Wikidata, Knowledge)   │
├─────────────────────────────────────────────────────────────┤
│  Layer 4: AI Accessibility (llms.txt, Clean HTML, SSR)      │
├─────────────────────────────────────────────────────────────┤
│  Layer 3: Machine-Readable Schema (Person, FAQ, HowTo, Org) │
├─────────────────────────────────────────────────────────────┤
│  Layer 2: Citation Worthiness (Primary Data, E-E-A-T, Dates)│
├─────────────────────────────────────────────────────────────┤
│  Layer 1: Extractable Semantic Structure (Atomic Facts)     │
└─────────────────────────────────────────────────────────────┘
```

### Layer 1: Extractable Semantic Structure
AI models do not index entire pages at once; they retrieve **semantic passages (chunks)**.
- Every H2 section should be self-contained and answer one query directly.
- Tables, ordered lists, and bold summary sentences allow deterministic extraction.

### Layer 2: Citation Worthiness
AI models are trained with guardrails against hallucinating facts and prefer citing primary authorities:
- **Original Data:** Proprietary benchmarks, survey metrics, case study numbers.
- **Explicit Author Credentials:** "Reviewed by [Dr. Jane Doe, PhD]" with author bios.
- **Recency Signals:** Explicit `datePublished` and `dateModified` timestamps.

### Layer 3: Machine-Readable Schema Depth
Schema is machine-readable semantic language:
- Use `Person` schema with `sameAs` links to LinkedIn, Google Scholar, GitHub.
- Use `Organization` schema with logo, contacts, and corporate identifiers.
- Use `FAQPage` and `HowTo` schemas only where authentic question/step pairs exist.

### Layer 4: AI Accessibility
- Provide `llms.txt` at the domain root.
- Ensure `robots.txt` explicitly permits AI crawlers (`GPTBot`, `PerplexityBot`, `ClaudeBot`).
- Avoid rendering critical factual answers exclusively via heavy client-side JavaScript.

### Layer 5: Real-World Entity Signals
AI engines cross-reference brands against knowledge graphs:
- Ensure consistent NAP (Name, Address, Phone, Website) across the web.
- Claim and maintain Wikidata entries for notable entities.
- Cultivate brand co-occurrences in authoritative trade publications.

---

## 2. 12 High-Yield AI Extraction Patterns

Apply these patterns to make content instantly extractable by answer engines:

1. **Question-Led Headings:** Phrase H2s/H3s as literal user queries (`## How long does vector indexing take?`).
2. **Answer-First Paragraph:** Place the direct 1–2 sentence answer immediately under the heading before elaborating.
3. **Inverse-Pyramid Definitions:** Define key terms in the first sentence; explain technical nuances in subsequent sentences.
4. **Numbered Lists for Procedures:** Use sequential numbers with bold action verbs for how-tos (`1. **Download** the CLI tool...`).
5. **Bullet Lists for Parallel Items:** Format feature lists and option sets as discrete bullets.
6. **Side-by-Side Comparison Tables:** Compare 2+ alternatives across 2+ criteria in markdown tables.
7. **Explicit Q&A Formatting:** Use `**Q:**` and `A:` blocks for discrete FAQ snippets.
8. **Self-Contained Sections:** Ensure each H2 section makes sense if read completely isolated from previous sections (avoid "as mentioned earlier").
9. **Specific Quantifiers & Sample Sizes:** Replace vague terms ("many customers") with concrete numbers ("In our survey of 450 enterprises, 68%...").
10. **Visible Metadata & Byline:** Include author name, credentials, date published, and date modified at the top of every guide.
11. **Explicit Topic Boundaries:** State clearly what the guide covers and what falls outside its scope to prevent LLMs conflating topics.
12. **TL;DR / Key Takeaways Box:** A 3–5 bullet summary box at the start of long-form articles.

---

## 3. How to Test GEO Extraction Readiness

1. **Heading + Lede Test:** Read only your H1 and the first sentence under each H2. Does the document still provide a comprehensive, logical summary?
2. **Table & List Extraction:** Verify that all comparative conclusions are present in text/tables, not trapped inside images or infographic PDFs.
3. **AI Search Prompting:** Prompt ChatGPT Search and Perplexity with the exact H2 question. Check if your domain is cited as a source pill.
