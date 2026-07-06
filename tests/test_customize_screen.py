"""Pilot tests for the customization screen (DVBRW-8)."""

from textual.widgets import Input, Static

from devbrew.repositories.user_repository import InMemoryUserRepository
from devbrew.services.auth_service import AuthService
from devbrew.ui.app import DevBrewApp
from devbrew.ui.screens.customize import CustomizeScreen
from devbrew.ui.widgets.option_picker import OptionPicker


def make_app() -> DevBrewApp:
    return DevBrewApp(auth_service=AuthService(InMemoryUserRepository()))


async def _to_customize(pilot, app) -> None:
    """Login -> menu -> Enter on the first item -> customize screen."""
    app.auth.register(name="Joseph", email="joseph@example.com", phone="0551234567")
    app.auth.logout()
    await pilot.pause()
    app.query_one("#prompt-input", Input).value = "login joseph@example.com"
    await pilot.press("enter")
    await pilot.pause()
    await pilot.press("enter")  # select first menu item
    await pilot.pause()


async def test_enter_opens_customize_screen():
    app = make_app()
    async with app.run_test() as pilot:
        await _to_customize(pilot, app)
        assert isinstance(app.screen, CustomizeScreen)


async def test_all_four_choices_are_adjustable():
    app = make_app()
    async with app.run_test() as pilot:
        await _to_customize(pilot, app)
        picker = app.query_one(OptionPicker)

        # Acceptance: choose size, milk, sugar, extra shot.
        # Row 0 = Size: cycle value with right arrow.
        before = picker.choices["Size"]
        await pilot.press("right")
        await pilot.pause()
        assert picker.choices["Size"] != before

        # Move to Milk, Sugar, Extra shot and change each.
        await pilot.press("down")   # Milk
        await pilot.press("right")
        await pilot.press("down")   # Sugar
        await pilot.press("right")
        await pilot.press("down")   # Extra shot
        await pilot.press("right")
        await pilot.pause()

        assert picker.choices["Milk"] != "Whole"
        assert picker.choices["Sugar"] != "None"
        assert picker.choices["Extra shot"] == "Yes"


async def test_summary_reflects_choices():
    app = make_app()
    async with app.run_test() as pilot:
        await _to_customize(pilot, app)

        # Turn on extra shot (row 3).
        await pilot.press("down")
        await pilot.press("down")
        await pilot.press("down")
        await pilot.press("right")
        await pilot.pause()

        summary = str(app.query_one("#summary", Static).renderable)
        assert "Yes" in summary          # extra shot appears in the summary
        assert "Extra shot" in summary


async def test_escape_returns_to_menu():
    app = make_app()
    async with app.run_test() as pilot:
        await _to_customize(pilot, app)
        assert isinstance(app.screen, CustomizeScreen)

        await pilot.press("escape")
        await pilot.pause()
        assert not isinstance(app.screen, CustomizeScreen)
