"""Domain-level exceptions for DevBrew.

Keeping these in one place lets the UI and CLI layers catch DevBrew errors and
show clear, user-friendly messages instead of raw tracebacks.
"""

from __future__ import annotations


class DevBrewError(Exception):
    """Base class for all DevBrew domain errors."""


class ValidationError(DevBrewError):
    """Raised when user-supplied data fails validation."""


class AuthError(DevBrewError):
    """Raised when registration or login cannot be completed."""
