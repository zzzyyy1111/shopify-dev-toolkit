---
name: shopify-data-contract-audit
description: Extract and compare Shopify theme data contracts for metafields, metaobjects, product and variant fields, cart attributes and line-item properties, section settings, and app-owned data. Use before cross-store migration, theme upgrade, feature delivery, or app replacement to identify required namespaces, keys, handles, expected types, ownership, fallback behavior, and missing target-store definitions without reading or mutating sensitive live content.
---

# Shopify Data Contract Audit

Default to local static analysis. Definitions and content are different: never create definitions, copy values, or mutate store data without a separate authorized workflow.

## Workflow

1. Run `scripts/extract_data_contracts.py <theme-path> --json-output <report>`.
2. Review matches in context and remove false positives.
3. Classify each contract by owner, resource, namespace/key or handle, expected type when known, required/optional state, fallback, and consuming files.
4. If source and target definition exports are provided, compare structure without exposing values.
5. Mark contracts as compatible, missing-definition, type-mismatch, app-owned, content-required, fallback-available, or unknown.
6. Produce `assets/data-contract-report.md` for the merchant or developer.

Never infer types from names alone, expose customer data, or claim a feature is portable until app and data requirements are both verified.
