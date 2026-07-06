"""Authentication service: registration, login, and session (DVBRW-6).

Holds the currently logged-in user for the duration of app usage so the session
is "remembered" while DevBrew is running.
"""

from __future__ import annotations

from devbrew.errors import AuthError
from devbrew.models.user import User, is_valid_email, normalize_email
from devbrew.repositories.user_repository import UserRepository


class AuthService:
    """Coordinates user registration, login, and the in-app session."""

    def __init__(self, users: UserRepository) -> None:
        self._users = users
        self._current_user: User | None = None

    @property
    def current_user(self) -> User | None:
        """The user logged in for this session, or None."""
        return self._current_user

    @property
    def is_authenticated(self) -> bool:
        """True while a user is logged in."""
        return self._current_user is not None

    def register(self, name: str, email: str, phone: str) -> User:
        """Register a new user and start their session.

        Raises:
            ValidationError: if name, email, or phone is invalid.
            AuthError: if the email is already registered.
        """
        user = User.create(name=name, email=email, phone=phone)
        if self._users.get_by_email(user.email) is not None:
            raise AuthError("An account with this email already exists. Try logging in.")

        self._users.add(user)
        self._current_user = user
        return user

    def login(self, email: str) -> User:
        """Log a user in by email and start their session.

        Raises:
            AuthError: if the email is missing, malformed, or not registered.
        """
        if not email or not email.strip():
            raise AuthError("Email is required to log in.")
        if not is_valid_email(email):
            raise AuthError("Please enter a valid email address.")

        user = self._users.get_by_email(normalize_email(email))
        if user is None:
            raise AuthError("No account found for that email. Please register first.")

        self._current_user = user
        return user

    def logout(self) -> None:
        """End the current session."""
        self._current_user = None
