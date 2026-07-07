"""Shopping cart (DVBRW-9).

Session-scoped, in-memory cart of customized drinks. Identical drinks (same item
and same customization) are merged into one line with a higher quantity.
"""

from __future__ import annotations

from dataclasses import dataclass

from devbrew.models.customization import CustomizedDrink
from devbrew.money import format_price


@dataclass
class CartItem:
    drink: CustomizedDrink
    quantity: int = 1

    @property
    def line_total(self) -> float:
        return self.drink.total_price * self.quantity

    @property
    def line_total_label(self) -> str:
        return format_price(self.line_total)


class Cart:
    """A user's shopping cart for the current session."""

    def __init__(self) -> None:
        self._items: list[CartItem] = []

    def add(self, drink: CustomizedDrink, quantity: int = 1) -> None:
        for item in self._items:
            if item.drink == drink:
                item.quantity += quantity
                return
        self._items.append(CartItem(drink, quantity))

    def items(self) -> list[CartItem]:
        return list(self._items)

    def update_quantity(self, index: int, quantity: int) -> None:
        if quantity <= 0:
            self.remove(index)
            return
        self._items[index].quantity = quantity

    def remove(self, index: int) -> None:
        del self._items[index]

    def clear(self) -> None:
        self._items.clear()

    @property
    def is_empty(self) -> bool:
        return not self._items

    @property
    def count(self) -> int:
        return sum(item.quantity for item in self._items)

    @property
    def subtotal(self) -> float:
        return sum(item.line_total for item in self._items)

    @property
    def total(self) -> float:
        return self.subtotal
