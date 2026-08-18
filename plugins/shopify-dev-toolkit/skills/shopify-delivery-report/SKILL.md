---
name: shopify-delivery-report
description: Assemble a concise, evidence-backed Shopify theme development handoff from change manifests, diffs, dependency audits, validation reports, preview links, test results, known limitations, configuration steps, rollback information, and unpublished-theme evidence. Use when a feature, migration, bug fix, upgrade, or draft-theme delivery is ready for developer, QA, merchant, or operations review.
---

# Shopify Delivery Report

Create documentation only. Do not upload, publish, change settings, or convert unverified claims into passed results.

## Workflow

1. Read `references/evidence-requirements.md` and collect available reports from the other toolkit Skills.
2. Verify store, local path, Development/unpublished Theme ID and role, preview URL, editor URL, changed-file manifest, and Git state where available.
3. Summarize the business outcome, implementation, Theme Editor usage, App/data dependencies, changed files, and excluded scope.
4. Record validation status for Schema, locale, SEO, Markets, performance, accessibility, functional, and visual tests. Mark missing evidence `not_tested`.
5. Include merchant configuration steps, known limitations, rollback instructions, and safe next actions.
6. Use `assets/delivery-report.md` and state `Live theme unchanged` unless evidence proves otherwise; never say released or published.

Remove secrets, tokens, customer data, and unnecessary local paths from reports intended for external sharing.
