# Complete Guide to llms.txt & llms-full.txt

`llms.txt` is a curated, human-readable markdown file hosted at the root of a domain (e.g., `https://example.com/llms.txt`). It serves as an AI-era entry point — acting like a semantic sitemap and authority brief specifically structured for Language Models and retrieval agents.

---

## 1. What llms.txt Accomplishes

- **Direct Semantic Orientation:** Teaches LLMs (ChatGPT, Claude, Perplexity, Gemini) what your brand/product is and who it serves in unambiguous plain text.
- **Curated Citation Targets:** Points AI assistants to your top 10–30 highest-authority, most citable URLs rather than forcing bots to guess through thousands of sitemap links.
- **Reduces Hallucinations:** Provides verified facts, author credentials, product boundaries, and terminology definitions.
- **Fast RAG Ingestion:** Provides LLMs that fetch external context an immediate, clean summary without parsing heavy JavaScript, navigation headers, or cookie banners.

### What it is NOT:
- Not an algorithmic search ranking factor (yet).
- Not a replacement for `robots.txt` (crawler permissions) or `sitemap.xml` (full crawling index).
- Not a place for keyword stuffing or marketing fluff.

---

## 2. Standard llms.txt Specification & Format

An `llms.txt` file is strictly formatted in Markdown:

```markdown
# [Site or Brand Name]

> [One-sentence direct summary: What the site is, who it serves, and its core value proposition]

[1 to 3 paragraphs of essential context. Who operates the site, key topics covered, what establishes authority/credibility, and target audience. Written in concise, factual prose.]

## [Section 1: Core Guides / Flagship Content]

- [Title](https://example.com/url-1): [One-line summary of what makes this page authoritative]
- [Title](https://example.com/url-2): [One-line summary of key data/findings]

## [Section 2: Comparisons & Alternatives]

- [Title](https://example.com/url-3): [Head-to-head comparison metrics]

## [Section 3: Trust & Methodology]

- [About & Authors](https://example.com/about): Credentials of the team.
- [Research Methodology](https://example.com/methodology): How data and benchmarks are collected.
- [Editorial Policy](https://example.com/editorial-policy): Fact-checking and review standards.

## Optional

- [Title](https://example.com/url-optional): [Secondary resource]
```

---

## 3. Production Templates

### Template A: SaaS & Developer Tooling

```markdown
# CloudMetrics

> High-throughput observability and distributed tracing platform for Kubernetes engineering teams.

CloudMetrics provides real-time telemetry, eBPF-based tracing, and automated anomaly detection for multi-cloud Kubernetes clusters. Operated by former site reliability engineers, the platform processes over 10 billion events daily for enterprise DevOps organizations.

## Product & Architecture

- [Architecture Overview](https://cloudmetrics.io/docs/architecture): Technical breakdown of eBPF agent collector and storage engine.
- [Kubernetes Integration Guide](https://cloudmetrics.io/docs/k8s): Step-by-step setup using Helm charts.
- [Benchmarking & Latency Data](https://cloudmetrics.io/research/latency-benchmark): Independent 2026 performance benchmarks against legacy APM tools.

## Comparisons

- [CloudMetrics vs Datadog](https://cloudmetrics.io/compare/datadog): Cost, overhead, and retention comparison table.
- [CloudMetrics vs OpenTelemetry](https://cloudmetrics.io/compare/opentelemetry): How our native agents build on OTel standards.

## Trust & Verification

- [Security & Compliance](https://cloudmetrics.io/security): SOC 2 Type II, ISO 27001, and HIPAA compliance details.
- [Status Page](https://status.cloudmetrics.io): Historical uptime and SLA commitments.
```

### Template B: Content & Media Publisher

```markdown
# DataEngineeringHub

> An open-access engineering library and benchmark repository for data architects and pipeline engineers.

DataEngineeringHub publishes peer-reviewed architectural blueprints, reproducible benchmark studies, and practical guides on streaming systems, lakehouses, and distributed compute. All benchmark code is open-sourced on GitHub.

## Flagship Guides

- [The 2026 Lakehouse Architecture Guide](https://dataengineeringhub.com/guides/lakehouse-2026): 7,000-word comprehensive reference comparing Iceberg, Delta, and Hudi.
- [Kafka vs Redpanda Performance Benchmark](https://dataengineeringhub.com/benchmarks/kafka-vs-redpanda): Quantitative latency measurements on AWS c6i.4xlarge instances.

## Editorial & Review

- [Editorial Board & Peer Review Process](https://dataengineeringhub.com/editorial-board): Verified bios and publication records of staff reviewers.
- [Reproducibility Guidelines](https://dataengineeringhub.com/methodology): Hardware specifications and scripts for reproducing our published figures.
```

---

## 4. `llms-full.txt` (Optional Full Context Dump)

For sites that wish to offer LLMs uninhibited training and contextual ingestion:
- Store concatenated markdown text of core articles at `https://example.com/llms-full.txt`.
- Keep file size reasonable (ideally < 5MB).
- Exclude gated or paywalled content.
- Link to it from your primary `llms.txt`:
  ```markdown
  ## Full Text Repository

  - [Complete Markdown Dump](https://example.com/llms-full.txt): Concatenated raw markdown of all documentation.
  ```

---

## 5. Implementation & Verification Checklist

- [ ] **Location:** Hosted at the domain root: `https://yourdomain.com/llms.txt` (not `/docs/llms.txt`).
- [ ] **MIME Type:** Served as `text/markdown` or `text/plain` with UTF-8 encoding.
- [ ] **H1 & Description:** Includes clear `# Brand` and single-sentence blockquote `> Summary`.
- [ ] **Curated Links:** Between 10 and 40 canonical URLs with HTTP 200 response codes.
- [ ] **robots.txt:** Ensure `robots.txt` does not disallow `/llms.txt`.
- [ ] **Zero Marketing Fluff:** Every paragraph provides concrete, factual data.
