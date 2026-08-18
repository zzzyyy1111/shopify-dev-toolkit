---
name: shopify-port-feature
description: Analyze, plan, implement, and verify safe feature migrations between Shopify Online Store 2.0 themes, including two verified unpublished themes from different stores, or recreate an observable feature from a user-provided public webpage in a local Shopify target theme. Use for Liquid, JSON, CSS, JavaScript, locale, metafield, metaobject, cart-property, theme-editor, app-dependency, and cross-platform feature analysis. Default to analysis-only, keep source artifacts read-only, block published or unverified remote targets, constrain local edits with a manifest, and never publish or change live store data.
---

# Shopify Feature Porter

Port behavior, not files. Extract a feature specification from the source theme, map it to the target theme's native architecture, implement only an approved local change set, and prove that the change stayed inside its safety boundary.

## Non-negotiable rules

- Default to `analyze` when the user does not explicitly request implementation.
- Treat the source theme as read-only. Snapshot it before investigation and verify it after work.
- Never run theme push, theme publish, app deploy, store mutations, or live-store configuration changes.
- Never migrate or upload into a published remote theme. Require a verified `unpublished` target role before a remote draft-to-draft workflow.
- Never modify `config/settings_data.json`.
- Do not discard, overwrite, or reset pre-existing user changes.
- Do not infer implementation authorization from a request to analyze, compare, estimate, or plan.
- Stop when a core dependency or target integration point has low confidence.
- Keep each port to one feature and one independently reversible target change set.
- Prefer a small adapter or isolated feature module over copying source-theme architecture.
- Do not claim the feature is production-ready without testing against a Shopify preview using representative store data.
- Whenever work stops, explain the exact stage, reason, evidence, completed actions, whether any file or remote state changed, and the safest next step.

## Choose the mode

1. `analyze`: Inspect the source and produce a feature specification. Make no edits.
2. `plan`: Inspect both themes, produce a target mapping and migration manifest. Make no edits.
3. `implement`: Require an approved manifest, then edit only allowed target files and validate.
4. `audit`: Inspect an existing port against its specification, manifest, and validation requirements.
5. `web-reference-analyze`: Observe a user-provided webpage and extract a feature specification without claiming access to its private source code.

If the user's request mixes modes, complete the safe earlier modes and pause before the first material edit unless implementation was explicit.

## Required inputs

Obtain or discover:

- Absolute source-theme path, or a user-provided public reference URL.
- Absolute target-theme path for `plan`, `implement`, or `audit`.
- A bounded feature identifier: description plus at least one seed such as a file, selector, locale key, metafield, screenshot, URL, commit, or visible UI label.
- Desired mode.

Reject a whole-theme request such as "copy everything." Ask the user to choose one feature.

## Remote unpublished-theme workflow

Read `references/remote-drafts.md` completely before accessing either store.

When the source and target are drafts in different Shopify stores:

1. Require both store identifiers and numeric Theme IDs.
2. Use Shopify CLI read-only theme listing to verify both roles are exactly `unpublished`.
3. Stop with a reason report if either role is `main`, `development`, `demo`, missing, ambiguous, or cannot be verified.
4. Pull each theme into a separate local directory. Treat the local source copy as read-only and the local target copy as the only editable theme.
5. Run the normal analyze, plan, implement, and audit workflow locally.
6. Hand the approved target file manifest to `$shopify-theme-preview-guard` in `update-unpublished` mode.
7. Let that Skill re-verify the target Theme ID as `unpublished` immediately before upload and upload only manifest-listed files.

This Skill itself never uploads. A local target folder without verified remote metadata may be edited locally, but must not be represented as safe for remote upload.

## Public webpage reference workflow

Read `references/web-reference.md` completely when the source is a URL. Use the available browser capability to observe public UI, behavior, responsiveness, states, and accessibility. Produce the same Feature Spec used for theme sources, with `source_type: web_reference` and evidence URLs, timestamps, screenshots, and interaction steps.

Recreate the behavior using the target Shopify theme's own architecture. Do not claim to migrate server-side code, private APIs, databases, paid assets, or inaccessible source code. Stop when access is blocked, the behavior cannot be observed, required assets or rights are missing, or a critical behavior depends on an unknown backend.

## Workflow

### 1. Preflight

Run `scripts/preflight.py` for the applicable theme paths. It validates theme shape, path separation, Git state, and protected files. Do not proceed with implementation when:

- Source and target resolve to the same directory.
- Either directory is not recognizable as a Shopify theme.
- The target is not a Git worktree.
- The target has pre-existing changes overlapping planned files.
- The source is already dirty and the changed files overlap the feature investigation.

Record existing dirty files; they belong to the user. Never include them in the port.

Create a source hash snapshot with `scripts/theme_snapshot.py create`. Store working artifacts outside both theme directories unless the user requests otherwise.

### 2. Discover the source feature

