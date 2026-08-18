---
name: shopify-markets-qa
description: Test Shopify Markets and cross-border storefront behavior on a Development Theme or verified unpublished preview. Use to compare countries, languages, currencies, localized URLs, market context templates, product availability, price formatting, selectors, redirects, tax or duty messaging, hreflang, app behavior, and cart continuity without changing Markets configuration or live store data.
---

# Shopify Markets QA

Run read-only market comparisons. Never change Markets, domains, languages, prices, duties, shipping, or catalog assignments.

## Preconditions

- Require a Development Theme or verified unpublished preview.
- Obtain the market matrix: country, language, currency, domain/subfolder, and representative product.
- Use the same product, variant, browser state, and viewport for comparisons.

## Workflow

1. Read `references/markets-matrix.md` and select at least one primary and one contrasting market.
2. Record detected country, language, currency, URL structure, selector state, and redirect behavior.
3. Compare home, product, collection, cart, and one content page.
4. Check product availability, price/currency formatting, compare-at price, translation, context template, app blocks, shipping/tax/duty text, canonical, and hreflang.
5. Confirm market switching preserves a sensible equivalent URL and cart behavior without completing checkout.
6. Classify issues as theme, locale, Markets configuration, catalog/data, domain, app, or session-dependent.
7. Write `assets/markets-report.md`. Never infer legal or tax correctness.

Use `$shopify-locale-audit` for locale files, `$shopify-seo-audit` for indexation, and `$shopify-bug-diagnosis` for reproducible failures.
