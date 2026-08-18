#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


PATTERNS = {
    "metafield": re.compile(r"\b(product|variant|collection|shop|customer|article|blog|page)\.metafields\.([A-Za-z0-9_-]+)\.([A-Za-z0-9_-]+)"),
    "metaobject": re.compile(r"\bmetaobjects(?:\[['\"]([^'\"]+)['\"]\]|\.([A-Za-z0-9_-]+))"),
    "cart_attribute": re.compile(r"attributes\[['\"]([^'\"]+)['\"]\]"),
    "line_item_property": re.compile(r"properties\[['\"]([^'\"]+)['\"]\]|name\s*=\s*['\"]properties\[([^\]]+)\]"),
}


def main():
    p = argparse.ArgumentParser(description="Extract Shopify theme data contracts")
    p.add_argument("theme_path")
    p.add_argument("--json-output")
    args = p.parse_args()
    root = Path(args.theme_path).expanduser().resolve()
    contracts = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix not in {".liquid", ".json", ".js"}:
            continue
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        for kind, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                groups = [x for x in match.groups() if x]
                if kind == "metafield":
                    key = f"{groups[0]}.metafields.{groups[1]}.{groups[2]}"
                else:
                    key = groups[0]
                line = text.count("\n", 0, match.start()) + 1
                contracts.append({"kind": kind, "reference": key, "file": rel, "line": line, "expected_type": "unknown", "ownership": "unverified"})
    unique = {}
    for item in contracts:
        key = (item["kind"], item["reference"], item["file"], item["line"])
        unique[key] = item
    items = sorted(unique.values(), key=lambda x: (x["kind"], x["reference"], x["file"], x["line"]))
    result = {"ok": True, "theme_root": str(root), "contracts": items, "count": len(items), "store_data_read": False, "store_data_modified": False}
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.json_output:
        Path(args.json_output).write_text(text + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
