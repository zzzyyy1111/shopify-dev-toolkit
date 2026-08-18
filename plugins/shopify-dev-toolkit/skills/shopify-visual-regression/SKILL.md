---
name: shopify-visual-regression
description: Compare baseline and changed Shopify Development Theme or verified unpublished previews for unintended visual differences. Use after Liquid, CSS, JavaScript, section, template, app block, or feature-migration changes to capture matched screenshots across pages, viewports, and UI states, classify expected versus unexpected differences, and produce evidence without modifying theme code or live store data.
---

# Shopify Visual Regression

Compare like-for-like preview states. Never mutate theme code while running this skill.

## Preconditions

- Require a baseline URL and changed preview URL, or baseline screenshots and a changed preview.
- Verify remote targets are Development Themes or unpublished themes. Reject live or unknown roles.
- Match product, variant, market, language, viewport, scroll position, consent state, cart state, and UI state.
- Stabilize animations, carousels, videos, timestamps, random counters, reviews, and personalized app content when possible; otherwise mark them dynamic.

## Workflow

1. Read `references/capture-matrix.md` and choose only affected pages plus one nearby integration page.
2. Capture baseline and changed screenshots at identical dimensions.
3. Compare full page and affected components. Record bounding boxes and screenshots for material differences.
4. Classify each difference as `expected`, `unexpected`, `dynamic`, `data-dependent`, or `blocked`.
5. Check overflow, wrapping, fonts, colors, spacing, image ratio, sticky elements, drawers, modals, focus, and layout shift.
6. Do not approve a change solely from pixel similarity; run functional tests through `$shopify-regression-test`.
7. Write `assets/visual-regression-report.md`.

If a repair is requested, hand off the exact affected files and evidence to `$shopify-code-change-guard`.
