"""Pilot tests for the order review / place-order flow (DVBRW-11)."""

from textual.widgets import Input

from devbrew.repositories.order_repository import InMemoryOrderRepository
from devbrew.repositories.user_repository import InMemoryUserRepository
from devbrew.services.auth_service import AuthService
from devbrew.services.order_service import OrderService
from devbrew.ui.app import DevBrewApp
from devbrew.ui.screens.menu import MenuScreen
from devbrew.ui.screens.order_review import OrderReviewScreen


def make_app() -> DevBrewApp:
    return DevBrewApp(
        auth_service=AuthService(InMemoryUserRepository()),
        order_service=OrderService(InMemoryOrderRepository()),
    )


async def _to_review(pilot, app) -> None:
    app.auth.register(name="Joseph", email="j@example.com", phone="0551234567")
    app.auth.logout()
    await pilot.pause()
    app.query_one("#prompt-input", Input).value = "login j@example.com"
    await pilot.press("enter")
    await pilot.pause()
    await pilot.press("enter")   # customize first item
    await pilot.pause()
    await pilot.press("enter")   # confirm -> add to cart -> menu
    await pilot.pause()
    await pilot.press("c")       # cart
    await pilot.pause()
    await pilot.press("enter")   # checkout -> delivery
    await pilot.pause()
    for field in ("Joseph", "0551234567", "KG 11 Ave", ""):
        app.query_one("#delivery-input", Input).value = field
        await pilot.press("enter")
        await pilot.pause()


async def test_delivery_flows_into_review():
    app = make_app()
    async with app.run_test() as pilot:
        await _to_review(pilot, app)
        assert isinstance(app.screen, OrderReviewScreen)


async def test_place_order_generates_id_and_clears_cart():
    app = make_app()
    async with app.run_test() as pilot:
        await _to_review(pilot, app)
        assert not app.cart.is_empty

        await pilot.press("enter")   # place order
        await pilot.pause()

        review = app.screen
        assert isinstance(review, OrderReviewScreen)
        assert review._order is not None
        assert review._order.id.startswith("DVB-")
        assert app.cart.is_empty          # cart cleared after placing


async def test_confirmation_then_return_to_menu():
    app = make_app()
    async with app.run_test() as pilot:
        await _to_review(pilot, app)
        await pilot.press("enter")   # place
        await pilot.pause()
        await pilot.press("enter")   # return to menu
        await pilot.pause()
        assert isinstance(app.screen, MenuScreen)
