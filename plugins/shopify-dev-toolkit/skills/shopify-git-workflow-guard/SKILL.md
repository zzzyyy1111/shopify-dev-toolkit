---
name: shopify-git-workflow-guard
description: Protect local Shopify theme work with safe Git inspection, task-scoped branches, reviewed staging, focused commits, diff evidence, and rollback guidance. Use before or after theme changes when Codex must preserve pre-existing edits, detect unrelated files, prepare a feature branch or commit, or explain recovery. Never use destructive reset, clean, force checkout, force push, automatic push, history rewriting, or remote publication.
---

# Shopify Git Workflow Guard

Default to read-only inspection. Git authorization does not authorize Shopify upload or publication.

## Permanent restrictions

- Never run `git reset --hard`, `git clean`, force checkout, force switch, rebase, amend, filter history, or force push.
- Never discard, stash, stage, commit, push, merge, or create a branch without explicit user approval for that action.
- Never stage all files blindly. Use an approved task manifest and explicit paths.
- Preserve unrelated tracked and untracked files.
- Stop if merge conflicts, an in-progress rebase/merge, suspicious repository root, or unexpected baseline changes are found.

## Workflow

1. Run `scripts/git_inspect.py <theme-path> --json-output <report>`.
2. If no repository exists, explain the benefits and ask before `git init`; never initialize automatically.
3. Record branch, HEAD, upstream, status, staged files, unstaged files, untracked files, and repository root.
4. Propose a short task branch and commit plan. Require approval before each state-changing Git step.
5. Before staging, compare changed paths with `$shopify-code-change-guard` manifest.
6. Stage explicit reviewed paths only, show the staged diff, then require approval before committing.
7. Generate a focused commit message and record non-destructive rollback options.
8. Never push automatically; provide the command only if requested, or run it after separate approval.

Use `assets/git-report.md` for the handoff.
