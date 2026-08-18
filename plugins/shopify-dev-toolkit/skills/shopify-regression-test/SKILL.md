---
name: shopify-regression-test
description: Perform read-only browser regression testing against a Shopify Development Theme or verified unpublished preview. Use after theme changes or feature migration to test products, variants, prices, add-to-cart, cart drawer, discounts, search, navigation, responsive layout, Theme Editor reload behavior, console errors, and network failures without changing live store data.
---

# Shopify Regression Test

Test only a Development Theme or verified unpublished preview. Never test a live theme when actions can mutate carts, customer state, or store data.

## Preconditions

- Obtain the preview URL, store, theme ID, and verified role.
- Reject a URL when the theme role is live, unknown, or cannot be verified.
- Use safe products and avoid checkout completion, real orders, customer changes, or app billing actions.
- Ask before adding persistent test data or changing Theme Editor settings.

## Workflow

1. Read `references/test-matrix.md` and select tests affected by the change.
2. Record viewport, product, market, language, and starting cart state.
3. Test the happy path, one boundary state, and one failure or empty state.
4. Capture screenshots for visual failures and record console/network evidence.
5. Distinguish theme defects from app dependencies, store data, market configuration, or browser-session issues.
6. Never repair code automatically. Hand failures to `$shopify-bug-diagnosis` or `$shopify-code-change-guard`.
7. Write the result using `assets/regression-report.md`.

Use `passed`, `passed_with_warnings`, `failed`, or `blocked`. A successful HTTP response alone is not a passed functional test.
