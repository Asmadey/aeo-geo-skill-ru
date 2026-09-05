# 3-Agent Content Verification Pipeline & Anti-Slop Protocol

Modern search and AI engines do not penalize content simply because it was drafted with AI assistance. They aggressively penalize **unoriginal, unverified, boilerplate text (AI Slop)** that adds zero new information to the web's knowledge graph.

To ensure every published asset passes both algorithmic originality filters and human editorial standards, follow this strict **3-Agent Verification Pipeline**.

---

## 1. The Production Loop with Human Gates

```text
┌─────────────────────────────────────────────────────────────┐
│  Phase 1: Prompt Research & Topical Brief                   │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│  [GATE 1: HUMAN APPROVAL] Topic & Angle Sign-off             │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│  Phase 2: First Draft Assembly                              │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│  Phase 3: 3-Agent Adversarial Verification Gate             │
│  ├── Agent A: Structural Editor                             │
│  ├── Agent B: Adversarial Fact-Checker                      │
│  └── Agent C: Anti-AI-Tells Reviewer                        │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│  [GATE 2: HUMAN REVIEW] Final Quality & Lived-Detail Check  │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│  Phase 4: Publication & IndexNow Signal                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. The 3 Reviewer Agents: Roles & Checklists

### Agent A: Structural Editor
* **Role:** Enforces the strict AEO/GEO passage contract.
* **Review Checklist:**
  - [ ] **ChatGPT Instant 200-Char Hook:** Does the text immediately following H1 provide a direct, definitive answer without navigation noise?
  - [ ] **H2 Phrasing:** Are major subheadings phrased as natural user questions?
  - [ ] **Self-Contained Passages:** Does every H2 section make complete sense if lifted entirely out of context (zero "as mentioned above")?
  - [ ] **Comparison Tables:** Are multi-criteria comparisons formatted in markdown tables rather than dense prose?

### Agent B: Adversarial Fact-Checker
* **Role:** Assumes every statistical and historical claim is a potential hallucination until verified.
* **Review Checklist:**
  - [ ] **Primary Source Citations:** Does every specific percentage, dollar figure, and date include a bracketed citation `[1]` to a verifiable primary source?
  - [ ] **Anti-Ghost Binding:** Are brand-owned statistics explicitly bound to the brand name (e.g., *"The [Brand] 2026 Survey"* instead of *"Studies show"* )?
  - [ ] **Mathematical Integrity:** Do percentages in tables and breakdowns add up to 100%?
  - [ ] **No Outdated Claims:** Are examples and data points updated for the current operating year?

### Agent C: Anti-AI-Tells Reviewer
* **Role:** Eliminates generic LLM stylistic markers and clichés.
* **Banned Vocabulary & Tells:**
  - ❌ *"In today's fast-paced digital world..."*
  - ❌ *"Delve into" / "Tapestry" / "Beacon" / "Testament to"*
  - ❌ *"It is crucial / vital / paramount to remember..."*
  - ❌ Symmetrical 3-bullet lists under every single paragraph.
  - ❌ Preachy, summarizing concluding paragraphs (*"In conclusion, the future of X is bright..."*).
* **Mandatory Injections:**
  - ✅ At least one first-person lived detail (*"In our benchmark run on AWS us-east-1..."*).
  - ✅ Varied sentence cadence (mix of 6-word punchy sentences and 25-word compound explanations).
  - ✅ Concrete edge cases and limitations where the tool/approach does *not* work.
