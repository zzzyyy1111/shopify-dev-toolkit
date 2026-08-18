---
name: shopify-schema-validator
description: Validate Shopify Online Store 2.0 section schemas and JSON templates before Development Theme preview or draft upload. Use to find malformed JSON, missing parent templates or sections, unknown block types, duplicate setting IDs, invalid defaults, range values outside min/max, invalid select values, and template settings that no longer match Liquid schema.
---

# Shopify Schema Validator

Run read-only validation. Do not modify theme files unless the user separately approves a proposed fix.

## Workflow

1. Resolve the absolute local theme path and confirm required theme directories.
2. Run `scripts/validate_schema.py <theme-path> --json-output <report-path>`.
3. Run Shopify Theme Check when available and keep its findings separate from deterministic schema findings.
4. Classify findings as `fatal`, `upload_blocking`, `warning`, or `information`.
5. Report the exact file, JSON path or schema ID, current value, allowed value, and smallest repair options.
6. Require approval before editing. Explain behavior impact when changing values or editor ranges.
7. Re-run validation after approved edits.

## Rules

- Do not silently coerce values.
- Treat context-template parent errors as potentially cascading from an invalid parent template.
- Prefer correcting a stale template instance when the schema is internally coherent.
- Change a section schema only when the intended editor contract is confirmed; schema changes affect every template instance.
- Hand off successful themes to `$shopify-theme-preview-guard` for remote Development Theme validation.
