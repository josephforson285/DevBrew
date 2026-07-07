# Sprint 2 - Retrospective

- **Date:** 2026-07-07
- **Sprint:** DVBRW Sprint 2 (2026-07-20 → 2026-08-03)
- **Participants:** Developer (Joseph Forson)
- **Format:** What went well · What didn't go well · Action items for Sprint 3

## What went well

- **Sprint goal achieved** - all seven stories (20/20 points) delivered and
  merged to `main` via reviewed PRs, with green CI, first release has been made where users can install on their linux machine.
- **Sprint 1 improvements paid off.** Dependencies stayed pinned and each story
  was verified in a clean virtual environment before pushing - there was **no CI
  dependency drift this sprint**.
- **Order flow landed cleanly.** Cart → delivery → review → place order, with the
  order persisted to MongoDB Atlas and verified end-to-end (then cleaned up).
- **Repository abstraction proved its worth.** Adding order persistence was a new
  repository behind the same interface; tests/CI ran DB-free while the real app
  used Atlas - no service or UI changes needed.
- **Backlog discipline.** Stakeholder ideas were turned into backlog items immediately: RWF/greeting (delivered).
## What didn't go well

- **Offline robustness gap.** The app assumed the database was reachable. With no
  internet, MongoDB calls raised a verbose traceback and crashed the TUI - only
  discovered when the stakeholder tested offline during the review. Error handling
  for network/database failures was missing.
<!-- - **UI error tests didn't cover connectivity.** Our tests run against the
  in-memory store, so they never exercised a failing database - the gap wasn't
  caught automatically. -->

## Action items for Sprint 3 (improvements)

1. **Add graceful network/database error handling (DVBRW-24).** Catch connection
   errors at the service/UI boundary and show a friendly message
   ("Please check your internet connection") instead of a traceback; keep the app
   running. 

2. More to be added when we meet for the next planning.
 
