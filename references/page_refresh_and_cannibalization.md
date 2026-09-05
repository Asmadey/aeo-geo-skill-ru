# Page Refresh Strategy, Cannibalization & Page Independence Test

Updating existing pages delivers significantly higher ROI than publishing unranked new URLs. In AI search, **76.4% of top-cited pages in ChatGPT have been updated within the past 30 days**.

However, haphazard updates cause self-inflicted demotions. Follow this disciplined protocol.

---

## 1. The 56-Day GSC Baseline

Before touching any live page:
1. Export Google Search Console performance data for the target URL for the prior **56 days** (8 full weeks).
2. Record:
   - Total clicks, impressions, and average CTR.
   - Primary ranking queries and their exact average position.
   - Queries in the **striking-distance window (positions 5–20)**.
3. **Lock this baseline:** Do not alter the page until this baseline snapshot is saved.

---

## 2. The Keep / Fix / Remove / Add Section Framework

Audit the document section-by-section using four explicit tags:

| Action Tag | Condition | Execution Standard |
|---|---|---|
| **KEEP** | Section ranks for target queries and factual data remains 100% accurate. | Do not touch sentence structure or phrasing. Preserve keyword associations. |
| **FIX** | Concept is correct, but execution is outdated (e.g., old 2024 dates, vague numbers). | Update numbers, inject current year, verify primary source links, add anti-ghost brand binding. |
| **REMOVE** | Information is obsolete, discredited, or represents duplicate thin content. | Delete the block cleanly. Verify removal does not break semantic transitions. |
| **ADD** | Crucial customer question identified in prompt research or striking-distance queries is missing. | Write a new, self-contained H2 block following the 117-word atomic passage format. |

---

## 3. The 3-Step Page Independence Test

Before creating a net-new page, run this test to prevent keyword cannibalization:

```text
Step 1: GSC Cannibalization Check
Does an existing page already receive impressions for this query cluster?
  ├── YES ➔ EXPAND existing page. Do NOT create a new URL.
  └── NO  ➔ Proceed to Step 2.

Step 2: Top-10 SERP Overlap Analysis
Compare Google's top 10 results for Query A vs. Query B.
  ├── High Overlap (5+ shared URLs) ➔ Google considers them the SAME intent.
  │   EXPAND existing page with an H2 section.
  └── Low Overlap (<3 shared URLs)  ➔ Distinct intent. Proceed to Step 3.

Step 3: Self-Containment Assessment
Can the topic support a 600+ word self-contained guide with proprietary data?
  ├── YES ➔ APPROVED: Create dedicated cluster page.
  └── NO  ➔ Combine into the main pillar guide.
```

---

## 4. The Golden Rules of Content Refresh

1. **NEVER change a functioning URL slug:** Renaming `/guide-2025` to `/guide-2026` destroys accumulated historical link equity and resets AI crawler trust. Keep the canonical URL static (e.g., `/guide`) and update the content.
2. **NEVER rewrite a functioning Title tag:** If a title ranks in positions 1–3, modifying it risks immediate keyword displacement. Only expand or clarify; never replace.
3. **Extend Schema, never replace:** Add new `FAQPage` entities or updated `dateModified` fields without deleting existing `Article` or `Organization` nodes.
4. **Fact-check every number:** Verify pricing, latency statistics, and dates. AI models penalize documents with demonstrably disproven numbers.
