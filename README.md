# DevBrew ☕

A developer-first **terminal coffee ordering app** — order coffee from your
terminal through a keyboard-driven TUI and CLI, with a modern developer
experience and simulated real-time delivery tracking.

> Built for an **Agile & DevOps** assessment: Scrum planning, backlog
> management, sprint execution, a professional Git workflow, testing, and CI/CD.
> Jira project: **DVBRW**.

## Status

Sprint 1 (active, 2026-07-06 → 2026-07-20) — goal: log in, browse the coffee
menu, and customize a drink.

- **DVBRW-6** Register and log into DevBrew
- **DVBRW-7** Browse the coffee menu using keyboard navigation
- **DVBRW-8** Customize coffee before ordering

See [`docs/`](docs/) for the full backlog, sprint plan, architecture, and
Definition of Done.

## Tech stack

Python 3.11+ · [Textual](https://textual.textualize.io/) (TUI) ·
[Typer](https://typer.tiangolo.com/) (CLI) · [Rich](https://rich.readthedocs.io/)
· MongoDB Atlas (via pymongo) · pytest · ruff · GitHub Actions.

## Getting started

```bash
# 1. Use the project virtual environment (Python 3.14 / MLprojs) or create one:
python -m venv .venv && source .venv/bin/activate

# 2. Install DevBrew with dev tooling
pip install -e ".[dev]"

# 3. Configure environment (optional — app runs in-memory without a DB)
cp .env.example .env    # then paste your MongoDB Atlas URI into .env

# 4. Run
devbrew            # interactive terminal UI (arrives with Sprint 1 stories)
devbrew --version  # print version
```

The app runs **without a database** by default (in-memory repository). Set
`MONGODB_URI` in `.env` to persist to MongoDB Atlas. `.env` is gitignored —
never commit credentials.

## Development

```bash
ruff check .       # lint
pytest             # run tests
```

CI (GitHub Actions) runs ruff + pytest on every push and pull request.

## Contributing / workflow

One feature branch per Jira story (`feature/DVBRW-<n>-<slug>`), small commits
referencing the Jira key (`feat(DVBRW-6): ...`), PR into `main`, merge only when
CI is green. No big-bang commits. See [`docs/AI_CONTEXT.md`](docs/AI_CONTEXT.md).

## License

MIT
