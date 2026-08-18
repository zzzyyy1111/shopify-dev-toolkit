#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path


def root_path(value):
    root = Path(value).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"Theme path is not a directory: {root}")
    return root


def hashes(root):
    result = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        rel = path.relative_to(root).as_posix()
        result[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def read_manifest(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    items = data.get("files", []) if isinstance(data, dict) else data
    if not isinstance(items, list) or not all(isinstance(x, str) for x in items):
        raise SystemExit("Manifest must be a JSON array or an object with a string files array")
    clean = set()
    for item in items:
        normalized = Path(item.replace("\\", "/"))
        if normalized.is_absolute() or ".." in normalized.parts or any(c in item for c in "*?[]"):
            raise SystemExit(f"Unsafe manifest path: {item}")
        clean.add(normalized.as_posix())
    return clean


def write(data, path=None):
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if path:
        Path(path).write_text(text + "\n", encoding="utf-8")
    print(text)


def main():
    parser = argparse.ArgumentParser(description="Constrain local Shopify theme edits to an approved manifest")
    sub = parser.add_subparsers(dest="action", required=True)
    snap = sub.add_parser("snapshot")
    snap.add_argument("--theme-path", required=True)
    snap.add_argument("--output", required=True)
    verify = sub.add_parser("verify")
    verify.add_argument("--theme-path", required=True)
    verify.add_argument("--snapshot", required=True)
    verify.add_argument("--manifest", required=True)
    verify.add_argument("--json-output")
    args = parser.parse_args()
    root = root_path(args.theme_path)

    if args.action == "snapshot":
        write({"theme_root": str(root), "files": hashes(root)}, args.output)
        return

    baseline = json.loads(Path(args.snapshot).read_text(encoding="utf-8"))
    if Path(baseline["theme_root"]).resolve() != root:
        raise SystemExit("Snapshot theme root does not match the requested theme")
    before = baseline.get("files", {})
    after = hashes(root)
    changed = sorted(k for k in before.keys() & after.keys() if before[k] != after[k])
    added = sorted(after.keys() - before.keys())
    deleted = sorted(before.keys() - after.keys())
    touched = set(changed + added + deleted)
    allowed = read_manifest(args.manifest)
    outside = sorted(touched - allowed)
    result = {
        "ok": not outside,
        "changed": changed,
        "added": added,
        "deleted": deleted,
        "outside_manifest": outside,
        "approved_but_unchanged": sorted(allowed - touched),
    }
    write(result, args.json_output)
    raise SystemExit(0 if result["ok"] else 2)


if __name__ == "__main__":
    main()
