"""User domain model and input validation (DVBRW-6)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from uuid import uuid4

from devbrew.errors import ValidationError

# Deliberately permissive email check: one @, a dot in the domain, no spaces.
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def normalize_email(email: str) -> str:
    """Trim surrounding whitespace and lower-case an email for consistent lookup."""
    return email.strip().lower()


def is_valid_email(email: str) -> bool:
    """Return True if the email has a plausible ``local@domain.tld`` shape."""
    return bool(_EMAIL_RE.match(email.strip()))


def is_valid_phone(phone: str) -> bool:
    """Return True if the phone number has 7-15 digits (ignoring spaces/punctuation)."""
    digits = re.sub(r"[\s\-()+]", "", phone)
    return digits.isdigit() and 7 <= len(digits) <= 15


@dataclass(frozen=True)
class User:
    """A registered DevBrew user."""

    name: str
    email: str
    phone: str
    id: str = field(default_factory=lambda: uuid4().hex)

    @classmethod
    def create(cls, name: str, email: str, phone: str) -> User:
        """Validate raw input and build a normalized User.

        Raises:
            ValidationError: if the name, email, or phone number is invalid.
        """
        name = name.strip()
        email = normalize_email(email)
        phone = phone.strip()

        if not name:
            raise ValidationError("Name is required.")
        if not is_valid_email(email):
            raise ValidationError("Please enter a valid email address.")
        if not is_valid_phone(phone):
            raise ValidationError("Please enter a valid phone number.")

        return cls(name=name, email=email, phone=phone)
