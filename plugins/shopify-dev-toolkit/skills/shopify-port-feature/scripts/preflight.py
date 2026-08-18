#!/usr/bin/env python3
"""Read-only preflight checks for local Shopify theme feature ports."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


REQUIRED_DIRS = {"assets", "config", "layout", "sections", "snippets", "templates"}


def git_status(path: Path) -> dict:
    probe = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
    )
    if probe.returncode != 0:
        return {"is_worktree": False, "root": None, "dirty_files": []}
    status = subprocess.run(
        ["git", "-C", str(path), "status", "--porcelain", "--untracked-files=all"],
        capture_output=True,
        text=True,
        check=False,
    )
    dirty = [line[3:].strip().replace("\\", "/") for line in status.stdout.splitlines() if len(line) >= 4]
    return {"is_worktree": True, "root": probe.stdout.strip(), "dirty_files": dirty}


def inspect_theme(path_text: str) -> dict:
    path = Path(path_text).resolve()
    present = sorted(item.name for item in path.iterdir() if item.is_dir()) if path.is_dir() else []
    missing = sorted(REQUIRED_DIRS - set(present))
    return {
        "path": str(path),
        "exists": path.exists(),
        "is_directory": path.is_dir(),
        "recognizable_theme": not missing and (path / "layout" / "theme.liquid").is_file(),
        "missing_required_directories": missing,
        "has_theme_liquid": (path / "layout" / "theme.liquid").is_file(),
        "git": git_status(path) if path.is_dir() else {"is_worktree": False, "root": None, "dirty_files": []},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--target")
    args = parser.parse_args()

    source = inspect_theme(args.source)
    target = inspect_theme(args.target) if args.target else None
    errors = []
    warnings = []

    if not source["recognizable_theme"]:
        errors.append("Source is not a recognizable Shopify theme.")
    if source["git"]["dirty_files"]:
        warnings.append("Source contains pre-existing changes; preserve them and check overlap.")
    if target:
        if source["path"].casefold() == target["path"].casefold():
            errors.append("Source and target resolve to the same directory.")
        if not target["recognizable_theme"]:
            errors.append("Target is not a recognizable Shopify theme.")
        if not target["git"]["is_worktree"]:
            errors.append("Target must be inside a Git worktree before implementation.")
        if target["git"]["dirty_files"]:
            warnings.append("Target contains pre-existing changes; do not edit overlapping files.")

    result = {"ok": not errors, "source": source, "target": target, "errors": errors, "warnings": warnings}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
