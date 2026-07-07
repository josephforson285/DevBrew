"""Unit tests for placing orders (DVBRW-11)."""

from devbrew.models.cart import Cart
from devbrew.models.customization import Customization, CustomizedDrink
from devbrew.models.delivery import DeliveryDetails
from devbrew.models.menu import MenuItem
from devbrew.models.user import User
from devbrew.repositories.order_repository import InMemoryOrderRepository
from devbrew.services.order_service import OrderService

LATTE = MenuItem("latte", "Latte", "Espresso + steamed milk", 3500, ("M", "L"))


def _cart() -> Cart:
    cart = Cart()
    cart.add(
        CustomizedDrink(LATTE, Customization("M", "Oat", "Low", True)), quantity=2
    )  # (3500 + 500) * 2 = 8000
    return cart


def _delivery() -> DeliveryDetails:
    return DeliveryDetails.create(name="Joseph", phone="0551234567", address="KG 11 Ave")


def _user() -> User:
    return User(name="Joseph", email="j@example.com", phone="0551234567")


def test_place_order_creates_order_with_id_and_total():
    service = OrderService(InMemoryOrderRepository())
    order = service.place_order(user=_user(), cart=_cart(), delivery=_delivery())

    assert order.id.startswith("DVB-")
    assert order.total == 8000
    assert order.user_email == "j@example.com"
    assert len(order.items) == 1
    assert order.items[0]["quantity"] == 2


def test_order_ids_are_unique():
    service = OrderService(InMemoryOrderRepository())
    order1 = service.place_order(user=_user(), cart=_cart(), delivery=_delivery())
    order2 = service.place_order(user=_user(), cart=_cart(), delivery=_delivery())
    assert order1.id != order2.id


def test_place_order_saves_and_clears_cart():
    repository = InMemoryOrderRepository()
    service = OrderService(repository)
    cart = _cart()

    service.place_order(user=_user(), cart=cart, delivery=_delivery())

    assert cart.is_empty
    assert len(repository.all()) == 1


def test_order_serialises_to_document():
    order = OrderService(InMemoryOrderRepository()).place_order(
        user=_user(), cart=_cart(), delivery=_delivery()
    )
    document = order.to_document()

    assert document["id"] == order.id
    assert document["delivery"]["address"] == "KG 11 Ave"
    assert document["total"] == 8000
    assert isinstance(document["created_at"], str)
