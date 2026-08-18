#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path


def root(value):
    path = Path(value).expanduser().resolve()
    if not path.is_dir() or not (path / "layout" / "theme.liquid").is_file():
        raise SystemExit(f"Not a recognizable Shopify theme: {path}")
    return path


def inventory(base):
    out = {}
    for path in sorted(base.rglob("*")):
        if path.is_file() and ".git" not in path.parts:
            out[path.relative_to(base).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return out


def classify(a, b, c):
    if a == b == c:
        return "unchanged"
    if a == b and c != a:
        return "vendor-only"
    if a == c and b != a:
        return "custom-only"
    if b == c and a != b:
        return "converged"
    if a is None and b is not None and c is None:
        return "custom-only"
    if a is None and c is not None and b is None:
        return "new-upstream"
    if a is not None and b is not None and c is None:
        return "deleted-upstream" if a == b else "conflict"
    return "conflict"


def main():
    p = argparse.ArgumentParser(description="Three-way Shopify theme inventory")
    p.add_argument("--old-original", required=True)
    p.add_argument("--old-customized", required=True)
    p.add_argument("--new-original", required=True)
    p.add_argument("--json-output")
    args = p.parse_args()
    roots = [root(args.old_original), root(args.old_customized), root(args.new_original)]
    if len(set(roots)) != 3:
        raise SystemExit("All three input roots must be distinct")
    old, custom, new = [inventory(x) for x in roots]
    files = []
    for name in sorted(set(old) | set(custom) | set(new)):
        files.append({"file": name, "classification": classify(old.get(name), custom.get(name), new.get(name)), "old_original": old.get(name), "old_customized": custom.get(name), "new_original": new.get(name)})
    counts = {}
    for item in files:
        counts[item["classification"]] = counts.get(item["classification"], 0) + 1
    result = {"ok": True, "roots": {"old_original": str(roots[0]), "old_customized": str(roots[1]), "new_original": str(roots[2])}, "counts": counts, "files": files, "writes_performed": False}
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.json_output:
        Path(args.json_output).write_text(text + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
