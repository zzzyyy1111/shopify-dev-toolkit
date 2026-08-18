---
name: shopify-locale-audit
description: Audit Shopify theme locale JSON files and translation usage across Liquid, sections, snippets, templates, and schema labels. Use to detect malformed locale JSON, missing or extra keys, placeholder mismatches, untranslated fallback values, and keys referenced by theme code but absent from the default locale before cross-border theme delivery.
---

# Shopify Locale Audit

Default to read-only reporting. Preserve human translations and never overwrite a locale automatically.

## Workflow

1. Identify the default locale from `*.default.json`; stop if ambiguous.
2. Run `scripts/audit_locales.py <theme-path> --json-output <report-path>`.
3. Report malformed files, missing keys, extra keys, placeholder mismatches, and code references missing from the default locale.
4. Separate storefront translations from `.schema.json` editor translations.
5. Preserve placeholders such as `{{ count }}`, `%{name}`, HTML fragments, and interpolation keys.
6. Propose additions without replacing existing human translations.
7. Require explicit approval and a language list before writing translations.
8. Re-run the audit after approved changes and recommend Markets/browser testing.

## Safety

- Never translate product, collection, metafield, or metaobject content; those are store data.
- Never infer legal, tax, shipping, warranty, or compliance wording.
- Never delete extra keys automatically; they may support app or market-specific code.
