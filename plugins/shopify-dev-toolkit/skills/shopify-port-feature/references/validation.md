# Validation contract

## Static validation

- Parse all changed JSON.
- Run Theme Check when available.
- Run project-native lint, build, and tests.
- Verify referenced snippets, assets, locale keys, schema IDs, and settings.
- Verify the source snapshot is unchanged.
- Verify target changes stay within the manifest.
- Verify protected files and patterns are unchanged.

## Behavioral regression

Select cases relevant to touched surfaces:

- Product with one and multiple variants.
- Available, unavailable, and sold-out variants.
- Regular and compare-at prices.
- Quantity changes and line item properties.
- Add to cart, cart drawer refresh, cart page update, remove, and checkout link.
- Dynamic checkout and nearby App blocks.
- Theme Editor load, unload, reorder, and block select.
- Mobile and desktop interaction.
- Supported locale, market, currency, and long translated text.

Test both feature-enabled and feature-disabled products. A port that only works when enabled is incomplete.

## Visual regression

Capture the target before and after with the same URL, data, viewport, locale, market, cookies, and UI state. Cover at least desktop and mobile plus any drawer, modal, expanded, error, unavailable, or focus state touched by the feature.

Mask only known dynamic regions and document each mask. Treat differences outside the intended feature root as failures until reviewed.

## Preview requirement

Local static checks cannot prove integration with Shopify data, CDN, Theme Editor, Cart API, Markets, or Apps. Require a development or unpublished-theme preview for production-readiness claims.

## Result states

- `analysis_complete`: specification produced; no target edits.
- `plan_ready`: mapping and manifest ready for approval.
- `local_implementation_complete`: edits and static checks pass.
- `preview_validation_pending`: real Shopify behavior not yet tested.
- `ready_for_review`: required preview tests pass; human review remains.
- `blocked`: a documented dependency, risk, or failed invariant prevents safe progress.

Never report `ready_for_review` when preview validation did not run.
