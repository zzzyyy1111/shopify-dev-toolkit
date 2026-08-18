# Cross-store unpublished-theme workflow

## Required identity

Collect source store, source numeric Theme ID, target store, and target numeric Theme ID. Never identify a remote theme only by display name.

## Verify roles before download

Use read-only listing for each theme:

```text
shopify theme list --id <id> --role unpublished --json --store <store>
```

Require exactly one returned theme whose numeric ID matches and whose role equals `unpublished`. Treat empty, multiple, malformed, authentication-failed, `main`, `development`, or `demo` results as blocked.

## Pull into isolated local folders

Use two distinct, new or empty local folders. Never pull source and target into the same path.

```text
shopify theme pull --theme <id> --store <store> --path <local-folder>
```

After pulling, snapshot the source and keep it read-only. Initialize or confirm Git for the target before implementation. Record store, Theme ID, verified role, local path, and verification time in the migration manifest.

## Upload boundary

This Skill never uploads. After local implementation and verification, pass the target manifest to `$shopify-theme-preview-guard update-unpublished`. That Skill must independently verify the target role immediately before uploading only approved files.

## Stop reasons

- `SOURCE_NOT_UNPUBLISHED`
- `TARGET_NOT_UNPUBLISHED`
- `SOURCE_ROLE_UNVERIFIED`
- `TARGET_ROLE_UNVERIFIED`
- `SOURCE_TARGET_PATH_COLLISION`
- `AUTHENTICATION_FAILED`
- `LOCAL_TARGET_NOT_RECOVERABLE`

Use the mandatory blocked report and state that no remote Shopify mutation occurred during verification or pull.
