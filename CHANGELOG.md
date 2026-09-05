# Changelog

All notable changes to the Answer Engine Optimization (AEO) & Generative Engine Optimization (GEO) Unified Skill are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.3.0] - 2026-09-05

### 🚀 Full Playbook V2 Integration (140+ Techniques from 247 Articles)
Integrated the complete discovery set from SearchEngineLand's Playbook V2 across all tools, scripts, and documentation:
- **OpenAI Markdown Reading Cache & JSON-LD Stripping:** Discovered that OpenAI strips all `<script type="application/ld+json">` during markdown conversion. Built `references/openai_markdown_cache_and_rendering.md` and added automated alt-text enrichment in `aeo_optimizer.py` and survival audits in `aeo_audit.py`.
- **Expanded Labrador Title Optimization:** Implemented automated generation and auditing of entity-rich, complete-sentence titles (up to 250–289 characters) tailored for OpenAI's `labrador` dense retriever index.
- **Multimodal Image GEO (Google Patent):** Integrated Google's Image-First matching patent and 20B Google Lens queries into `references/multimodal_image_geo.md`; added image denotation auditing.
- **Accessibility Tree for AI Agents:** Created `references/accessibility_tree_for_ai_agents.md` defining ARIA landmarks and accessible names for autonomous browser agents (ChatGPT Atlas, WebMCP, Playwright).
- **56-Day GSC Baseline & Keep/Fix/Remove/Add Refresh Matrix:** Created `references/page_refresh_and_cannibalization.md` and added `--refresh-matrix` generation to `report_generator.py` with 3-step Page Independence Test to prevent URL cannibalization.
- **Dark Funnel Recovery (GA4):** Added `#:~:text=` URL Text Fragment tracking guidance to `query_researcher.py` to recover the 22.4% of AI Overview traffic misclassified as Direct.
- **Funnel-Mapped Query Research:** Extended `query_researcher.py` with ToFU (Problem Discovery), MoFU (Comparison & Benchmarks), and BoFU (Vendor Selection & ROI) categories.

---

## [2.2.0] - 2026-09-05

### 🚀 Playbook V2 & Zero-to-Top Architecture
Upgraded the framework based on empirical findings from SearchEngineLand's Playbook V2 (247 articles):
- **4 Visibility Channels Model:** Integrated dedicated optimization workflows for ChatGPT Instant (`labrador` index), ChatGPT Thinking (`ChatGPT-User` live opens), Perplexity/Gemini/AI Overviews, and Google Organic.
- **ChatGPT Instant 200-Char Grounding Budget:** Added automated audit and optimization checks in `aeo_audit.py` and `aeo_optimizer.py` to ensure the post-H1 lede delivers direct answers without navigation noise.
- **Anti-Ghost Citation Engine:** Added `--brand` parameter to `aeo_optimizer.py` to bind factual statistics directly to brand names in sentences; added Ghost Citation Ratio calculation to `citation_tracker.py`.
- **Passage Independence Scoring:** Added heuristic detection of dependent cross-references (*"as mentioned above"*) to enforce 117-word self-contained passage architecture.
- **Technical AI Guardrails:** Enforced `< 4 MB` payload limits and `< 30-day` freshness validation.
- **New Strategic Guides:** Added `references/chatgpt_instant_vs_thinking.md`, `references/third_party_ugc_footprint.md`, `references/anti_ghost_citation_guide.md`, and `references/content_verification_pipeline.md`.

---

## [2.1.0] - 2026-09-05

### ✨ GEO & llms.txt Integration
Integrated core methodologies from `rampstackco/seo-aeo-geo`, expanding the skill into a complete AEO + GEO framework:
- **llms.txt Guide & Standard:** Added `references/llms_txt_guide.md` with standard format rules, curated link guidelines, and SaaS/Publisher templates.
- **llms.txt CLI Generator & Validator:** Added `scripts/llms_txt_generator.py` to generate valid `llms.txt`, validate existing files, and concatenate markdown into `llms-full.txt`.
- **GEO 5-Layer Stack & 12 Extraction Patterns:** Added `references/geo_entity_optimization.md` covering entity building, knowledge panels, and 12 proven semantic extraction block patterns.

---

## [2.0.0] - 2026-09-05

### 🚀 Unified Production Release
Merged and standardized the two independent implementations into a single, comprehensive Agent Skill conforming to modern Agent Skills standards.
