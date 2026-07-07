"""Pilot tests for the cart flow (DVBRW-9)."""

from textual.widgets import Input

from devbrew.repositories.user_repository import InMemoryUserRepository
from devbrew.services.auth_service import AuthService
from devbrew.ui.app import DevBrewApp
from devbrew.ui.screens.cart import CartScreen
from devbrew.ui.widgets.cart_view import CartView


def make_app() -> DevBrewApp:
    return DevBrewApp(auth_service=AuthService(InMemoryUserRepository()))


async def _login_to_menu(pilot, app) -> None:
    app.auth.register(name="Joseph", email="j@example.com", phone="0551234567")
    app.auth.logout()
    await pilot.pause()
    app.query_one("#prompt-input", Input).value = "login j@example.com"
    await pilot.press("enter")
    await pilot.pause()


async def _add_first_drink(pilot) -> None:
    await pilot.press("enter")   # open customize for the highlighted item
    await pilot.pause()
    await pilot.press("enter")   # confirm -> add to cart -> back to menu
    await pilot.pause()


async def test_confirm_adds_to_cart():
    app = make_app()
    async with app.run_test() as pilot:
        await _login_to_menu(pilot, app)
        await _add_first_drink(pilot)
        assert app.cart.count == 1


async def test_c_opens_cart_screen():
    app = make_app()
    async with app.run_test() as pilot:
        await _login_to_menu(pilot, app)
        await _add_first_drink(pilot)
        await pilot.press("c")
        await pilot.pause()
        assert isinstance(app.screen, CartScreen)


async def test_quantity_increase_and_remove():
    app = make_app()
    async with app.run_test() as pilot:
        await _login_to_menu(pilot, app)
        await _add_first_drink(pilot)
        await pilot.press("c")
        await pilot.pause()

        # Increase quantity of the selected line.
        await pilot.press("right")
        await pilot.pause()
        assert app.cart.items()[0].quantity == 2

        # Remove it.
        app.query_one(CartView)  # ensure it's mounted/focused
        await pilot.press("x")
        await pilot.pause()
        assert app.cart.is_empty
