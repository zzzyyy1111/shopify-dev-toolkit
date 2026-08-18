---
name: shopify-seo-audit
description: Audit technical SEO and structured data in a local Shopify Online Store 2.0 theme and a Development Theme or verified unpublished preview. Use for titles, meta descriptions, canonical URLs, robots directives, hreflang, headings, image alt text, pagination, Markets URLs, Product and Breadcrumb JSON-LD, duplicate schema output, and SEO app conflicts. Default to reporting and never edit SEO behavior or store content without approval.
---

# Shopify SEO Audit

Audit first. Do not change SEO text, canonical, hreflang, robots, or structured data automatically.

## Workflow

1. Resolve the local theme and run `scripts/seo_static_audit.py <theme-path> --json-output <report>`.
2. If a preview is provided, verify it is Development or unpublished before browser checks.
3. Read `references/runtime-checks.md`; inspect representative home, product, collection, content, search, pagination, and 404 pages.
4. Validate rendered canonical, robots, title, description, headings, hreflang, internal links, image alt, and JSON-LD.
5. Compare JSON-LD price, currency, availability, URL, variant, and review data with visible page state.
6. Detect duplicate output from the theme and SEO/review apps; do not delete either source without confirming ownership.
7. Separate theme-code defects from Shopify-generated sitemap, product content, redirects, Markets settings, and app output.
8. Produce `assets/seo-report.md` with severity, evidence, affected templates, and smallest safe repair.

Never fabricate ratings, reviews, inventory, prices, legal text, or localization. Hand approved theme repairs to `$shopify-code-change-guard` and verify through `$shopify-theme-preview-guard`.
