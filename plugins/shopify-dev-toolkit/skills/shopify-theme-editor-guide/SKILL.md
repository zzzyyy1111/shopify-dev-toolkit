---
name: shopify-theme-editor-guide
description: Create merchant- and operations-friendly instructions for configuring a Shopify theme feature in the Theme Editor. Use after section, block, template, setting, app block, metafield, metaobject, or migrated-feature work to explain where the feature appears, how to add and configure it, setting meanings and safe ranges, dependencies, market and device behavior, preview steps, common problems, and recovery without modifying theme code or store settings.
---

# Shopify Theme Editor Guide

Create instructions from verified code and preview evidence. Do not invent setting names, defaults, App requirements, or merchant capabilities.

## Workflow

1. Identify the exact template, section type, block type, setting IDs, labels, defaults, ranges, presets, limits, and enabled conditions.
2. Trace locale labels, App blocks, metafields, metaobjects, product/collection requirements, Markets behavior, and desktop/mobile differences.
3. Verify the steps in a Development Theme or unpublished Theme Editor when available. Do not save persistent settings without approval.
4. Translate technical names into concise operator language while preserving exact UI labels in quotation marks.
5. Include prerequisites, add/configure steps, recommended values, preview checks, common errors, disable/remove steps, and recovery.
6. Mark unverified or store-specific steps clearly.
7. Use `assets/theme-editor-guide.md`; optionally incorporate it into `$shopify-delivery-report`.

Never instruct the merchant to publish. End at preview or draft-theme review.
