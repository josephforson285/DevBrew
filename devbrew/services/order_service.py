"""Order service: place an order (DVBRW-11)."""

from __future__ import annotations

from devbrew.models.cart import Cart
from devbrew.models.delivery import DeliveryDetails
from devbrew.models.order import Order
from devbrew.models.user import User
from devbrew.repositories.order_repository import InMemoryOrderRepository, OrderRepository


class OrderService:
    """Turns a cart plus delivery details into a saved order."""

    def __init__(self, repository: OrderRepository | None = None) -> None:
        self._repository = repository or InMemoryOrderRepository()

    def place_order(self, user: User, cart: Cart, delivery: DeliveryDetails) -> Order:
        """Create an order from the cart, persist it, and clear the cart."""
        items = [
            {
                "name": item.drink.item.name,
                "descriptor": item.drink.descriptor,
                "quantity": item.quantity,
                "unit_price": item.drink.total_price,
                "line_total": item.line_total,
            }
            for item in cart.items()
        ]
        order = Order(
            user_email=user.email,
            items=items,
            delivery=delivery,
            total=cart.total,
        )
        self._repository.save(order)
        cart.clear()
        return order
