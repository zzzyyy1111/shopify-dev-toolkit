---
name: shopify-performance-budget
description: Measure and enforce local Shopify theme asset-size and code-growth budgets before preview or draft sync. Use after adding sections, JavaScript, CSS, images, fonts, libraries, app integrations, or migrated features to snapshot assets, compare baselines, detect unexpectedly large or duplicated resources, and identify performance risk. Default to reporting; never optimize or remove functionality automatically.
---

# Shopify Performance Budget

Measure before optimizing. Preserve functionality, styling, analytics, consent, accessibility, and app behavior.

## Workflow

1. Create a baseline with `scripts/performance_budget.py snapshot --theme-path <path> --output <json>` before changes, or use a trusted previous snapshot.
2. After changes, run `compare --theme-path <path> --baseline <json> --budget <json> --json-output <report>`.
3. Read `references/runtime-performance.md` and, when a Development Theme is available, record representative runtime evidence for home, product, collection, and cart.
4. Separate theme-owned resources from Shopify CDN, apps, consent, analytics, and dynamic data.
5. Report asset growth, new large files, total JS/CSS growth, image/font additions, duplicated names/hashes, and runtime risks.
6. Require explicit approval before optimization. Explain functional and visual risks for each proposal.
7. Re-run functional and visual regression after any approved optimization.

Do not remove scripts, defer execution, change image loading, alter fonts, or rewrite Liquid merely to satisfy a budget without user approval.
