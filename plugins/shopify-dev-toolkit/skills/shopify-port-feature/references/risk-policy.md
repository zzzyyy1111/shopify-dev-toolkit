# Risk policy

## Low risk

- Add an isolated snippet or scoped asset.
- Add new locale keys without changing existing keys.
- Read an existing metafield without changing store data.
- Add a render call at a verified extension point.
- Add non-breaking presentation markup outside core forms.

Low risk still requires manifest and validation.

## Medium risk

- Integrate with product-form or variant lifecycle.
- Add line item properties or cart attributes.
- Add Theme Editor settings without renaming existing IDs.
- Render new content in cart drawer or cart page.
- Subscribe to existing target-theme events.
- Add styles near App blocks or dynamic content.

Require explicit plan approval and runtime tests.

## High risk

- Change variant selection, availability, price, selling plans, cart requests, discounts, checkout, subscriptions, bundles, inventory decisions, or payment behavior.
- Replace existing components or event infrastructure.
- Change global CSS, broad selectors, DOM order, form semantics, schema IDs, setting IDs, block types, or persisted settings.
- Remove, defer, or rewrite third-party App behavior.

Keep high-risk work plan-only by default. Require narrow user authorization after showing affected behavior and rollback strategy.

## Unsupported automatic migration

- App backend or database.
- Webhooks, scheduled jobs, or queues.
- Shopify Functions or checkout extensions.
- Private App APIs, App proxies without source, subscriptions, bundles, search providers, page builders, or server-side personalization.
- Store data creation, metafield definition mutations, app installation, theme upload, or publish.

Create a manual workstream for these dependencies. Theme code may be ported only when it can safely degrade without the external dependency and that behavior is approved.

## Hard stops

- Source and target are the same resolved path.
- Core behavior is uncertain.
- Core mapping confidence is low.
- Target user changes overlap planned files.
- Manifest scope is exceeded.
- Source snapshot changes.
- Protected file or pattern changes.
- Required regression test fails.
- Unexpected visual change occurs outside the feature region.
