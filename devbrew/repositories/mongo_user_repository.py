"""MongoDB-backed user repository (DVBRW-6).

Used only when a MongoDB URI is configured. Unit tests and CI use the in-memory
repository instead, so this code path never runs without a real database.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from devbrew.models.user import User, normalize_email
from devbrew.repositories.user_repository import UserRepository

if TYPE_CHECKING:
    from pymongo.collection import Collection


class MongoUserRepository(UserRepository):
    """Store users in a MongoDB collection, keyed by unique email."""

    def __init__(self, collection: Collection) -> None:
        self._collection = collection
        self._collection.create_index("email", unique=True)

    def add(self, user: User) -> User:
        self._collection.update_one(
            {"email": user.email},
            {
                "$setOnInsert": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "phone": user.phone,
                }
            },
            upsert=True,
        )
        return user

    def get_by_email(self, email: str) -> User | None:
        doc = self._collection.find_one({"email": normalize_email(email)})
        if doc is None:
            return None
        return User(name=doc["name"], email=doc["email"], phone=doc["phone"], id=doc["id"])
