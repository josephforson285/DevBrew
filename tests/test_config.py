"""Smoke tests for configuration loading."""

from devbrew import __version__
from devbrew.config import get_settings


def test_version_is_set():
    assert __version__ == "0.1.0"


def test_defaults_without_env(monkeypatch):
    monkeypatch.delenv("MONGODB_URI", raising=False)
    monkeypatch.delenv("MONGODB_DB", raising=False)
    monkeypatch.delenv("DEVBREW_ENV", raising=False)

    settings = get_settings()

    assert settings.mongodb_uri is None
    assert settings.mongodb_db == "devbrew"
    assert settings.env == "development"
    assert settings.has_database is False


def test_reads_env_values(monkeypatch):
    monkeypatch.setenv("MONGODB_URI", "mongodb+srv://example")
    monkeypatch.setenv("MONGODB_DB", "devbrew_test")
    monkeypatch.setenv("DEVBREW_ENV", "test")

    settings = get_settings()

    assert settings.mongodb_uri == "mongodb+srv://example"
    assert settings.mongodb_db == "devbrew_test"
    assert settings.env == "test"
    assert settings.has_database is True
