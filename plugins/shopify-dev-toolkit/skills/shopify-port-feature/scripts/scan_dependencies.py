#!/usr/bin/env python3
"""Collect likely Shopify theme dependencies from seed files; output is evidence, not proof."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PATTERNS = {
    "renders": re.compile(r"{%-?\s*render\s+['\"]([^'\"]+)"),
    "assets": re.compile(r"['\"]([^'\"]+\.(?:js|css))['\"]\s*\|\s*asset_url"),
    "locale_keys": re.compile(r"['\"]([^'\"]+)['\"]\s*\|\s*t\b"),
    "metafields": re.compile(r"(?:product|variant|collection|shop)\.metafields\.([\w-]+)\.([\w-]+)"),
    "selectors": re.compile(r"(?:querySelector(?:All)?|closest|matches)\(\s*['\"]([^'\"]+)"),
    "events": re.compile(r"(?:addEventListener|dispatchEvent|CustomEvent)\(\s*['\"]([^'\"]+)"),
    "imports": re.compile(r"(?:import[^;]*?from\s*|import\s*)['\"]([^'\"]+)['\"]"),
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--theme", required=True)
    parser.add_argument("--seed", action="append", required=True, help="Theme-relative seed file; repeat as needed")
    args = parser.parse_args()
    root = Path(args.theme).resolve()
    output = {key: [] for key in PATTERNS}
    output["files"] = []
    output["missing_seeds"] = []

    for seed in args.seed:
        path = (root / seed).resolve()
        try:
            path.relative_to(root)
        except ValueError:
            output["missing_seeds"].append(seed)
            continue
        if not path.is_file():
            output["missing_seeds"].append(seed)
            continue
        output["files"].append(seed.replace("\\", "/"))
        text = path.read_text(encoding="utf-8", errors="replace")
        for key, pattern in PATTERNS.items():
            for match in pattern.findall(text):
                value = ".".join(match) if isinstance(match, tuple) else match
                output[key].append({"value": value, "evidence": seed.replace("\\", "/")})

    for key in PATTERNS:
        seen = set()
        output[key] = [item for item in output[key] if not (item["value"] in seen or seen.add(item["value"]))]
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0 if not output["missing_seeds"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
