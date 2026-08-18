# Three-way merge policy

- `vendor-only`: old original equals customized; accept upstream after review.
- `custom-only`: old original equals new original; port the customization after dependency review.
- `converged`: customized already matches new upstream; no merge needed.
- `conflict`: both customized and upstream changed differently; resolve behavior, schema, styling, and dependencies manually.
- `deleted-upstream`: upstream removed a file retained or customized locally; identify replacement architecture before porting.
- `new-upstream`: new vendor file; preserve unless it conflicts with a customization.

Never overwrite the new theme with the customized old tree. Merge by approved file manifest into a separate target.
