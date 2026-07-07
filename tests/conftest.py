"""Shared test configuration.

Ensures the whole suite runs without a database: with no MONGODB_URI, the
repository factories return in-memory stores, so tests never touch MongoDB Atlas.
"""

import pytest


@pytest.fixture(autouse=True)
def _no_database(monkeypatch):
    monkeypatch.delenv("MONGODB_URI", raising=False)
