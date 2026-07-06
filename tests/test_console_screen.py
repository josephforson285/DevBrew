"""Pilot tests for the terminal console: prompt REPL auth (DVBRW-6 UI)."""

from textual.widgets import Input

from devbrew.repositories.user_repository import InMemoryUserRepository
from devbrew.services.auth_service import AuthService
from devbrew.ui.app import DevBrewApp
from devbrew.ui.screens.console import ConsoleScreen
from devbrew.ui.screens.menu import MenuScreen


def make_app() -> DevBrewApp:
    return DevBrewApp(auth_service=AuthService(InMemoryUserRepository()))


async def _enter(pilot, app, text: str) -> None:
    """Type a line at the prompt and submit it."""
    app.query_one("#prompt-input", Input).value = text
    await pilot.press("enter")
    await pilot.pause()


async def test_starts_on_console():
    app = make_app()
    async with app.run_test() as pilot:
        await pilot.pause()
        assert isinstance(app.screen, ConsoleScreen)


async def test_register_flow_signs_in_and_opens_menu():
    app = make_app()
    async with app.run_test() as pilot:
        await pilot.pause()
        await _enter(pilot, app, "register")
        await _enter(pilot, app, "Joseph")             # name
        await _enter(pilot, app, "joseph@example.com")  # email
        await _enter(pilot, app, "0551234567")          # phone

        assert app.auth.is_authenticated
        assert app.auth.current_user.email == "joseph@example.com"
        assert isinstance(app.screen, MenuScreen)


async def test_login_command_signs_in():
    app = make_app()
    app.auth.register(name="Joseph", email="joseph@example.com", phone="0551234567")
    app.auth.logout()

    async with app.run_test() as pilot:
        await pilot.pause()
        await _enter(pilot, app, "login joseph@example.com")

        assert app.auth.is_authenticated
        assert isinstance(app.screen, MenuScreen)


async def test_invalid_login_keeps_console_and_no_session():
    app = make_app()
    async with app.run_test() as pilot:
        await pilot.pause()
        await _enter(pilot, app, "login stranger@example.com")

        assert app.auth.is_authenticated is False
        assert isinstance(app.screen, ConsoleScreen)


async def test_menu_command_requires_login():
    app = make_app()
    async with app.run_test() as pilot:
        await pilot.pause()
        await _enter(pilot, app, "menu")
        # Not logged in: still on the console, no crash.
        assert isinstance(app.screen, ConsoleScreen)
