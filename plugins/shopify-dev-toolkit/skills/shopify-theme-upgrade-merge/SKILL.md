---
name: shopify-theme-upgrade-merge
description: Compare an original old Shopify theme, its customized working copy, and a new upstream theme version to identify vendor changes, custom changes, conflicts, renamed or removed theme contracts, and safe merge candidates. Use for theme upgrades and vendor-version migrations when Codex must preserve custom features and styling without overwriting source trees, targeting a live theme, or publishing.
---

# Shopify Theme Upgrade Merge

Use three distinct local theme roots: `old-original`, `old-customized`, and `new-original`. Keep all three read-only and write only to a separate `new-customized` target approved by the user.

## Workflow

1. Verify every theme root is recognizable and resolve absolute paths.
2. Run `scripts/three_way_inventory.py --old-original <path> --old-customized <path> --new-original <path> --json-output <report>`.
3. Read `references/merge-policy.md` and classify files as vendor-only, custom-only, converged, conflict, deleted-upstream, or new-upstream.
4. Trace affected schema IDs, settings, templates, snippets, assets, locale keys, app blocks, metafields, and JavaScript lifecycle behavior.
5. Produce a phased merge manifest and require approval before creating or editing the target.
6. Apply minimal changes through `$shopify-code-change-guard`; never bulk-copy a directory over the new theme.
7. Validate with Schema, locale, App dependency, SEO, performance, Development Theme, functional, visual, accessibility, and Markets checks as relevant.

Never write to the three inputs, update a live theme, or publish. Stop when the theme versions cannot be identified or the requested target overlaps an input root.
