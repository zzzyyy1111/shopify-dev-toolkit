# Safe Git policy

- Read-only inspection is the default.
- Require separate approval for init, branch creation, staging, commit, merge, and push.
- Stage explicit manifest paths only and review `git diff --cached` before commit.
- Preserve unrelated tracked and untracked work.
- Prefer revert or a new corrective commit over history rewriting.
- Never use destructive reset, clean, force checkout, force push, or automatic push.
