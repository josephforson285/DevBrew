"""MongoDB Atlas connection helper.

The client is created lazily and only when a ``MONGODB_URI`` is configured, so
importing this module never forces a network connection (keeps tests/CI offline).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from devbrew.config import Settings, get_settings

if TYPE_CHECKING:
    from pymongo.database import Database


def get_database(settings: Settings | None = None) -> Database:
    """Return the configured MongoDB database.

    Raises:
        RuntimeError: if no ``MONGODB_URI`` is configured.
    """
    settings = settings or get_settings()
    if not settings.mongodb_uri:
        raise RuntimeError("MONGODB_URI is not configured; cannot connect to MongoDB.")

    # Imported here so pymongo is only needed when a database is actually used.
    from pymongo import MongoClient

    client: MongoClient = MongoClient(settings.mongodb_uri)
    return client[settings.mongodb_db]
