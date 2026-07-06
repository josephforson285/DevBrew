"""User repository interface and in-memory implementation (DVBRW-6).

Services depend on the ``UserRepository`` interface, never on a concrete storage
backend. This keeps business logic testable and lets MongoDB Atlas be swapped in
via configuration without changing service code.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from devbrew.models.user import User, normalize_email


class UserRepository(ABC):
    """Abstract storage for users."""

    @abstractmethod
    def add(self, user: User) -> User:
        """Persist a user and return it."""

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        """Return the user with this email, or None if not found."""


class InMemoryUserRepository(UserRepository):
    """Non-persistent user store used for local dev, tests, and CI."""

    def __init__(self) -> None:
        self._by_email: dict[str, User] = {}

    def add(self, user: User) -> User:
        self._by_email[user.email] = user
        return user

    def get_by_email(self, email: str) -> User | None:
        return self._by_email.get(normalize_email(email))
