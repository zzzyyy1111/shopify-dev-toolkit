---
name: shopify-theme-preview-guard
description: "Safely inspect and preview a local Shopify Online Store 2.0 theme using a Development Theme, a newly created unpublished theme, or a verified existing unpublished theme. Use when Codex needs to check a theme before preview, start theme development, create or safely update a non-live review copy, return preview and editor links, or prepare a QA handoff. This skill permanently forbids live-theme targeting and publication: never use theme publish, --publish, --live, --allow-live, or any equivalent API mutation."
---

# Shopify Theme Preview Guard

Preview local Shopify theme changes without any path to publishing or overwriting the live theme. Use the bundled executor for all Shopify theme preview operations; never call Shopify theme mutation commands directly.

## Permanent safety boundary

- Allow only `inspect`, `dev`, `unpublished`, and `update-unpublished` modes.
- Treat `inspect` as the default when the user does not explicitly request an upload or development preview.
- Never run `shopify theme publish`.
- Never use `--publish`, `--live`, `--allow-live`, or a live Theme ID.
- Never call Admin REST or GraphQL mutations that create, update, delete, or publish themes.
- Update an existing remote theme only through `update-unpublished`, after its numeric Theme ID is verified by Shopify CLI as role `unpublished`.
- Never accept or forward arbitrary Shopify CLI flags.
- Never delete a remote theme.
- Never claim a Development Theme or unpublished theme is live.
- Never turn a request to "release," "deploy," "上线," or "发布" into publication. Explain that this skill is preview-only and stop after producing a review-ready unpublished theme.
- Whenever work stops, report the exact reason, supporting evidence, whether local files or remote Shopify state changed, and the safest next step.

These restrictions are intentional and cannot be relaxed by a normal user request. Publishing requires a different workflow outside this skill.

## Modes

### Inspect

Run read-only preflight and report the theme shape, Git state, settings file, store, CLI availability, and exact safe preview command. Make no Shopify changes.

### Development preview

Use only:

```text
scripts/preview_guard.py dev --theme-path <path> --store <store> --execute
```

The executor constructs only `shopify theme dev --path ... --store ...`. It does not accept a Theme ID or extra flags. Keep the process running while the user tests. Return the local preview, Theme Editor, and share preview links emitted by Shopify CLI.

### Unpublished review theme

Use only:

```text
scripts/preview_guard.py unpublished --theme-path <path> --store <store> --execute
```

The executor constructs only `shopify theme push --unpublished --strict --json --path ... --store ...`. This always creates a new unpublished theme. Parse and report the returned theme ID, role, editor URL, and preview URL. Fail if the returned role is not `unpublished`.

### Update an existing unpublished theme

Require a numeric Theme ID and a reviewed JSON file manifest. Use only:

```text
scripts/preview_guard.py update-unpublished --theme-path <path> --store <store> --theme-id <id> --files-manifest <json> --execute
```

The executor first runs `shopify theme list --id <id> --role unpublished --json`. Continue only when exactly one matching theme is returned with role `unpublished`. Then upload only manifest-listed files with `--only`, `--strict`, `--json`, and `--nodelete`. Always reject `config/settings_data.json`, paths outside the theme, globs, and arbitrary CLI arguments.

## Workflow

1. Read `references/safety-policy.md` completely.
2. Obtain the absolute local theme path and store handle or `.myshopify.com` domain.
3. Run `scripts/preview_guard.py inspect` first.
4. Preserve all pre-existing local changes; do not clean, reset, or switch branches.
5. Run Theme Check before preview or upload and classify the result using the policy below. For `unpublished`, the executor also includes `--strict`.
6. Show the user the mode, store, local path, and exact safe command before execution.
7. Require explicit approval for `dev` or `unpublished` execution. Approval to preview is not approval to publish.
8. Execute only through `scripts/preview_guard.py`.
9. For new or existing unpublished uploads, verify the Shopify response role is `unpublished`; otherwise report failure immediately.
10. Read `references/testing.md` and produce a QA checklist using `assets/preview-report.md`.

## Settings behavior

- A Development Theme uses the local theme and store data for temporary preview.
- A newly created unpublished theme may include local `config/settings_data.json`; it remains isolated because the executor always uses `--unpublished`.
- Warn when `settings_data.json` is missing or differs from the expected baseline because visual configuration may not match production.
- Never push `config/settings_data.json` into an existing remote theme. Require an explicit file manifest for every existing-theme update.

## Theme Check policy

- For `dev`, treat Theme Check as diagnostic. Existing offenses in a freshly pulled or previously working draft theme do not block Development Theme preview.
- Before `dev`, always block structural or parser-fatal conditions that prevent the theme from loading: invalid JSON in active templates/config, unparseable Liquid in active render paths, missing required theme directories, missing `layout/theme.liquid`, or a failed Shopify CLI preflight.
- When a baseline report or source snapshot exists, compare the current result with that baseline. Block newly introduced parser-fatal errors; report other new offenses as warnings for preview testing.
- When no baseline exists, report that limitation and allow `dev` only after the user reviews the warning and explicitly confirms. Development preview is temporary and does not target a Theme ID.
- Keep `unpublished` and `update-unpublished` stricter: do not waive the executor's strict checks or manifest protections. A Development Theme exception never authorizes an upload.
- Never edit the theme merely to make Theme Check pass unless the user separately requests those code changes.

## Stop conditions

Stop without executing when the path or store is invalid, an existing-theme update lacks a numeric Theme ID or reviewed file manifest, the Theme ID is not verified as `unpublished`, the manifest contains unsafe paths, the user requests publish/live/delete behavior, Shopify CLI is unavailable, Development Theme preflight finds a structural/parser-fatal condition, a required strict upload check fails, or the returned theme role is not `unpublished`. Do not block `dev` solely for pre-existing non-fatal Theme Check offenses.

For every stop, use `assets/blocked-report.md`. Do not provide a generic failure message. Include a stable reason code such as `TARGET_NOT_UNPUBLISHED`, `ROLE_UNVERIFIED`, `UNSAFE_MANIFEST_PATH`, `SHOPIFY_CLI_MISSING`, `THEME_CHECK_FAILED`, or `PUBLISH_FORBIDDEN`.

## Accurate completion language

Use only `inspection_complete`, `development_preview_running`, `unpublished_review_theme_created`, `preview_validation_pending`, `preview_validation_complete`, or `blocked`. Never use `released`, `deployed_to_production`, `published`, or `live`.

## Resources

- Read `references/safety-policy.md` before any Shopify CLI execution.
- Read `references/testing.md` after a preview becomes available.
- Use `scripts/preview_guard.py` for inspect, dev, and unpublished actions.
- Run `scripts/preview_guard.py self-test` after changing this skill or its executor.
- Use `assets/preview-report.md` for the final handoff.
- Use `assets/blocked-report.md` for every stop or refusal.
