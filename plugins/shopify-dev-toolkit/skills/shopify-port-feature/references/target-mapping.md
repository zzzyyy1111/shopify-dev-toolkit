# Target-theme mapping

## Mapping principles

Map capabilities, not filenames. For each required behavior, locate the target definition, call site, lifecycle, styling convention, and test surface.

Prefer, in order:

1. Existing target extension point or snippet parameter.
2. Existing target component and event contract.
3. Small adapter using target conventions.
4. Isolated feature module with a minimal integration hook.

Do not copy the source event bus, utility layer, global CSS, or component base class merely because the source feature uses it.

## Required mapping fields

For each capability record:

- Source path and symbol.
- Target path and symbol or proposed hook.
- Evidence supporting the mapping.
- Confidence: high, medium, or low.
- Behavioral differences.
- Required adapter.
- Validation scenarios.

## Theme contracts to preserve

- Product form action and variant input.
- Quantity, selling-plan, and line item property fields.
- Price and availability update containers.
- Cart section-rendering behavior.
- Existing data attributes and event payloads.
- Theme Editor section lifecycle.
- App block placement and dynamic checkout buttons.
- Schema setting IDs, block types, presets, and saved configuration.
- Accessibility names, focus management, live regions, and keyboard behavior.

## Styling adaptation

- Reuse target color schemes, typography, spacing, buttons, breakpoints, and utilities.
- Scope new CSS beneath one feature root.
- Avoid source-theme class names unless the target already defines the same semantic contract.
- Avoid selector specificity escalation and global element selectors.
- Record every intentional visual difference.

## Confidence rules

- High: definition and runtime consumer are both verified.
- Medium: the mapping is supported by code evidence but needs preview behavior confirmation.
- Low: based mainly on naming, visual similarity, or incomplete code.

Do not implement a low-confidence core mapping.
