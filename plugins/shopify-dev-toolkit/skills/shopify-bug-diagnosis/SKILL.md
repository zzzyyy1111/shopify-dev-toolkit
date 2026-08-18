---
name: shopify-bug-diagnosis
description: Reproduce and diagnose Shopify storefront and theme-editor defects using local theme code, a Development Theme or verified unpublished preview, browser evidence, console errors, network requests, and dependency analysis. Use for Liquid, CSS, JavaScript, cart, variant, discount, app block, Markets, locale, responsive, or preview failures when the user wants the cause identified before any repair.
---

# Shopify Bug Diagnosis

Diagnose first. Do not implement a repair unless the user separately asks for it and approves the affected-file plan.

## Safety boundary

- Prefer a Development Theme or verified unpublished preview.
- Never perform checkout, place orders, alter customers, publish themes, or change live store data.
- Do not disable apps, change Markets, or mutate Theme Editor settings without approval.
- Preserve the exact starting state and separate observation from inference.

## Workflow

1. Capture expected behavior, actual behavior, URL, viewport, market, language, product, variant, and reproduction steps.
2. Reproduce once and record console, network, DOM, screenshots, and timing evidence.
3. Trace the element to its template, section, block, snippet, asset, setting, metafield, metaobject, or app dependency.
4. Classify the cause: theme code, invalid schema/config, missing store data, app dependency, browser/session, Shopify platform, or not reproduced.
5. Identify the smallest repair surface and regression risks.
6. Report confidence and competing explanations. Never claim certainty without evidence.
7. If repair is requested, hand off to `$shopify-code-change-guard`, then `$shopify-theme-preview-guard` and `$shopify-regression-test`.

Use `assets/diagnosis-report.md` for the handoff.
