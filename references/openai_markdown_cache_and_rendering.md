# OpenAI Retrieval Stack: Markdown Reading Cache & labrador Engine

Empirical analysis across 14,000+ queries and 28 days of retrieval monitoring reveals the internal architecture of OpenAI's search ecosystem. Optimizing for Google or Bing alone is insufficient for ChatGPT because OpenAI operates a dedicated ingestion and caching pipeline.

---

## 1. The Three-Tier Architecture

OpenAI serves search results through three distinct operational tiers:

```text
┌─────────────────────────────────────────────────────────────┐
│  Tier 1: Discovery Index (`labrador`)                       │
│  OpenAI's proprietary web index. Evaluates Title + 200 chars│
├─────────────────────────────────────────────────────────────┤
│  Tier 2: Reading Cache (Shared Markdown Store)              │
│  Stale-while-revalidate full-page cache (~30 min freshness) │
├─────────────────────────────────────────────────────────────┤
│  Tier 3: Live Navigation Agent (`ChatGPT-User`)             │
│  Real-time headless page traversal (paid Thinking mode)     │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. The `labrador` Index vs. Bing

A widespread misconception is that ChatGPT is merely a wrapper around Bing:
- **Index Independence:** Only **1.5% of URLs** appearing in `labrador` match the top 20 rankings on Bing for identical queries.
- **Title Truncation Rules:**
  - **Bing:** Truncates titles strictly at 65–75 characters.
  - **`labrador`:** **Never truncates titles.** Studies documented complete titles up to **289 characters** entering the model's context window intact.
  - **AEO Rule:** Write informative, self-contained sentence titles rather than keyword-stuffed fragments.
- **Meta Descriptions:** Ignored by `labrador` during instant synthesis. The model relies strictly on the first ~200 characters following `<h1>`.

---

## 3. The Reading Cache & The JSON-LD Stripping Trap

When ChatGPT fetches a live web page, it converts the HTML to **Markdown** before caching it in its shared cluster:

### What Gets Stripped During Markdown Conversion:
- ❌ `<script>` tags: **All JSON-LD structured data is completely deleted.**
- ❌ `<iframe>` embeds and external widgets.
- ❌ Client-side rendered JavaScript that hasn't finished hydrating.

### What Survives Markdown Conversion:
- ✅ **Visible Body Text:** Headings, paragraphs, blockquotes, ordered lists.
- ✅ **Native Markdown Tables:** HTML tables converted to `| col | col |` format.
- ✅ **Image `alt` Text:** Markdown images preserve their alt tags: `![alt text](url)`.
- ✅ **CSS-Hidden Text:** Elements styled with `display: none` or `visibility: hidden` are frequently extracted during raw HTML string flattening!

> [!CRITICAL]
> **The Dual-Layer Verification Rule:** Never rely exclusively on Schema.org JSON-LD to communicate author credentials, publication dates, or product attributes. Because the Reading Cache strips JSON-LD, **all critical entities must be duplicated in visible body text or descriptive image `alt` attributes.**

---

## 4. Cache Expiration & Recrawl Mechanics

- **Stale-While-Revalidate:** Cached pages remain valid for approximately 30 minutes. If multiple users ask related questions, ChatGPT serves the cached Markdown version.
- **Cache Directives Ignored:** `Cache-Control: no-store` and `noindex` directives are ignored by the background reading cache once a page is accessed.
- **Query-Driven Refresh:** Infrequently requested URLs age indefinitely. Recrawling is not determined by site sitemaps, but by **user prompt demand** for that specific entity.
