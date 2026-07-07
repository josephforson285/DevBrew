"""Unit tests for the shopping cart (DVBRW-9)."""

from devbrew.models.cart import Cart
from devbrew.models.customization import Customization, CustomizedDrink
from devbrew.models.menu import MenuItem

LATTE = MenuItem("latte", "Latte", "Espresso + steamed milk", 3500, ("M", "L"))


def _drink(size: str = "M", extra: bool = False) -> CustomizedDrink:
    return CustomizedDrink(
        LATTE, Customization(size=size, milk="Oat", sugar="Low", extra_shot=extra)
    )


def test_starts_empty():
    assert Cart().is_empty


def test_add_and_view_items():
    cart = Cart()
    cart.add(_drink())
    assert len(cart.items()) == 1
    assert cart.count == 1


def test_identical_drinks_merge_into_quantity():
    cart = Cart()
    cart.add(_drink())
    cart.add(_drink())
    assert len(cart.items()) == 1
    assert cart.items()[0].quantity == 2


def test_different_customizations_are_separate_lines():
    cart = Cart()
    cart.add(_drink(size="M"))
    cart.add(_drink(size="L"))
    assert len(cart.items()) == 2


def test_update_quantity():
    cart = Cart()
    cart.add(_drink())
    cart.update_quantity(0, 3)
    assert cart.items()[0].quantity == 3


def test_update_quantity_to_zero_removes_item():
    cart = Cart()
    cart.add(_drink())
    cart.update_quantity(0, 0)
    assert cart.is_empty


def test_remove_item():
    cart = Cart()
    cart.add(_drink())
    cart.remove(0)
    assert cart.is_empty


def test_subtotal_and_total():
    cart = Cart()
    cart.add(_drink(extra=True), quantity=2)  # (3500 + 500) * 2 = 8000
    assert cart.subtotal == 8000
    assert cart.total == 8000
    assert cart.items()[0].line_total == 8000