Read `references/discovery.md` completely. Trace from the provided seeds through Liquid renders, assets, selectors, events, settings, locale keys, data dependencies, and external services. Use `scripts/scan_dependencies.py` as evidence collection, not as a substitute for code reading.

Produce a feature specification using `assets/feature-spec.template.json`. Record unknowns instead of guessing. Stop if an unknown affects activation, price, variants, cart submission, discounts, checkout, subscriptions, or persisted data.

### 3. Classify support and risk

Read `references/risk-policy.md` completely. Classify every capability and proposed edit.

- Supported theme-only behavior may proceed.
- App backend, database, webhook, Function, checkout, subscription, bundle, or private API dependencies require a manual workstream and are not silently ported.
- High-risk core-commerce edits remain plan-only unless the user gives narrow, explicit authorization after reviewing the risk.

### 4. Map to the target theme

Read `references/target-mapping.md` completely. Locate target-native integration points and record confidence for every mapping.

- `high`: verified through definitions and call sites.
- `medium`: supported by evidence but requires runtime validation.
- `low`: ambiguous or inferred from naming only.

Do not implement when any core mapping is `low`. Prefer target utilities, events, styling tokens, accessibility conventions, and Theme Editor lifecycle patterns.

### 5. Create and approve the migration manifest

Copy `assets/migration-manifest.template.json` to the working-artifact directory and fill it with exact relative paths. The manifest must list:

- Allowed files to create.
- Allowed files to modify.
- Protected files and patterns.
- Behavioral and structural invariants.
- Required validation scenarios.
- Known manual steps and unresolved risks.

Show the user the planned file boundary before implementation. An approved plan does not authorize new files discovered later; update the plan and request approval when scope expands materially.

### 6. Implement locally

Before editing:

- Confirm the requested mode is `implement`.
- Confirm the manifest is approved.
- Confirm the current target Git state still matches preflight.
- Create or use a feature branch when allowed. Do not change branches if that would disturb user work.

Modify only manifest-allowed files. Keep source-specific class names, global utilities, event buses, and component architecture out of the target unless deliberately mapped. Preserve DOM contracts, schema IDs, setting IDs, block types, form fields, accessibility attributes, and existing locale keys.

If an additional file becomes necessary, stop, explain why, and revise the manifest before touching it.

### 7. Verify boundaries

Run:

- `scripts/theme_snapshot.py verify` against the source snapshot.
- `scripts/verify_migration.py` against the target and manifest.
- Theme Check when available.
- Project-native lint, build, and tests when present.

Any source change, protected-file change, or out-of-manifest target change fails the port. Do not auto-revert user files; report the exact paths.

### 8. Validate behavior and visuals

Read `references/validation.md` completely. Derive feature tests from the specification and regression tests from affected target surfaces.

At minimum validate relevant combinations of:

- Desktop and mobile.
- Default, alternate, unavailable, and sold-out variants.
- Add to cart, quantity update, remove, cart drawer, and cart page when touched.
- Theme Editor section load/unload/reorder when JavaScript is added.
- Supported locales and markets when content varies.
- App blocks and dynamic checkout buttons near the integration point.

Compare before/after screenshots of the target theme. Ignore only explicitly documented dynamic regions. A visual difference outside the intended feature region is a failure until explained and approved.

### 9. Report truthfully

Use `assets/verification-report.md`. Distinguish:

- Static validation passed.
- Local behavior validation passed.
- Preview validation passed.
- Manual steps remain.
- Production readiness is unverified.

Never equate successful parsing or Theme Check with verified storefront behavior.

## Completion gate

Call a port complete only when:

- The feature specification has no unresolved core behavior.
- All core target mappings are high or explicitly reviewed medium confidence.
- Actual edits are entirely within the approved manifest.
- The source snapshot is unchanged.
- Protected files are unchanged.
- Required static and behavior tests pass.
- Visual differences are limited to the intended feature.
- Shopify preview validation passes with representative data.

Otherwise report the narrowest accurate state, such as "local implementation complete; preview validation pending."

## Mandatory stop report

Use `assets/blocked-report.md` whenever the workflow stops or blocks. Never reply only with "cannot continue." Include a stable reason code, evidence, local and remote mutation status, and a concrete recovery path.

## Resource routing

- Read `references/discovery.md` during source analysis.
- Read `references/risk-policy.md` before classifying or implementing.
- Read `references/target-mapping.md` before creating a plan.
- Read `references/validation.md` before implementation testing or audits.
- Read `references/web-reference.md` when the source is a webpage URL.
- Read `references/remote-drafts.md` when either theme is identified by a Shopify store and Theme ID.
- Use templates in `assets/` for durable artifacts; do not invent abbreviated substitutes.
- Use scripts in `scripts/` for safety evidence. If a script cannot run, do not waive its check silently; perform an equivalent read-only check and disclose the substitution.
