---
name: shopify-draft-sync
description: Safely synchronize an explicitly reviewed local Shopify theme file manifest to a numerically identified and CLI-verified unpublished theme. Use only after Development Theme testing when Codex must update an existing draft theme without publishing, touching the live theme, deleting remote files, or overwriting theme settings.
---

# Shopify Draft Sync

Use the bundled `$shopify-theme-preview-guard` executor. Do not construct a separate Shopify mutation command.

## Permanent restrictions

- Require store domain, absolute local theme path, numeric Theme ID, and reviewed JSON file manifest.
- Verify exactly one target with role `unpublished` through Shopify CLI.
- Never target a theme by name.
- Never use a live or development Theme ID.
- Never include `config/settings_data.json`, globs, absolute manifest entries, or parent traversal.
- Always use `--nodelete`; never remove remote files.
- Never publish, rename, duplicate, or delete a theme.
- Stop if the verified role is not exactly `unpublished`.

## Workflow

1. Confirm local validation and Development Theme regression results.
2. Generate a manifest containing only reviewed changed files.
3. Show store, path, Theme ID, manifest, and exact guarded action.
4. Require explicit confirmation.
5. Execute only:

```text
../shopify-theme-preview-guard/scripts/preview_guard.py update-unpublished --theme-path <path> --store <store> --theme-id <id> --files-manifest <json> --execute
```

6. Verify the returned target remains `unpublished`.
7. Produce `assets/sync-report.md` with uploaded files, omitted files, role evidence, and `Live theme unchanged`.

If the existing draft must receive `settings_data.json`, stop. This skill intentionally cannot do that.
