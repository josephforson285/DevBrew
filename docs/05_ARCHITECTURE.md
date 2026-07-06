# 05 - Architecture

DevBrew uses a **modular, layered** architecture. Terminal screens are kept
separate from business logic, and business logic is kept separate from database
access. This makes the app easy to test and lets CI verify it without a live DB.

## Layers

- **Presentation** - Textual screens and widgets (`devbrew/ui/`).
- **CLI** - Typer commands: `devbrew`, `devbrew menu`, `devbrew track`,
  `devbrew history`, `devbrew health` (`devbrew/cli.py`).
- **Application (services)** - authentication, menu browsing, customization,
  ordering, tracking, logging, health (`devbrew/services/`).
- **Persistence (repositories)** - read/write through a repository interface
  (`devbrew/repositories/`). A MongoDB implementation (via pymongo) is used when
  `MONGODB_URI` is set; an in-memory implementation is used otherwise (tests/CI).
- **Models** - plain data models for user, menu, order (`devbrew/models/`).

## Key principle: repository abstraction

Services depend on a repository **interface**, not on pymongo directly. This
means:

- Unit tests and CI run against an in-memory repository (fast, no network).
- Swapping to MongoDB Atlas is a configuration change, not a code change.
- Secrets stay out of the codebase.

## Planned package layout

```
devbrew/
  __init__.py
  main.py            # launches the interactive TUI
  cli.py             # Typer command entry point
  config.py          # env/.env configuration
  logging_config.py  # logging setup (later story)
  ui/                # app.py, screens/, widgets/
  models/            # user.py, menu.py, order.py
  services/          # auth_service.py, menu_service.py, order_service.py
  repositories/      # user_repository.py, menu_repository.py, order_repository.py
  database/          # mongo.py
tests/
.github/workflows/ci.yml
```
