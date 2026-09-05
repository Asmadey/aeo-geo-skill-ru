#!/usr/bin/env python3
"""
llms_txt_generator.py — llms.txt & llms-full.txt Builder and Validator.

Creates, structures, and validates standard llms.txt files according to the
AI-readability specification (https://llmstxt.org).
Works 100% offline using Python standard library only.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse


TEMPLATES = {
    "saas": {
        "title": "CloudMetrics",
        "description": "High-throughput observability and distributed tracing platform for cloud-native engineering teams.",
        "context": "CloudMetrics provides real-time telemetry, eBPF-based tracing, and automated anomaly detection for multi-cloud Kubernetes clusters. Operated by site reliability engineers, the platform processes over 10 billion events daily.",
        "sections": {
            "Product & Architecture": [
                ("Architecture Overview", "https://example.com/docs/architecture", "Technical breakdown of eBPF agent collector and storage engine."),
                ("Kubernetes Integration", "https://example.com/docs/k8s", "Step-by-step setup using Helm charts."),
                ("Latency Benchmarks", "https://example.com/research/benchmarks", "Independent 2026 performance benchmarks against legacy APM tools."),
            ],
            "Comparisons": [
                ("CloudMetrics vs Datadog", "https://example.com/compare/datadog", "Cost, overhead, and retention comparison table."),
                ("CloudMetrics vs OpenTelemetry", "https://example.com/compare/opentelemetry", "Native agents built on OTel standards."),
            ],
            "Trust & Verification": [
                ("Security & Compliance", "https://example.com/security", "SOC 2 Type II, ISO 27001, and HIPAA compliance."),
                ("Status & Uptime", "https://status.example.com", "Historical uptime and SLA commitments."),
            ],
        },
    },
    "content_site": {
        "title": "TechGuideHub",
        "description": "An open-access engineering library and benchmark repository for software architects and developers.",
        "context": "TechGuideHub publishes peer-reviewed architectural blueprints, reproducible benchmark studies, and practical guides on distributed systems and AI applications. Written by practicing engineers and updated weekly.",
        "sections": {
            "Flagship Guides": [
                ("Vector Search Architecture Guide", "https://example.com/guides/vector-search", "Comprehensive 6,000-word reference on embeddings, indexing, and vector DBs."),
                ("Modern Postgres Optimization", "https://example.com/guides/postgres-tuning", "Performance tuning patterns and index strategies."),
            ],
            "Comparisons & Benchmarks": [
                ("Vector Database Benchmark 2026", "https://example.com/benchmarks/vector-dbs", "Quantitative latency and recall measurements."),
            ],
            "Editorial Standards": [
                ("Review Methodology", "https://example.com/methodology", "How benchmarks and tests are run."),
                ("Editorial Board", "https://example.com/about/editorial-board", "Credentials of staff reviewers and contributors."),
            ],
        },
    },
}


class LLMsTxtManager:
    """Builder and validator for llms.txt standard files."""

    def __init__(self):
        pass

    def build_from_template(self, template_name: str, site_name: Optional[str] = None, site_url: Optional[str] = None) -> str:
        tmpl = TEMPLATES.get(template_name, TEMPLATES["saas"])
        title = site_name or tmpl["title"]
        desc = tmpl["description"]
        ctx = tmpl["context"]

        lines = [
            f"# {title}",
            "",
            f"> {desc}",
            "",
            ctx,
            "",
        ]

        for sec_name, links in tmpl["sections"].items():
            lines.append(f"## {sec_name}")
            lines.append("")
            for text, url, summary in links:
                if site_url:
                    parsed = urlparse(url)
                    url = f"{site_url.rstrip('/')}{parsed.path}"
                lines.append(f"- [{text}]({url}): {summary}")
            lines.append("")

        lines.extend([
            "## Optional",
            "",
            f"- [Full Content Dump]({site_url.rstrip('/') if site_url else 'https://example.com'}/llms-full.txt): Complete raw markdown archive for AI context.",
            "",
        ])

        return "\n".join(lines)

    def validate(self, file_path: Path) -> Dict[str, Any]:
        """Validate an llms.txt file against the standard specification."""
        if not file_path.exists():
            return {"valid": False, "errors": [f"File not found: {file_path}"], "warnings": []}

        content = file_path.read_text(encoding="utf-8")
        lines = [line.strip() for line in content.splitlines()]

        errors = []
        warnings = []

        # 1. Check for H1 at start
        has_h1 = any(line.startswith("# ") for line in lines[:5])
        if not has_h1:
            errors.append("Missing H1 site title (must start with '# Site Name')")

        # 2. Check for blockquote description
        has_blockquote = any(line.startswith("> ") for line in lines[:10])
        if not has_blockquote:
            errors.append("Missing one-sentence blockquote description (must start with '> ')")

        # 3. Check for sections (H2)
        h2_sections = [line[3:].strip() for line in lines if line.startswith("## ")]
        if len(h2_sections) < 2:
            warnings.append(f"Found only {len(h2_sections)} H2 section(s); recommended is 3-6 sections.")

        # 4. Check for links
        link_pattern = re.compile(r"^-\s*\[(.*?)\]\((https?://.*?)\):\s*(.+)$")
        links_found = 0
        for line in lines:
            if line.startswith("- ["):
                match = link_pattern.match(line)
                if match:
                    links_found += 1
                else:
                    warnings.append(f"Link line does not strictly match '- [Title](URL): Description': {line[:60]}...")

        if links_found < 3:
            errors.append(f"Too few curated links ({links_found} found, minimum recommended is 5+).")

        word_count = len(content.split())
        if word_count < 80:
            warnings.append(f"File is very short ({word_count} words); recommended length is 150-1000 words.")

        return {
            "valid": len(errors) == 0,
            "h1_present": has_h1,
            "description_present": has_blockquote,
            "sections_count": len(h2_sections),
            "links_count": links_found,
            "word_count": word_count,
            "errors": errors,
            "warnings": warnings,
        }

    def generate_full_dump(self, input_dir: Path, output_file: Path, extensions: List[str] = [".md"]):
        """Concatenate markdown files into llms-full.txt."""
        files = []
        for ext in extensions:
            files.extend(list(input_dir.glob(f"**/*{ext}")))

        collected = []
        for f in sorted(files):
            if f.name.startswith(".") or "node_modules" in str(f) or "llms" in f.name:
                continue
            try:
                txt = f.read_text(encoding="utf-8")
                collected.append(f"<!-- FILE: {f.name} -->\n\n{txt}\n\n---\n")
            except Exception as e:
                print(f"Skipping {f}: {e}")

        full_content = "\n".join(collected)
        output_file.write_text(full_content, encoding="utf-8")
        return len(files), len(full_content.split())


def main():
    parser = argparse.ArgumentParser(description="llms.txt & llms-full.txt Builder and Validator")
    subparsers = parser.add_subparsers(dest="command")

    # Command: generate
    gen_parser = subparsers.add_parser("generate", help="Generate a standard llms.txt")
    gen_parser.add_argument("--template", choices=["saas", "content_site"], default="saas", help="Starting template")
    gen_parser.add_argument("--name", help="Site / Brand name")
    gen_parser.add_argument("--url", help="Base site URL (e.g. https://example.com)")
    gen_parser.add_argument("--output", default="llms.txt", help="Output file path (default: llms.txt)")

    # Command: validate
    val_parser = subparsers.add_parser("validate", help="Validate an existing llms.txt file")
    val_parser.add_argument("--file", required=True, help="Path to llms.txt to validate")

    # Command: dump
    dump_parser = subparsers.add_parser("dump", help="Generate llms-full.txt by concatenating docs")
    dump_parser.add_argument("--input-dir", required=True, help="Directory with markdown docs")
    dump_parser.add_argument("--output", default="llms-full.txt", help="Output file path")

    args = parser.parse_args()

    manager = LLMsTxtManager()

    if args.command == "generate":
        result = manager.build_from_template(template_name=args.template, site_name=args.name, site_url=args.url)
        out_p = Path(args.output)
        out_p.write_text(result, encoding="utf-8")
        print(f"✅ Generated {out_p} using '{args.template}' template ({len(result.split())} words).")
        return

    if args.command == "validate":
        report = manager.validate(Path(args.file))
        print(f"=== llms.txt Validation Report: {args.file} ===")
        print(f"Status: {'🟢 VALID' if report['valid'] else '🔴 INVALID'}")
        print(f"Word count: {report['word_count']} words")
        print(f"Curated links: {report['links_count']}")
        print(f"Sections: {report['sections_count']}")
        if report["errors"]:
            print("\nErrors:")
            for err in report["errors"]:
                print(f"  ❌ {err}")
        if report["warnings"]:
            print("\nWarnings:")
            for warn in report["warnings"]:
                print(f"  ⚠️ {warn}")
        sys.exit(0 if report["valid"] else 1)

    if args.command == "dump":
        in_p = Path(args.input_dir)
        out_p = Path(args.output)
        count, words = manager.generate_full_dump(in_p, out_p)
        print(f"✅ Generated {out_p}: merged {count} files ({words} words).")
        return

    # No args -> demo sample
    print("Usage: python3 scripts/llms_txt_generator.py [generate|validate|dump] --help")
    print("\nSample generated llms.txt preview:")
    print("--------------------------------------------------")
    print(manager.build_from_template("saas", site_name="AcmePlatform", site_url="https://acme.io"))


if __name__ == "__main__":
    main()
