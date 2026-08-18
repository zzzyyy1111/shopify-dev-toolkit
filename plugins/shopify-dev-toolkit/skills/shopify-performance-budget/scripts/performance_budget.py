#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path


DEFAULTS = {"max_total_js_growth": 30720, "max_total_css_growth": 30720, "max_new_asset_bytes": 524288, "max_single_asset_bytes": 1048576}


def inventory(root):
    result = {}
    assets = root / "assets"
    for path in sorted(assets.rglob("*")) if assets.exists() else []:
        if path.is_file():
            data = path.read_bytes()
            result[path.relative_to(root).as_posix()] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "extension": path.suffix.lower()}
    return result


def totals(items):
    js = sum(v["bytes"] for k, v in items.items() if Path(k).suffix.lower() in {".js", ".mjs"})
    css = sum(v["bytes"] for k, v in items.items() if Path(k).suffix.lower() == ".css")
    return {"js": js, "css": css, "all": sum(v["bytes"] for v in items.values())}


def output(data, path=None):
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if path:
        Path(path).write_text(text + "\n", encoding="utf-8")
    print(json.dumps(data, ensure_ascii=True, indent=2))


def main():
    p = argparse.ArgumentParser(description="Snapshot and compare Shopify theme asset budgets")
    sub = p.add_subparsers(dest="action", required=True)
    s = sub.add_parser("snapshot")
    s.add_argument("--theme-path", required=True)
    s.add_argument("--output", required=True)
    c = sub.add_parser("compare")
    c.add_argument("--theme-path", required=True)
    c.add_argument("--baseline", required=True)
    c.add_argument("--budget")
    c.add_argument("--json-output")
    args = p.parse_args()
    root = Path(args.theme_path).expanduser().resolve()
    current = inventory(root)
    if args.action == "snapshot":
        output({"theme_root": str(root), "assets": current, "totals": totals(current)}, args.output)
        return
    baseline = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
    before = baseline.get("assets", {})
    budget = DEFAULTS.copy()
    if args.budget:
        budget.update(json.loads(Path(args.budget).read_text(encoding="utf-8")))
    old_total, new_total = totals(before), totals(current)
    added = sorted(current.keys() - before.keys())
    changed = sorted(k for k in current.keys() & before.keys() if current[k]["sha256"] != before[k]["sha256"])
    removed = sorted(before.keys() - current.keys())
    violations = []
    if new_total["js"] - old_total["js"] > budget["max_total_js_growth"]:
        violations.append("TOTAL_JS_GROWTH")
    if new_total["css"] - old_total["css"] > budget["max_total_css_growth"]:
        violations.append("TOTAL_CSS_GROWTH")
    for name in added:
        if current[name]["bytes"] > budget["max_new_asset_bytes"]:
            violations.append(f"NEW_ASSET_TOO_LARGE:{name}")
    for name, meta in current.items():
        if meta["bytes"] > budget["max_single_asset_bytes"]:
            violations.append(f"ASSET_TOO_LARGE:{name}")
    result = {"ok": not violations, "theme_root": str(root), "budget": budget, "before": old_total, "after": new_total, "growth": {k: new_total[k] - old_total[k] for k in new_total}, "added": added, "changed": changed, "removed": removed, "violations": violations}
    output(result, args.json_output)
    raise SystemExit(0 if result["ok"] else 2)


if __name__ == "__main__":
    main()
