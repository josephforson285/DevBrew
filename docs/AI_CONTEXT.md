# AI Context & Working Agreement

Instructions for any coding assistant (Claude / Codex) working on this repo.

## Source of truth
- Jira **DVBRW** is authoritative. Do not change user stories, story points,
  priorities, or acceptance criteria unless explicitly instructed.
- Definition of Done is DVBRW-20 (see `docs/07_DEFINITION_OF_DONE.md`).

## Scope
- Implement the **active Sprint 1** stories only: **DVBRW-6, DVBRW-7, DVBRW-8**.
- Do **not** implement cart, checkout, tracking, logging, or health check until
  explicitly asked.

## Git workflow (professional, no big-bang)
- One feature branch per story: `feature/DVBRW-<n>-<slug>`.
- Small, incremental commits, each referencing the Jira key, e.g.
  `feat(DVBRW-6): add registration flow`.
- Open a PR per branch; merge to `main` after review and green CI.
- Never force-push or rewrite shared history; never delete work without asking.

## Engineering
- Keep the architecture modular and testable (see `05_ARCHITECTURE.md`).
- Services depend on repository interfaces, not on pymongo directly.
- Every feature has tests where reasonable; all tests pass locally and in CI
  before a story is Done.
- Secrets (Atlas URI) live in `.env` only.
