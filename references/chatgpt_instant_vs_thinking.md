# ChatGPT Instant (Labrador) vs. ChatGPT Thinking: Architecture & Optimization

Understanding the dual-engine architecture of OpenAI Search is essential for modern AEO. ChatGPT does not process the web with a single monolithic crawler; it divides queries between two completely different retrieval mechanisms.

---

## 1. The Two Retrieval Mechanisms

| Feature | ChatGPT Instant (Free tier, ~90% of queries) | ChatGPT Thinking / Deep Search (Paid tiers) |
|---|---|---|
| **Underlying Engine** | OpenAI's proprietary index: `labrador` + Bing corpus | Real-time web navigation agent |
| **Crawler / User-Agent** | `OAI-SearchBot` / background indexing | `ChatGPT-User` (live open) |
| **Information Budget** | **Title + first ~200 characters directly following H1** | Full rendered HTML document |
| **Page Opening** | Does **NOT** open the live page during synthesis | Opens live pages (74% citation rate for opened pages vs 7% for unopened) |
| **Latency Budget** | < 800 milliseconds | 5–40 seconds (multi-step reasoning) |

---

## 2. The 200-Character Grounding Budget (ChatGPT Instant)

Because ChatGPT Instant serves millions of real-time queries per second, it cannot afford to fetch and parse full DOMs for every user prompt. It relies on pre-indexed summary vectors and a strict **200-character grounding window**:

```text
┌─────────────────────────────────────────────────────────────┐
│ <h1>How to Calculate Cloud Egress Latency</h1>              │
├─────────────────────────────────────────────────────────────┤
│ ❌ BAD: Breadcrumbs > Nov 14, 2026 > By Admin > Table of    │
│    Contents (200 characters wasted on zero-information nav) │
├─────────────────────────────────────────────────────────────┤
│ ✅ GOOD: Cloud egress latency measures packet transfer      │
│    delays between AWS and GCP, averaging 42ms over public   │
│    IPs and 8ms over private interconnects [1].               │
└─────────────────────────────────────────────────────────────┘
```

### The Strict H1-to-Lede Contract:
1. **Zero Noise Between H1 and Text:** No breadcrumbs, author social pills, table of contents, or banner images between `<h1>` and the opening paragraph.
2. **Definitive Grounding Sentence:** The first 200 characters must contain the core answer, key metric, and defining entity.
3. **No Fluff:** Remove "In today's fast-paced digital world..." — every character counts toward the instant extraction budget.

---

## 3. ChatGPT Thinking & `ChatGPT-User` Live Opens

When ChatGPT enters "Deep Research" or "Thinking Mode", it dispatches autonomous requests using the `ChatGPT-User` user-agent:
- **74% Citation Probability:** If `ChatGPT-User` chooses to open your page, your probability of being cited is **74%**. If it only views snippet search results, your citation rate drops to **7%**.
- **Server Logs Monitoring:** Monitor your web server access logs for `User-Agent: ChatGPT-User`. Unlike standard referral clicks, live opens may not include UTM parameters.
- **Raw HTML Only:** `ChatGPT-User` operates with strict headless budgets. If your core text or internal links are injected via client-side JavaScript (CSR), the bot sees an empty shell.

---

## 4. The Multilingual Hack: The `/en/` Folder Multiplier

Empirical research across 240+ international domains reveals a critical finding:
- **`ChatGPT-User` over-indexes on `/en/` URLs by 2.6×.**
- In 65% to 79% of cross-border queries, ChatGPT opens the `/en/` localized version of a page even if the user query was entered in French, German, or Spanish.
- **Action Item:** If your primary website is non-English, maintain a pristine `/en/` mirror for your top 20 cornerstone guides and studies. It expands your AI citation footprint by over 200%.
