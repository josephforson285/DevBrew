# 04 - Tech Stack

| Area | Tool |
|------|------|
| Language | Python 3.11+ (local dev on 3.14) |
| Terminal UI | Textual |
| CLI commands | Typer |
| Terminal styling | Rich |
| Database | MongoDB (Atlas) |
| Database driver | pymongo |
| Testing | pytest |
| Coverage | pytest-cov |
| Code quality | ruff |
| Logging | Python `logging` module |
| CI/CD | GitHub Actions |
| Packaging | pyproject.toml |
| Version control | Git + GitHub |
| Agile tracking | Jira |

## Environment notes

- Local development uses the `MLprojs` virtual environment (Python 3.14).
- CI pins Python **3.14** so the pipeline matches local development.
- The MongoDB Atlas connection string lives in a gitignored `.env` file
  (see `.env.example`). It is **never** committed.
- Tests and CI run **without** a live database: services talk to a repository
  abstraction backed by an in-memory store when no `MONGODB_URI` is set.
