# Sprint 2 - Review

- **Date:** 2026-07-07
- **Sprint:** DVBRW Sprint 2 (2026-07-20 → 2026-08-03)
- **Participants:** Developer (Joseph Forson), Stakeholder / Product Owner
- **Sprint goal:** Implement stakeholder feedback, complete the cart, and improve DevOps visibility.

## Outcome

**Sprint goal met.** All seven committed stories were delivered and merged to
`main` via reviewed pull requests, with green CI.

| Story | Points | Status |
|-------|--------|--------|
| DVBRW-21 Prices in Rwandan Francs (RWF) | 2 | Done |
| DVBRW-22 Personalised greeting after login | 1 | Done |
| DVBRW-9 Add drinks to shopping cart | 3 | Done |
| DVBRW-10 Enter delivery address and phone | 2 | Done |
| DVBRW-11 Confirm and place order | 5 | Done |
| DVBRW-18 Record application events in logs | 5 | Done |
| DVBRW-19 Add health check command | 2 | Done |

**20 / 20 story points completed.**

## What was demonstrated

1. **RWF pricing** - the menu, customization, and order totals all display in
   Rwandan Francs (e.g. `RWF 3,000`).
2. **Greeting** - after login the menu shows "Hi, <name> — ready for a coffee?".
3. **Cart** - add customized drinks (identical drinks merge into a quantity),
   change quantity, remove, with subtotal/total in RWF.
4. **Delivery** - guided `>` prompt for name/phone/address/instructions, with
   required-field validation.
5. **Place order** - order review, unique order id (`DVB-XXXXXXXX`), **saved to
   MongoDB Atlas**, and a terminal confirmation. Verified end-to-end against Atlas.
6. **Logging** - login, order creation, status changes, and errors written to
   `logs/devbrew.log`.
7. **Health check** - `devbrew health` reports application status and live
   database connection status (connected / not configured / unavailable).

**Quality evidence:** 87 automated tests (unit + headless Textual UI tests + CLI
tests), ruff clean, GitHub Actions CI passing on every PR.

<br>
<b> SHOT 4 </b>
<img width="1183" height="693" alt="Screenshot From 2026-07-07 20-49-42" src="https://github.com/user-attachments/assets/39d9fb83-44da-4e8d-bc29-1e19110540a3" />

<br><br>

<b> SHOT 5 </b>

<img width="587" height="633" alt="Screenshot From 2026-07-07 22-51-44" src="https://github.com/user-attachments/assets/01306059-1cd3-4ea9-8f04-77d7a02e118f" />

<br><br>

<b> SHOT 6 </b>
<img width="1172" height="693" alt="Screenshot From 2026-07-07 22-54-27" src="https://github.com/user-attachments/assets/8599ab40-c74f-4e3e-9e1b-d68f2a9ba5d2" />

<br><br>

<b> SHOT 7 - Logs </b>
<img width="1181" height="580" alt="image" src="https://github.com/user-attachments/assets/e695bb97-6a4a-4501-aabe-dc83e34e0eea" />

<br><br>

<b> SHOT 7 - Monitoring health and sys check </b>
<img width="1181" height="293" alt="Screenshot From 2026-07-07 22-59-01" src="https://github.com/user-attachments/assets/58babff2-b576-4a48-bbc1-b699b23e61dd" />


## Stakeholder feedback (this review)

The stakeholder was happy so far with the increment ("That's great"), and raised
one issue:

- **Graceful offline handling.** With the internet turned off, actions that reach
  MongoDB (login, place order) surfaced a long, verbose error and broke the app.
  The stakeholder wants DevBrew to stay on screen and show a clean message such as
  *"Please check your internet connection"* instead of a raw traceback.

This is accepted into the backlog for **Sprint 3**.

## What to be sent to backlog (possibly Sprint 3)

| Key | Story | Est. | Priority | Source |
|-----|-------|------|----------|--------|
| DVBRW-24 | Graceful handling of network / database errors | 3 | High | Sprint 2 Review feedback |
 

**DVBRW-24 - Graceful network/database error handling**

 
