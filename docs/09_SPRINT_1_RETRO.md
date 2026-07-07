# Sprint 1 - Retrospective

- **Date:** 2026-07-07
- **Sprint:** DVBRW Sprint 1 (2026-07-06 → 2026-07-20)
- **Participants:** Developer (Joseph Forson)
- **Format:** What went well · What didn't go well · Action items for Sprint 2

## What went well

- **Sprint goal achieved** — all three committed stories (DVBRW-6, 7, 8; 13/13
  points) delivered and merged to `main`.
- **Professional Git workflow** — one feature branch per story, a reviewed pull
  request per story, small incremental commits referencing the Jira key. History reads as a clear, iterative delivery.
- **CI/CD in place from the start** — GitHub Actions ran `ruff` + `pytest` on
  every pull request and blocked merges when red.
- **Testable architecture** — the repository abstraction let 41 tests (unit +
  headless Textual UI tests) run without a database, while MongoDB Atlas was
  verified working locally end-to-end. CI stays fast and DB-independent.
- **Responsive to feedback** — UI direction was adjusted quickly based on
  stakeholder input to reach a clean, terminal-native experience.

## What didn't go well

- **Dependency drift broke CI ("works on my machine").** Dependencies were left
  unpinned, so CI installed Textual 8.x while local development used 0.89.1. The
  UI tests passed locally but failed in CI. It cost a debugging cycle to trace.
- **UI direction changed several times after implementation.** The interface was
  built as form widgets, then reworked into a terminal console, then into a
  classic `>`-cursor menu, plus a theme change (green → orange). Because the
  visual direction was not agreed up front, some screens were built more than once.
- **Commit authorship hygiene.** An early commit included an unintended
  co-author trailer that had to be removed by rewriting history before it spread.

## Action items for Sprint 2 (improvements)

1. **Pin dependencies and verify CI-parity before pushing.** *

2. **Agree the UI/UX direction before building a screen.** Sketch the target
   (a short ASCII mockup or a note) and confirm it with the stakeholder before
   implementation, to avoid rebuilding screens. 
    

3. **Keep the Sprint Review feedback loop tight.** Turn stakeholder feedback into
   backlog items immediately (done this sprint: DVBRW-21 RWF currency, DVBRW-22
   greeting) and pull them into Sprint 2 planning.
## Carried into Sprint 2

- Apply improvements 1–3 above.
- Deliver stakeholder-requested backlog items: **DVBRW-21** (prices in Rwandan
  Francs) and **DVBRW-22** (personalised greeting after login).
- Begin DevOps/monitoring stories as capacity allows (logging, health check).
