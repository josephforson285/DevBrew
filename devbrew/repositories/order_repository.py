"""Order repository interface and in-memory implementation (DVBRW-11)."""

from __future__ import annotations

from abc import ABC, abstractmethod

from devbrew.models.order import Order


class OrderRepository(ABC):
    """Abstract storage for placed orders."""

    @abstractmethod
    def save(self, order: Order) -> Order:
        """Persist an order and return it."""


class InMemoryOrderRepository(OrderRepository):
    """Non-persistent order store for local dev, tests, and CI."""

    def __init__(self) -> None:
        self._orders: list[Order] = []

    def save(self, order: Order) -> Order:
        self._orders.append(order)
        return order

    def all(self) -> list[Order]:
        return list(self._orders)
