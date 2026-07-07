# Sprint 2 - Plan

- **Sprint:** DVBRW Sprint 2
- **Window:** 2026-07-20 → 2026-08-03
- **Committed:** 7 stories, 20 story points
- **Goal:** Implement stakeholder feedback, complete the cart, and improve DevOps visibility.

## Committed work

| Key      | Story                                   | Pts | Priority | Source                   |
| -------- | --------------------------------------- | --- | -------- | ------------------------ |
| DVBRW-21 | Display prices in Rwandan Francs (RWF)  | 2   | Highest  | Sprint 1 Review feedback |
| DVBRW-22 | Personalised greeting after login       | 1   | High     | Sprint 1 Review feedback |
| DVBRW-9  | Add drinks to shopping cart             | 3   | High     | Product backlog          |
| DVBRW-10 | Enter delivery address and phone number | 2   | High     | Product backlog          |
| DVBRW-11 | Confirm and place order                 | 5   | High     | Product backlog          |
| DVBRW-18 | Record application events in logs       | 5   | Low      | DevOps improvement       |
| DVBRW-19 | Add health check command                | 2   | Low      | DevOps monitoring        |

## Acceptance criteria

See each story in [Jira backlog](https://amali-tech.atlassian.net/?continue=https%3A%2F%2Famali-tech.atlassian.net%2Fwelcome%2Fsoftware%3FprojectId%3D14816&atlOrigin=eyJpIjoiZjQxZjIyZDU0ODBmNGMxOTliNmUyYWQ5YTYzZDUyNTkiLCJwIjoiamlyYS1zb2Z0d2FyZSJ9).

Key points:

- DVBRW-21: all prices (menu, customization, totals) shown in RWF.
- DVBRW-22: greeting under the logo using the logged-in user's name.
- DVBRW-9: add/view/update-quantity/remove cart items; subtotal & total.
- DVBRW-10: enter name/phone/address (+optional instructions); required fields validated.
- DVBRW-11: review order, unique order ID, **saved to MongoDB**, terminal confirmation.
- DVBRW-18: log login, order creation, status changes, and errors to a log file.
- DVBRW-19: `devbrew health` reports application and database status, readably.

## Development order

1. DVBRW-21, DVBRW-22 - quick, high-value stakeholder items.
2. DVBRW-9 → DVBRW-10 → DVBRW-11 - the order flow (cart → delivery → place & persist).
3. DVBRW-18, DVBRW-19 - DevOps visibility (logging, health).

<br><br>

<b> Evidence of Sprint 2 jira workflow </b>
<img width="1167" height="726" alt="image" src="https://github.com/user-attachments/assets/892a0eae-e914-422b-8b87-086d3914fe13" />

