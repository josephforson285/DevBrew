"""MongoDB-backed order repository (DVBRW-11).

Used only when a MongoDB URI is configured. Tests and CI use the in-memory
repository, so this code path never runs without a real database.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from devbrew.models.order import Order
from devbrew.repositories.order_repository import OrderRepository

if TYPE_CHECKING:
    from pymongo.collection import Collection


class MongoOrderRepository(OrderRepository):
    """Store orders in a MongoDB collection, keyed by unique order id."""

    def __init__(self, collection: Collection) -> None:
        self._collection = collection
        self._collection.create_index("id", unique=True)

    def save(self, order: Order) -> Order:
        self._collection.insert_one(order.to_document())
        return order
