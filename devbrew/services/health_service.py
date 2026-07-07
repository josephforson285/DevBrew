"""Health check service (DVBRW-19).

Reports application status and whether the configured database is reachable.
Safe to run without logging in, and never raises - a failing DB just reports
"unavailable" so the command can be used to diagnose an outage.
"""

from __future__ import annotations

from dataclasses import dataclass

from devbrew import __version__
from devbrew.config import Settings, get_settings

# Database states.
CONNECTED = "connected"
NOT_CONFIGURED = "not configured"
UNAVAILABLE = "unavailable"


@dataclass
class HealthReport:
    app_ok: bool
    app_detail: str
    db_status: str
    db_detail: str

    @property
    def healthy(self) -> bool:
        return self.app_ok and self.db_status != UNAVAILABLE


def _check_database(settings: Settings) -> tuple[str, str]:
    if not settings.has_database:
        return NOT_CONFIGURED, "no MONGODB_URI set (using in-memory storage)"
    try:
        from pymongo import MongoClient

        client = MongoClient(settings.mongodb_uri, serverSelectionTimeoutMS=3000)
        client.admin.command("ping")
        version = client.server_info().get("version", "unknown")
        return CONNECTED, f"MongoDB {version} (db: {settings.mongodb_db})"
    except Exception as exc:
        return UNAVAILABLE, type(exc).__name__


def check_health(settings: Settings | None = None) -> HealthReport:
    """Build a health report for the application and its database."""
    settings = settings or get_settings()
    db_status, db_detail = _check_database(settings)
    return HealthReport(
        app_ok=True,
        app_detail=f"DevBrew {__version__}",
        db_status=db_status,
        db_detail=db_detail,
    )
