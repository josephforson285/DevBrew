# DevBrew

A **terminal coffee ordering app** for developers — Log in, browse the menu,
customize a drink, and place an order, all from a keyboard-driven terminal
console. Just like claude code or lazygit. This is a prototype which is still a work in progress.


> Built to follow **Agile & DevOps** practices (Jira project **DVBRW**): Scrum
> planning, backlog management, a branch-per-story Git workflow, automated
> testing, and CI/CD.
<br>
<img width="1020" height="600" alt="Screenshot From 2026-07-07 20-47-55" src="https://github.com/user-attachments/assets/b1e5393c-2436-44a9-b3f1-579c3dab071b" />

## Status

**Sprint 1 & Sprint 2 complete** — released as **v0.1.0**.

- **Sprint 1:** register/login, browse the coffee menu, customize a drink.
- **Sprint 2:** prices in Rwandan Francs, personalised greeting, shopping cart,
  delivery details, place order (saved to MongoDB), event logging, health check.

See [`docs/`](docs/) for the backlog, product vision, sprint plans, reviews, retrospectives,
architecture, and Definition of Done.

## Features

- **Terminal console** — a `>` prompt for auth and commands, plus arrow-key screens.
- **Auth** — register (name / email / phone) and log in by email; personalised greeting.
- **Menu** — arrow-key list showing name, description, sizes, and price in **RWF**.
- **Customize** — size, milk, sugar, and extra shot, with a live order summary.
- **Cart** — add, change quantity, remove; subtotal & total.
- **Delivery & order** — enter delivery details, review, and place an order
  (unique order ID, **saved to MongoDB Atlas**, terminal confirmation).
- **DevOps** — event logging to a file and a `devbrew health` command.

## Tech stack

Python 3.11+ · [Textual](https://textual.textualize.io/) (TUI) ·
[Typer](https://typer.tiangolo.com/) (CLI) · [Rich](https://rich.readthedocs.io/)
· MongoDB Atlas (via pymongo) · pytest · ruff · GitHub Actions (CI + CD).

## Install

From the published release (no clone needed):

```bash
pip install "https://github.com/josephforson285/DevBrew/releases/download/v0.1.0/devbrew-0.1.0-py3-none-any.whl"
```

Or from source:

```bash
git clone https://github.com/josephforson285/DevBrew.git
cd DevBrew
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

<!-- ## Configure (optional)

DevBrew runs **without a database** by default (in-memory). To persist users and
orders to MongoDB Atlas:

```bash
cp .env.example .env      # then paste your Atlas URI into MONGODB_URI
```

`.env` is gitignored — never commit credentials. -->

## Usage

```bash
devbrew            # launch the terminal app
devbrew --version  # print version
devbrew health     # report application + database status
```

Inside the app: press **Enter** at the splash, then type commands at the `>`
prompt — `register`, `login <email>`, `menu`, `cart`, `help`, `quit`. Navigate
menus with **↑/↓**, select with **Enter** or **Tab**, go back with **Esc**. Events are
logged to `logs/devbrew.log`. At the splash screen you can type `help` for list of commands. The current working prototype is on linux.

## Code Quality

```bash
ruff check .   # lint
pytest         # run tests
```

## CI/CD

- **CI** — GitHub Actions runs `ruff` + `pytest` on every push / pull request to
  `main`; a red run blocks the merge.
- **CD** — pushing a version tag (`vX.Y.Z`) lint+tests, builds the package, and
  publishes a **GitHub Release** with the wheel and sdist.

## Workflow

One feature branch per Jira story (`feature/DVBRW-<n>), small commits
referencing the Jira key (`feat(DVBRW-9): ...`), PR into `main`, merged only when
CI is green. No big-bang commits.

Check out the [Jira backlog](https://amali-tech.atlassian.net/?continue=https%3A%2F%2Famali-tech.atlassian.net%2Fwelcome%2Fsoftware%3FprojectId%3D14816&atlOrigin=eyJpIjoiZjQxZjIyZDU0ODBmNGMxOTliNmUyYWQ5YTYzZDUyNTkiLCJwIjoiamlyYS1zb2Z0d2FyZSJ9).

<!-- ## License -->
