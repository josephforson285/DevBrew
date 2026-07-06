"""Central configuration for DevBrew, loaded from environment / .env.

Reading configuration in one place keeps secrets (the MongoDB Atlas URI) out
of the code and lets tests and CI run without a real database.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Load variables from a local .env file if present. In CI / production the
# real environment variables take precedence; a missing .env is fine.
load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Immutable snapshot of the app's runtime configuration."""

    mongodb_uri: str | None
    mongodb_db: str
    env: str

    @property
    def has_database(self) -> bool:
        """True when a MongoDB URI is configured; otherwise use in-memory storage."""
        return bool(self.mongodb_uri)


def get_settings() -> Settings:
    """Build a Settings object from the current environment."""
    uri = os.getenv("MONGODB_URI") or None
    return Settings(
        mongodb_uri=uri,
        mongodb_db=os.getenv("MONGODB_DB", "devbrew"),
        env=os.getenv("DEVBREW_ENV", "development"),
    )
