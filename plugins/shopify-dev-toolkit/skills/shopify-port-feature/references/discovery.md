# Source feature discovery

## Goal

Build an evidence-backed dependency graph and feature specification. Do not treat filename similarity as proof.

## Seed expansion

Start from the user's seed and search in both directions:

- Definitions: snippets, sections, custom elements, functions, CSS selectors, locale entries, schema settings.
- Consumers: Liquid renders, imports, script tags, DOM queries, event listeners, template references.
- Data: metafields, metaobjects, tags, line item properties, cart attributes, customer state, routes.
- Runtime: custom events, Pub/Sub topics, `shopify:section:*`, network endpoints, third-party globals.

Record each dependency as `required`, `optional`, `presentation-only`, `external`, or `unknown`.

## Liquid checks

- Follow `render`, `section`, and asset references.
- Record every object assumption and scope requirement.
- Inspect schema settings, blocks, presets, and locale keys.
- Identify conditions controlling activation and visibility.
- Note HTML/data attributes consumed by JavaScript or CSS.

## JavaScript checks

- Follow imports, registrations, and initialization call sites.
- Map selectors to the Liquid that emits them.
- Record events produced and consumed, including payload shape.
- Identify Shopify Cart API calls and submitted form fields.
- Check Theme Editor reinitialization and cleanup.
- Identify third-party globals and remote requests.

## CSS checks

- Find the smallest feature root selector.
- Identify global selectors and cascade dependencies.
- Record variables, color schemes, breakpoints, animations, and state classes.
- Treat DOM nesting selectors as structural dependencies.

## Commerce-sensitive checks

Explicitly trace:

- Variant ID source and updates.
- Price and compare-at price display.
- Availability and selling-plan state.
- Product-form submission.
- Line item properties and cart attributes.
- Cart rendering after section updates.
- Discount, bundle, subscription, or checkout dependencies.

Stop on ambiguous commerce-sensitive behavior.

## Output quality

The feature specification must state activation, surfaces, inputs, outputs, UI states, persistence, localization, accessibility, editor behavior, dependencies, external systems, and uncertainties. Cite file paths and symbols for important claims.
