# AEO API Configuration & Provider Integration Guide

The AEO skill is designed with a **Graceful Degradation** philosophy:
- **Core Functionality (Default):** 100% offline, stdlib-only. Content auditing, structural analysis, schema generation, citation logging, and readability calculations require **zero external API keys**.
- **Enhanced Mode (Optional):** When provided, API keys allow enhanced backlink auditing (Ahrefs), keyword volume tracking (SEMrush), and direct LLM prompt evaluation (OpenAI, Anthropic, Gemini, Perplexity).

---

## 1. Supported API Providers

| Environment Variable | Provider | Purpose | Rate Limit |
|---|---|---|---|
| `OPENAI_API_KEY` | OpenAI (GPT-4o, o3-mini) | Real-time citation testing & content evaluation | 60 req/min |
| `ANTHROPIC_API_KEY` | Anthropic (Claude 3.5 Sonnet / Haiku) | In-depth technical reasoning & tone auditing | 50 req/min |
| `PERPLEXITY_API_KEY` | Perplexity AI (Sonar) | Direct verification of live web citation sources | 30 req/min |
| `GEMINI_API_KEY` | Google Gemini (Gemini 2.5/Flash) | Google AI Overviews simulation & testing | 60 req/min |
| `AHREFS_API_KEY` | Ahrefs | Live domain rating, backlink verification | 1 req/sec |
| `SEMRUSH_API_KEY` | SEMrush | Organic search volume, keyword difficulty | 10 req/min |

---

## 2. Configuring Keys

### Option A: Environment Variables (Recommended)
Set the keys in your shell profile (`~/.zshrc` or `~/.bashrc`):
```bash
export PERPLEXITY_API_KEY="pplx-xxxx"
export OPENAI_API_KEY="sk-xxxx"
```

### Option B: Local AEO Key Manager
You can securely store keys locally in `~/.aeo-data/api_config.json` via the CLI:
```bash
python3 scripts/api_manager.py --set PERPLEXITY_API_KEY "pplx-xxxx"
python3 scripts/api_manager.py --set OPENAI_API_KEY "sk-xxxx"
```

---

## 3. Checking Integration Status

Inspect the current status of all connectors at any time:
```bash
python3 scripts/api_manager.py --status
```

Output:
```text
=== AEO API Integration Status ===
Operational Mode: hybrid

API Keys:
  🟢 OPENAI_API_KEY       configured
  🟢 PERPLEXITY_API_KEY   configured
  ⚪ ANTHROPIC_API_KEY    missing (using local heuristic)
  ⚪ GEMINI_API_KEY       missing (using local heuristic)
  ⚪ AHREFS_API_KEY       missing (using local heuristic)
  ⚪ SEMRUSH_API_KEY      missing (using local heuristic)
```
