# Sprint 1 - Review

- **Date:** 2026-07-07
- **Sprint:** DVBRW Sprint 1 (2026-07-06 → 2026-07-20)
- **Participants:** Developer (Joseph Forson), Stakeholder / Product Owner
- **Sprint goal:** Deliver the first usable DevBrew terminal experience where a
  user can log in, browse the coffee menu, and customize a drink.

## Outcome

**Sprint goal met.** All three committed stories were delivered, merged to `main`
via reviewed pull requests, with green CI.

| Story | Points | Status | Acceptance criteria |
|-------|--------|--------|---------------------|
| DVBRW-6 Register and log into DevBrew | 5 | Done | All met |
| DVBRW-7 Browse the coffee menu (keyboard) | 3 | Done | All met |
| DVBRW-8 Customize coffee before ordering | 5 | Done | All met |

**13 / 13 story points completed.**

## What was demonstrated

1. **Launch** `devbrew` → Terminal style with the DEVBREW logo splash.
2. **Register / login** at the `>` console prompt (guided name → email → phone;
   or `login <email>`). Session is remembered; invalid input shows a clear error.
3. **Browse menu** — arrow-key list with a `>` cursor showing name, price, sizes,
   and description.
4. **Customize** — choose Size / Milk / Sugar / Extra shot; a live ORDER SUMMARY
   updates with the total (extra shot +$0.50).
5. **Quality evidence** — 41 automated tests (unit + headless Textual UI tests),
   `ruff` clean, GitHub Actions CI passing on every PR.
<br>
<b> SHOT 1 </b>

<img width="1178" height="694" alt="Screenshot From 2026-07-07 22-09-56" src="https://github.com/user-attachments/assets/d382abbe-ee04-4252-b71e-00d2f9a979eb" />

<br><br>

<b> SHOT 2 </b>

<img width="894" height="335" alt="image" src="https://github.com/user-attachments/assets/7066e114-4e8d-4a25-9e4c-8bb427d26be5" />



<br><br>
<b> SHOT 3 </b>
<img width="1178" height="694" alt="Screenshot From 2026-07-07 22-23-11" src="https://github.com/user-attachments/assets/1da2045b-de86-4bbe-87d3-c3abbd8d7605" />


## Acceptance criteria evidence

- **DVBRW-6:** register with name/email/phone; login by email; session persists;
  clear error on invalid input. 
- **DVBRW-7:** view items; arrow-key navigation; each item shows name/price/sizes/
  description; no crash on load. 
- **DVBRW-8:** choose size/milk/sugar/extra shot; customization appears in the
  order summary.

## Stakeholder feedback (this review)

The stakeholder reviewed the increment and raised two requests:

1. **Localise currency to Rwandan Francs.** "Since we are in Rwanda, all prices
   should be shown in Rwandan Francs (RWF), not US dollars."
2. **Personalised greeting after login.** "Beneath the DevBrew logo, show a
   friendly greeting using the user's name — e.g. *'Hi, Joseph — ready for a
   coffee?'*"

Both are accepted into the product backlog for **Sprint 2** (see below).  

## New backlog items (proposed for Sprint 2)

| Key | Story | Est. | Priority |
|-----|-------|------|----------|
| DVBRW-21 | Display prices in Rwandan Francs (RWF) | 2 | High |
| DVBRW-22 | Personalised greeting after login | 1 | Medium |

<!-- **DVBRW-21 - Display prices in Rwandan Francs**
As a user in Rwanda, I want prices shown in RWF so amounts are relevant to me.
- All prices display in RWF (e.g. `RWF 3,000`) instead of USD.
- Menu, customization summary, and totals all use RWF.
- Currency formatting comes from one place (single source of truth).

**DVBRW-22 - Personalised greeting after login**
As a logged-in user, I want a greeting under the logo so the app feels personal.
- After login, a greeting appears beneath the DEVBREW logo.
- It uses the logged-in user's name, e.g. `Hi, Joseph — ready for a coffee?`.
- Shown on the landing/menu screen. -->
