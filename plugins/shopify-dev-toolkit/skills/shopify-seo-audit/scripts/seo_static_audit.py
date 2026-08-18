#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


CHECKS = {
    "TITLE": (r"<title\b|page_title", "warning", "No title output pattern found"),
    "META_DESCRIPTION": (r"name\s*=\s*['\"]description|page_description", "warning", "No meta description output pattern found"),
    "CANONICAL": (r"rel\s*=\s*['\"]canonical|canonical_url", "warning", "No canonical URL output pattern found"),
    "ROBOTS": (r"name\s*=\s*['\"]robots", "information", "No explicit robots meta pattern found"),
    "HREFLANG": (r"hreflang\s*=|localization\.available", "information", "No hreflang/localization output pattern found"),
    "JSON_LD": (r"application/ld\+json", "warning", "No JSON-LD output pattern found"),
    "PRODUCT_SCHEMA": (r"['\"]Product['\"]|schema\.org/Product", "information", "No Product schema pattern found"),
    "BREADCRUMB_SCHEMA": (r"BreadcrumbList", "information", "No BreadcrumbList schema pattern found"),
}


def main():
    p = argparse.ArgumentParser(description="Static Shopify theme SEO audit")
    p.add_argument("theme_path")
    p.add_argument("--json-output")
    args = p.parse_args()
    root = Path(args.theme_path).expanduser().resolve()
    files = [x for folder in ("layout", "sections", "snippets", "templates", "config") for x in (root / folder).rglob("*") if x.is_file() and x.suffix in {".liquid", ".json"}]
    corpus = "\n".join(x.read_text(encoding="utf-8-sig", errors="replace") for x in files)
    findings, evidence = [], {}
    for code, (pattern, level, missing) in CHECKS.items():
        matches = []
        rx = re.compile(pattern, re.I)
        for path in files:
            text = path.read_text(encoding="utf-8-sig", errors="replace")
            if rx.search(text):
                matches.append(path.relative_to(root).as_posix())
        evidence[code] = sorted(set(matches))
        if not matches:
            findings.append({"level": level, "code": code + "_NOT_FOUND", "message": missing})
    ld_count = len(re.findall(r"application/ld\+json", corpus, re.I))
    if ld_count > 8:
        findings.append({"level": "information", "code": "MANY_JSON_LD_SOURCES", "message": f"Found {ld_count} JSON-LD script patterns; verify rendered pages for duplicates"})
    if re.search(r"noindex", corpus, re.I):
        findings.append({"level": "information", "code": "NOINDEX_PRESENT", "message": "Theme contains noindex logic; verify its rendered conditions"})
    result = {"ok": True, "theme_root": str(root), "scope": "static_theme_only", "findings": findings, "evidence": evidence, "runtime_validation_required": True}
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.json_output:
        Path(args.json_output).write_text(text + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
