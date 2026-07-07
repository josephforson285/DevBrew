"""Pilot tests for the delivery details flow (DVBRW-10)."""

from textual.widgets import Input

from devbrew.repositories.user_repository import InMemoryUserRepository
from devbrew.services.auth_service import AuthService
from devbrew.ui.app import DevBrewApp
from devbrew.ui.screens.delivery import DeliveryScreen


def make_app() -> DevBrewApp:
    return DevBrewApp(auth_service=AuthService(InMemoryUserRepository()))


async def _to_delivery(pilot, app) -> None:
    """Login -> menu -> customize -> add to cart -> cart -> checkout."""
    app.auth.register(name="Joseph", email="j@example.com", phone="0551234567")
    app.auth.logout()
    await pilot.pause()
    app.query_one("#prompt-input", Input).value = "login j@example.com"
    await pilot.press("enter")
    await pilot.pause()
    await pilot.press("enter")   # customize first item
    await pilot.pause()
    await pilot.press("enter")   # confirm -> add to cart -> back to menu
    await pilot.pause()
    await pilot.press("c")       # open cart
    await pilot.pause()
    await pilot.press("enter")   # checkout -> delivery
    await pilot.pause()


async def _enter(pilot, app, text: str) -> None:
    app.query_one("#delivery-input", Input).value = text
    await pilot.press("enter")
    await pilot.pause()


async def test_checkout_opens_delivery():
    app = make_app()
    async with app.run_test() as pilot:
        await _to_delivery(pilot, app)
        assert isinstance(app.screen, DeliveryScreen)


async def test_entering_details_saves_them():
    app = make_app()
    async with app.run_test() as pilot:
        await _to_delivery(pilot, app)
        await _enter(pilot, app, "Joseph")        # name
        await _enter(pilot, app, "0551234567")    # phone
        await _enter(pilot, app, "KG 11 Ave")     # address
        await _enter(pilot, app, "Gate 2")        # instructions

        assert app.delivery is not None
        assert app.delivery.name == "Joseph"
        assert app.delivery.address == "KG 11 Ave"


async def test_invalid_phone_reprompts_without_advancing():
    app = make_app()
    async with app.run_test() as pilot:
        await _to_delivery(pilot, app)
        await _enter(pilot, app, "Joseph")   # name accepted
        await _enter(pilot, app, "abc")      # invalid phone -> stays on phone

        # A valid phone now should still be accepted (we didn't skip the field).
        await _enter(pilot, app, "0551234567")
        await _enter(pilot, app, "KG 11 Ave")
        await _enter(pilot, app, "")          # optional instructions

        assert app.delivery is not None
        assert app.delivery.phone == "0551234567"
