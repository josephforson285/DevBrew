"""Tests for the health check (DVBRW-19)."""

from typer.testing import CliRunner

from devbrew.cli import app
from devbrew.config import Settings
from devbrew.services import health_service
from devbrew.services.health_service import (
    CONNECTED,
    NOT_CONFIGURED,
    UNAVAILABLE,
    HealthReport,
    check_health,
)

runner = CliRunner()


def test_health_without_database():
    # conftest clears MONGODB_URI, so the DB is "not configured".
    report = check_health()
    assert report.app_ok is True
    assert report.db_status == NOT_CONFIGURED
    assert report.healthy is True


def test_report_healthy_property():
    ok = HealthReport(True, "app", CONNECTED, "db")
    bad = HealthReport(True, "app", UNAVAILABLE, "err")
    assert ok.healthy is True
    assert bad.healthy is False


def test_check_database_reports_unavailable_on_bad_uri():
    settings = Settings(mongodb_uri="mongodb://127.0.0.1:1/", mongodb_db="devbrew", env="test")
    status, _ = health_service._check_database(settings)
    assert status == UNAVAILABLE


def test_health_command_runs_and_is_readable():
    result = runner.invoke(app, ["health"])
    assert result.exit_code == 0
    assert "Application" in result.stdout
    assert "Database" in result.stdout


def test_health_command_exits_nonzero_when_unavailable(monkeypatch):
    monkeypatch.setattr(
        health_service,
        "check_health",
        lambda settings=None: HealthReport(True, "app", UNAVAILABLE, "err"),
    )
    result = runner.invoke(app, ["health"])
    assert result.exit_code == 1
