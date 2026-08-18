#!/usr/bin/env python3
"""Create or verify a SHA-256 snapshot without modifying a theme."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


IGNORED_PARTS = {".git", "node_modules", ".shopify"}


def hashes(root: Path) -> dict[str, str]:
    result = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in IGNORED_PARTS for part in path.parts):
            continue
        rel = path.relative_to(root).as_posix()
        result[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["create", "verify"])
    parser.add_argument("--theme", required=True)
    parser.add_argument("--snapshot", required=True)
    args = parser.parse_args()

    theme = Path(args.theme).resolve()
    snapshot = Path(args.snapshot).resolve()
    current = hashes(theme)

    if args.action == "create":
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        snapshot.write_text(json.dumps({"theme": str(theme), "files": current}, indent=2), encoding="utf-8")
        print(json.dumps({"ok": True, "file_count": len(current), "snapshot": str(snapshot)}, indent=2))
        return 0

    recorded = json.loads(snapshot.read_text(encoding="utf-8"))
    before = recorded.get("files", {})
    changed = sorted(path for path in set(before) | set(current) if before.get(path) != current.get(path))
    print(json.dumps({"ok": not changed, "changed_files": changed}, indent=2))
    return 0 if not changed else 2


if __name__ == "__main__":
    raise SystemExit(main())
