"""Application logging configuration (DVBRW-18).

Events are written to a rotating log file (``logs/devbrew.log``). We log to a
file rather than the console because the interactive Textual UI owns the
terminal - writing log lines to stdout/stderr would corrupt the display.
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"
_configured = False

# Stay silent until the app configures logging, so importing DevBrew never
# spams stderr (and tests stay clean).
logging.getLogger("devbrew").addHandler(logging.NullHandler())


def get_logger(name: str) -> logging.Logger:
    """Return a namespaced ``devbrew.<name>`` logger."""
    return logging.getLogger(f"devbrew.{name}")


def setup_logging(level: int = logging.INFO) -> Path:
    """Configure file logging once and return the log file path."""
    global _configured
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / "devbrew.log"
    if _configured:
        return log_file

    logger = logging.getLogger("devbrew")
    logger.setLevel(level)
    handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3)
    handler.setFormatter(logging.Formatter(_FORMAT))
    logger.addHandler(handler)
    _configured = True
    return log_file
