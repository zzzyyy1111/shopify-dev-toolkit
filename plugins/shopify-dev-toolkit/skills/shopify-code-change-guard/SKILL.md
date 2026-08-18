---
name: shopify-code-change-guard
description: Safely plan, constrain, implement, review, and roll back local Shopify Online Store 2.0 theme code changes. Use for Liquid, JSON templates, sections, snippets, CSS, JavaScript, locale, and theme configuration edits when Codex must preserve existing functionality and styling, restrict edits to an approved file manifest, show diffs, and verify the result before preview or upload.
---

# Shopify Code Change Guard

Modify only a local theme. Never use this skill to mutate Shopify remotely.

## Safety boundary

- Default to analysis-only until the user approves the change plan.
- Resolve the absolute theme root and reject paths outside it.
- Preserve existing dirty files. Never reset, clean, checkout, stash, or overwrite unrelated work.
- Create an approved manifest containing only files required by the task.
- Treat `config/settings_data.json`, layout files, global assets, cart logic, pricing, analytics, app code, and locale files as high-impact.
- Require separate confirmation before changing any high-impact file not named in the original request.
- Never perform broad formatting, dependency upgrades, or opportunistic cleanup.
- Stop when the required fix expands beyond the approved manifest.

## Workflow

1. Inspect the theme structure and relevant code paths.
2. Record the pre-change hashes with `scripts/change_guard.py snapshot`.
3. Produce a plan listing files, behavior, visual impact, dependencies, and rollback approach.
4. Obtain explicit approval before editing.
5. Edit only approved files using minimal patches.
6. Run `scripts/change_guard.py verify` against the snapshot and manifest.
7. Validate changed JSON, Liquid structure, CSS/JS syntax where tools exist, and Theme Check.
8. Show the diff and identify functional or visual behavior that still needs browser testing.
9. Hand off to `$shopify-theme-preview-guard`; never upload or publish from this skill.

## Stop report

Report the exact reason, files changed, files untouched, verification evidence, and safest next step. Use `SCOPE_EXPANDED`, `UNAPPROVED_HIGH_IMPACT_FILE`, `PATH_OUTSIDE_THEME`, `BASELINE_CHANGED`, or `VALIDATION_FAILED` where applicable.
