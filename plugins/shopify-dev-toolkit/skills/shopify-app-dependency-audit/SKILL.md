---
name: shopify-app-dependency-audit
description: Map Shopify theme dependencies on apps and external services before feature migration, app removal, theme upgrade, or cross-store delivery. Use to find Theme App Extension blocks, app embeds, shopify://apps references, app snippets and assets, external scripts, API endpoints, metafields, metaobjects, script loaders, tracking integrations, and likely orphaned code. Default to read-only analysis and never uninstall apps or delete code automatically.
---

# Shopify App Dependency Audit

Identify dependencies and ownership. Do not remove code, disable embeds, uninstall apps, or mutate store configuration.

## Workflow

1. Run `scripts/audit_app_dependencies.py <theme-path> --json-output <report>`.
2. Review matches in context and group them by app/service, file, dependency type, and confidence.
3. Distinguish Theme App Extension references from legacy injected snippets, native Shopify resources, analytics, consent tools, CDNs, and custom endpoints.
4. Trace each feature to required app installation, app block/embed state, metafield/metaobject contract, external API, and store configuration.
5. For migrations, label each dependency `portable`, `requires_app`, `requires_store_data`, `requires_configuration`, `reimplement`, or `unknown`.
6. Treat apparently orphaned code as a candidate only; require browser/network evidence and explicit approval before removal.
7. Produce `assets/app-dependency-report.md`.

Hand approved removals or replacements to `$shopify-code-change-guard`. Never touch live themes or app billing.
