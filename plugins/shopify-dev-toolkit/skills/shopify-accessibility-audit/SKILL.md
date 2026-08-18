---
name: shopify-accessibility-audit
description: Audit accessibility of a Shopify Development Theme or verified unpublished preview using browser interaction and code evidence. Use to test keyboard navigation, focus order and trapping, semantic structure, headings, labels, names, ARIA, color contrast, image alternatives, errors, drawers, modals, menus, product forms, reduced motion, and Theme Editor interactions without modifying code or live store data.
---

# Shopify Accessibility Audit

Run evidence-based checks against Development or unpublished previews only. Do not claim certification or complete WCAG compliance from automated checks.

## Workflow

1. Verify the preview role and select representative home, product, collection, search, cart, and affected pages.
2. Read `references/accessibility-matrix.md`.
3. Test keyboard-only navigation, visible focus, focus order, escape/close behavior, focus return, and focus trapping.
4. Inspect landmarks, headings, accessible names, labels, errors, live regions, images, icons, tables, dialogs, menus, and product controls.
5. Check contrast, zoom/reflow, horizontal scrolling, reduced motion, touch targets, and mobile controls.
6. Record exact reproduction steps, DOM evidence, screenshot, impact, and confidence. Separate automated findings from manual findings.
7. Write `assets/accessibility-report.md` and hand approved repairs to `$shopify-code-change-guard`.

Never change copy, colors, interaction behavior, or ARIA automatically. Re-test functionality and visuals after approved fixes.
