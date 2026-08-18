# Preview-only safety policy

## Allowed remote effects

Only two effects are permitted:

1. Create or refresh the caller's Shopify Development Theme through `shopify theme dev` without specifying a Theme ID.
2. Create a brand-new unpublished theme through `shopify theme push --unpublished`.
3. Update an existing theme only after `shopify theme list --id <id> --role unpublished --json` verifies its role, and only for files named in a reviewed manifest.

An existing Theme ID may be used only by the fixed `update-unpublished` workflow after role verification.

## Permanently forbidden

- `shopify theme publish`
- `shopify theme push --publish`
- `shopify theme push --live`
- `shopify theme push --allow-live`
- Any command or API request that sets a theme role to `main` or `live`
- Updating a theme by name, or updating a Theme ID without first verifying role `unpublished`
- Deleting, renaming, or duplicating remote themes
- Admin API theme mutations
- Passing user-supplied extra arguments to Shopify CLI
- Uploading `config/settings_data.json` to an existing theme
- Using globs, parent traversal, absolute paths, or files outside the local theme in an update manifest

If a user asks for one of these, explain that the installed skill is intentionally incapable of doing it. Do not propose a bypass inside the same task.

## Required confirmation

Before `dev` or `unpublished`, show the store identifier, absolute local path, mode, exact generated command, and a statement that the live theme cannot be changed by this executor. Require explicit confirmation after showing this information.

## Local safety

- Preserve dirty files and user changes.
- Do not reset, checkout, clean, stash, or commit without a separate explicit request.
- Run inspection before execution.
- Warn when the local theme is not in Git, but allow preview if the user confirms.
- Run Theme Check when available. For Development Theme preview, use it as a baseline-aware diagnostic: preserve and report pre-existing offenses, block newly introduced parser-fatal errors, and always block structural failures that prevent theme loading.
- If no baseline exists, allow `dev` only after reporting the limitation and receiving explicit confirmation. Do not treat the absence of Git as proof that files are safe or unsafe.
- Do not block `dev` solely because a freshly pulled or previously working draft theme contains historical translation mismatches, performance checks, undefined-object warnings, or other non-fatal offenses.
- Keep unpublished creation and existing-draft updates strict. The Development Theme exception never applies to an upload.

## Result verification

For new or existing unpublished uploads, require JSON output and verify `theme.id`, `theme.role == unpublished`, `theme.preview_url`, and the editor URL when returned. Before an existing-theme update, verify exactly one theme is returned by `theme list --id <id> --role unpublished --json`. If role verification fails, label the action `blocked` and do not run another Shopify mutation.
