"""Repository factory: choose storage backend from configuration (DVBRW-6).

With a ``MONGODB_URI`` configured, repositories are backed by MongoDB Atlas;
otherwise an in-memory store is used (local dev, tests, CI).
"""

from __future__ import annotations

from devbrew.config import Settings, get_settings
from devbrew.repositories.order_repository import InMemoryOrderRepository, OrderRepository
from devbrew.repositories.user_repository import InMemoryUserRepository, UserRepository


def build_user_repository(settings: Settings | None = None) -> UserRepository:
    """Return a user repository appropriate for the current configuration."""
    settings = settings or get_settings()

    if settings.has_database:
        # Imported lazily so the MongoDB path is only loaded when configured.
        from devbrew.database.mongo import get_database
        from devbrew.repositories.mongo_user_repository import MongoUserRepository

        database = get_database(settings)
        return MongoUserRepository(database["users"])

    return InMemoryUserRepository()


def build_order_repository(settings: Settings | None = None) -> OrderRepository:
    """Return an order repository appropriate for the current configuration."""
    settings = settings or get_settings()

    if settings.has_database:
        from devbrew.database.mongo import get_database
        from devbrew.repositories.mongo_order_repository import MongoOrderRepository

        database = get_database(settings)
        return MongoOrderRepository(database["orders"])

    return InMemoryOrderRepository()
