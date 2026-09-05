# AEO Success Patterns & Adaptive Learning Guide

How to build and exploit high-performing content structures that AI models prioritize for citations.

---

## 1. Why Patterns Matter for AI Answer Engines

Unlike Google's PageRank (which treats the entire document as a weighted node in a backlink graph), LLM retrieval systems (RAG, perplexity-like search pipelines, AI Overviews) work with **extracted semantic chunks**:
1. Search query is embedded or expanded into keywords.
2. Web scraper retrieves top ranking pages.
3. Chunker splits the page into ~200-500 token passages.
4. Reranker selects top 3-5 passages based on **information density**, **conciseness**, and **direct factual answering**.
5. Generation model writes an answer citing the exact chunk that answered the user query.

If your content chunk is structured to match the retrieval model's ideal passage, you win the citation.

---

## 2. The 4 Proven AEO Block Patterns

### Pattern A: Definition Block (Single-Sentence Primacy)
* **LLM Match:** Definitions, "What is X", glossary queries.
* **Format:**
  ```markdown
  ## What is [Topic]?
  **[Topic] is [one-sentence direct definition without fluff].** [One sentence highlighting historical context or 2026 data point] [1].
  ```
* **Lift:** +40% citation frequency in Perplexity and Gemini.

### Pattern B: The Trade-off Comparison Table
* **LLM Match:** "X vs Y", "Best alternatives to X".
* **Format:** Markdown table with 4 columns: Feature / Criterion, Solution A, Solution B, Source/Verification.
* **Why it works:** LLM attention mechanisms parse markdown tables with high fidelity. Tables are cited as definitive source charts.

### Pattern C: Attributed Statistics (Primary Data)
* **LLM Match:** Industry trends, benchmarks, adoption rates.
* **Format:**
  ```markdown
  According to [Authoritative Survey/Research] (2026, n=[Sample Size]), **[Metric]%** of [Audience] experienced [Outcome] [Reference Marker].
  ```
* **Why it works:** LLM guardrails penalize hallucinating statistics. When user asks for numbers, LLMs strictly require a cited source.

### Pattern D: Step-by-Step Executable Runbook
* **LLM Match:** "How to do X", implementation workflows.
* **Format:** Ordered list where every item begins with an **active verb** and includes expected time/outcome.

---

## 3. Tracking Your Success Patterns

When you notice your domain cited in ChatGPT or Perplexity:
```bash
python3 scripts/success_patterns.py --record \
  --pattern "attributed_statistic" \
  --url "https://example.com/blog/metrics-2026" \
  --llm "perplexity" \
  --query "AEO adoption statistics" \
  --notes "Cited directly as source #1 in top pill"
```

Inspect your organization's accumulated patterns:
```bash
python3 scripts/success_patterns.py --stats
```
