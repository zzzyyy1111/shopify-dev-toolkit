#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse


APP_BLOCK = re.compile(r"shopify://apps/[^\"'\s}]+", re.I)
URL = re.compile(r"https?://[^\"'\s<>]+", re.I)
DATA_REF = re.compile(r"(?:product|variant|shop|customer|collection)\.metafields\.([\w.-]+)|metaobjects\[?['\"]?([\w.-]+)", re.I)
NATIVE_DOMAINS = {"shopify.com", "myshopify.com", "shopifycdn.com", "cdn.shopify.com"}


def main():
    p = argparse.ArgumentParser(description="Audit app and external dependencies in a Shopify theme")
    p.add_argument("theme_path")
    p.add_argument("--json-output")
    args = p.parse_args()
    root = Path(args.theme_path).expanduser().resolve()
    app_blocks, domains, data_refs, suspicious_files = [], {}, [], []
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        rel = path.relative_to(root).as_posix()
        if any(word in path.name.lower() for word in ("app", "review", "pixel", "tracking", "wishlist", "subscription")):
            suspicious_files.append(rel)
        if path.suffix not in {".liquid", ".json", ".js", ".css"}:
            continue
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        for value in APP_BLOCK.findall(text):
            app_blocks.append({"file": rel, "reference": value})
        for value in URL.findall(text):
            host = (urlparse(value.rstrip("),.;")).hostname or "").lower()
            if host and not any(host == d or host.endswith("." + d) for d in NATIVE_DOMAINS):
                domains.setdefault(host, set()).add(rel)
        for match in DATA_REF.finditer(text):
            data_refs.append({"file": rel, "reference": next(x for x in match.groups() if x)})
    result = {
        "ok": True,
        "theme_root": str(root),
        "app_blocks": app_blocks,
        "external_domains": {k: sorted(v) for k, v in sorted(domains.items())},
        "metafield_metaobject_references": data_refs,
        "candidate_app_files": sorted(set(suspicious_files)),
        "removal_safe": False,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.json_output:
        Path(args.json_output).write_text(text + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
