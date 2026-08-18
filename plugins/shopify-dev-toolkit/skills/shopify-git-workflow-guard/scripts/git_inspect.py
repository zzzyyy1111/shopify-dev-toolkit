#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path


def git(path, *args):
    result = subprocess.run(["git", "-C", str(path), *args], text=True, capture_output=True, encoding="utf-8", errors="replace")
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def main():
    p = argparse.ArgumentParser(description="Read-only Git inspection for a Shopify theme")
    p.add_argument("theme_path")
    p.add_argument("--json-output")
    args = p.parse_args()
    theme = Path(args.theme_path).expanduser().resolve()
    code, repo, error = git(theme, "rev-parse", "--show-toplevel")
    if code:
        result = {"ok": True, "theme_path": str(theme), "is_worktree": False, "writes_performed": False, "message": error or "Not a Git worktree"}
    else:
        repo_path = Path(repo).resolve()
        _, branch, _ = git(theme, "branch", "--show-current")
        _, head, _ = git(theme, "rev-parse", "HEAD")
        upstream_code, upstream, _ = git(theme, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
        _, status, _ = git(theme, "status", "--porcelain=v1", "--untracked-files=all")
        _, staged, _ = git(theme, "diff", "--cached", "--name-only")
        _, unstaged, _ = git(theme, "diff", "--name-only")
        _, untracked, _ = git(theme, "ls-files", "--others", "--exclude-standard")
        state_files = [name for name in ("MERGE_HEAD", "REBASE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD") if (repo_path / ".git" / name).exists()]
        result = {
            "ok": not state_files,
            "theme_path": str(theme),
            "is_worktree": True,
            "repository_root": str(repo_path),
            "branch": branch,
            "head": head,
            "upstream": upstream if upstream_code == 0 else None,
            "status_porcelain": status.splitlines() if status else [],
            "staged": staged.splitlines() if staged else [],
            "unstaged": unstaged.splitlines() if unstaged else [],
            "untracked": untracked.splitlines() if untracked else [],
            "in_progress_states": state_files,
            "writes_performed": False,
        }
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.json_output:
        Path(args.json_output).write_text(text + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=True, indent=2))
    raise SystemExit(0 if result["ok"] else 2)


if __name__ == "__main__":
    main()
