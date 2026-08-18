#!/usr/bin/env python3
"""Verify that target Git changes stay inside an approved migration manifest."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def git_paths(target: Path, baseline: str) -> list[str]:
    commands = [
        ["git", "-C", str(target), "diff", "--name-only", baseline, "--"],
        ["git", "-C", str(target), "ls-files", "--others", "--exclude-standard"],
    ]
    paths = set()
    for command in commands:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "Git inspection failed")
        paths.update(line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip())
    return sorted(paths)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    parser.add_argument("--manifest", required=True)
    args = parser.parse_args()

    target = Path(args.target).resolve()
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    errors = []
    if not manifest.get("approved"):
        errors.append("Manifest is not approved.")

    allowed = {p.replace("\\", "/") for p in manifest.get("allowed_create", []) + manifest.get("allowed_modify", [])}
    protected = {p.replace("\\", "/") for p in manifest.get("protected_files", [])}
    baseline = manifest.get("baseline_ref") or "HEAD"
    try:
        changed = git_paths(target, baseline)
    except RuntimeError as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, indent=2))
        return 2

    unexpected = sorted(set(changed) - allowed)
    protected_changed = sorted(set(changed) & protected)
    if unexpected:
        errors.append("Changes exceed the manifest boundary.")
    if protected_changed:
        errors.append("Protected files changed.")

    invalid_json = []
    for rel in changed:
        path = target / rel
        if path.is_file() and path.suffix.lower() == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                invalid_json.append(rel)
    if invalid_json:
        errors.append("Changed JSON files are invalid.")

    result = {
        "ok": not errors,
        "baseline": baseline,
        "changed_files": changed,
        "unexpected_files": unexpected,
        "protected_files_changed": protected_changed,
        "invalid_json": invalid_json,
        "errors": errors,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
