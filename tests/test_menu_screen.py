"""Pilot tests for the menu screen: load and arrow-key navigation (DVBRW-7)."""

from textual.widgets import Input, Static

from devbrew.repositories.user_repository import InMemoryUserRepository
from devbrew.services.auth_service import AuthService
from devbrew.ui.app import DevBrewApp
from devbrew.ui.screens.console import ConsoleScreen
from devbrew.ui.screens.menu import MenuScreen
from devbrew.ui.widgets.arrow_menu import ArrowMenu


def make_app() -> DevBrewApp:
    return DevBrewApp(auth_service=AuthService(InMemoryUserRepository()))


async def _login_to_menu(pilot, app) -> None:
    """Console login -> menu screen."""
    app.auth.register(name="Joseph", email="joseph@example.com", phone="0551234567")
    app.auth.logout()
    await pilot.pause()
    app.query_one("#prompt-input", Input).value = "login joseph@example.com"
    await pilot.press("enter")
    await pilot.pause()


async def test_menu_loads_without_crashing():
    app = make_app()
    async with app.run_test() as pilot:
        await _login_to_menu(pilot, app)

        assert isinstance(app.screen, MenuScreen)
        menu = app.query_one(ArrowMenu)
        assert menu.count >= 3


async def test_greeting_shows_logged_in_user_name():
    app = make_app()
    async with app.run_test() as pilot:
        await _login_to_menu(pilot, app)  # logs in as Joseph

        greeting = str(app.query_one("#greeting", Static).renderable)
        assert "Joseph" in greeting
        assert "coffee" in greeting.lower()


async def test_arrow_keys_move_the_cursor():
    app = make_app()
    async with app.run_test() as pilot:
        await _login_to_menu(pilot, app)

        menu = app.query_one(ArrowMenu)
        assert menu.index == 0
        await pilot.press("down")
        await pilot.pause()
        assert menu.index == 1

        await pilot.press("up")
        await pilot.pause()
        assert menu.index == 0


async def test_escape_returns_to_console():
    app = make_app()
    async with app.run_test() as pilot:
        await _login_to_menu(pilot, app)
        assert isinstance(app.screen, MenuScreen)

        await pilot.press("escape")
        await pilot.pause()
        assert isinstance(app.screen, ConsoleScreen)
