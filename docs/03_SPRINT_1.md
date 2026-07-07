# 03 - Sprint 1 Plan

- **Sprint:** DVBRW Sprint 1
- **State:** Done
- **Dates:** 2026-07-06 → 2026-07-20
- **Goal:** Deliver the first usable DevBrew terminal experience where a user can
  log in, browse the coffee menu, and customize a drink.
- **Committed:** 3 stories, 13 story points.

| Key | Story | Pts | Priority |
|-----|-------|-----|----------|
| DVBRW-6 | Register and log into DevBrew | 5 | High |
| DVBRW-7 | Browse the coffee menu using keyboard navigation | 3 | High |
| DVBRW-8 | Customize coffee before ordering | 5 | High |

## Acceptance Criteria

### DVBRW-6 - Register and log into DevBrew
- User can register using name, email, and phone number.
- User can log in with email.
- User session is remembered during app usage.
- Invalid login input shows a clear error message.

### DVBRW-7 - Browse the coffee menu using keyboard navigation
- User can view available coffee items.
- User can navigate menu options with arrow keys.
- Each menu item displays name, price, size options, and description.
- The app does not crash when menu data is loaded.

### DVBRW-8 - Customize coffee before ordering
- User can choose size.
- User can choose milk option.
- User can choose sugar level.
- User can add extra shot.
- Customization appears correctly in cart/order summary.

## Out of scope for Sprint 1
Cart, checkout, delivery/tracking, logging, and health check are **not**
implemented this sprint (later stories DVBRW-9+).

## Development order
1. DVBRW-6 - auth basics, user model, register/login, session, tests.
2. DVBRW-7 - menu data model, Textual menu screen, arrow-key nav, tests.
3. DVBRW-8 - customization options, screen, validation, summary, tests.
