"""Launch the DevBrew interactive terminal UI."""

from __future__ import annotations

from devbrew.logging_config import get_logger, setup_logging
from devbrew.ui.app import DevBrewApp


def run() -> None:
    """Start the DevBrew Textual app with logging configured."""
    setup_logging()
    log = get_logger("app")
    log.info("DevBrew started")
    try:
        DevBrewApp().run()
    except Exception:
        log.exception("unhandled runtime error")
        raise
    finally:
        log.info("DevBrew stopped")


if __name__ == "__main__":
    run()
