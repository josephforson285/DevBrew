"""Tests for DVBRW-6: register and log into DevBrew.

Each acceptance criterion from the story is covered:
- register using name, email, and phone number
- log in with email
- session is remembered during app usage
- invalid input shows a clear error message
"""

import pytest

from devbrew.errors import AuthError, ValidationError
from devbrew.repositories.user_repository import InMemoryUserRepository
from devbrew.services.auth_service import AuthService


@pytest.fixture
def auth() -> AuthService:
    return AuthService(InMemoryUserRepository())


# --- Acceptance: register using name, email, and phone number -----------------

def test_register_creates_user(auth: AuthService):
    user = auth.register(name="Joseph", email="joseph@example.com", phone="0551234567")

    assert user.name == "Joseph"
    assert user.email == "joseph@example.com"
    assert user.phone == "0551234567"
    assert user.id


def test_register_normalizes_email(auth: AuthService):
    user = auth.register(name="Joseph", email="  Joseph@Example.COM ", phone="0551234567")
    assert user.email == "joseph@example.com"


def test_register_rejects_duplicate_email(auth: AuthService):
    auth.register(name="Joseph", email="joseph@example.com", phone="0551234567")

    with pytest.raises(AuthError, match="already exists"):
        auth.register(name="Imposter", email="joseph@example.com", phone="0559999999")


# --- Acceptance: log in with email --------------------------------------------

def test_login_returns_registered_user(auth: AuthService):
    auth.register(name="Joseph", email="joseph@example.com", phone="0551234567")
    auth.logout()

    user = auth.login("joseph@example.com")
    assert user.email == "joseph@example.com"


def test_login_is_case_insensitive(auth: AuthService):
    auth.register(name="Joseph", email="joseph@example.com", phone="0551234567")
    auth.logout()

    assert auth.login("JOSEPH@example.com").email == "joseph@example.com"


# --- Acceptance: session is remembered during app usage -----------------------

def test_session_started_on_register(auth: AuthService):
    assert auth.is_authenticated is False

    user = auth.register(name="Joseph", email="joseph@example.com", phone="0551234567")

    assert auth.is_authenticated is True
    assert auth.current_user == user


def test_session_persists_across_calls(auth: AuthService):
    auth.register(name="Joseph", email="joseph@example.com", phone="0551234567")

    # A later, unrelated read still sees the same session.
    assert auth.current_user is not None
    assert auth.current_user.name == "Joseph"


def test_logout_clears_session(auth: AuthService):
    auth.register(name="Joseph", email="joseph@example.com", phone="0551234567")
    auth.logout()

    assert auth.is_authenticated is False
    assert auth.current_user is None


# --- Acceptance: invalid input shows a clear error message --------------------

def test_register_rejects_blank_name(auth: AuthService):
    with pytest.raises(ValidationError, match="Name is required"):
        auth.register(name="   ", email="joseph@example.com", phone="0551234567")


@pytest.mark.parametrize("bad_email", ["notanemail", "missing@domain", "@example.com", ""])
def test_register_rejects_invalid_email(auth: AuthService, bad_email: str):
    with pytest.raises(ValidationError, match="valid email"):
        auth.register(name="Joseph", email=bad_email, phone="0551234567")


@pytest.mark.parametrize("bad_phone", ["abc", "123", ""])
def test_register_rejects_invalid_phone(auth: AuthService, bad_phone: str):
    with pytest.raises(ValidationError, match="valid phone"):
        auth.register(name="Joseph", email="joseph@example.com", phone=bad_phone)


def test_login_requires_email(auth: AuthService):
    with pytest.raises(AuthError, match="required"):
        auth.login("")


def test_login_rejects_malformed_email(auth: AuthService):
    with pytest.raises(AuthError, match="valid email"):
        auth.login("notanemail")


def test_login_unknown_email_errors(auth: AuthService):
    with pytest.raises(AuthError, match="No account found"):
        auth.login("stranger@example.com")
