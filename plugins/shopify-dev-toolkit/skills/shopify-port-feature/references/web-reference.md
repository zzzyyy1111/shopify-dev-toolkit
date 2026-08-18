# Public webpage feature reference

## Scope

Use a public webpage as observable product behavior, not as a source-code repository. Recreate the requested feature in the target Shopify theme using original implementation code and the target theme's conventions.

## Required evidence

- Source URL and observation time.
- Desktop and mobile screenshots.
- Initial, hover/focus, loading, empty, error, expanded, modal/drawer, and completed states when observable.
- User interaction steps and resulting UI changes.
- Visible text, controls, accessibility names, keyboard behavior, and responsive layout.
- Public network behavior only when needed to understand the interaction; do not bypass authentication or technical controls.

## Limits

- Do not claim access to server-side logic, private APIs, databases, build sources, or original unminified code.
- Do not copy proprietary code, paid assets, logos, product media, or protected branding without user-provided rights.
- Do not bypass login, CAPTCHA, paywalls, geoblocking, bot protection, or access controls.
- Do not reproduce payment, credential, tracking, or sensitive-data behavior without a separate security review.
- Treat inferred backend behavior as an uncertainty.

## Output

Convert observable behavior into the standard Feature Spec. Mark each behavior as `observed`, `inferred`, or `unknown`. Block implementation when a commerce-critical behavior is unknown. Adapt visual style to the target theme unless the user explicitly supplies authorized design assets and requests closer fidelity.
