"""Menu repository: source of coffee menu data (DVBRW-7).

The menu is static reference data for the prototype, so a built-in catalog is
used. It sits behind a repository interface like the other stores, so it could
later be sourced from MongoDB without changing the service or UI.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from devbrew.models.menu import MenuItem

_DEFAULT_MENU: tuple[MenuItem, ...] = (
    MenuItem("espresso", "Espresso", "Strong and bold shot", 2.50, ("S", "M")),
    MenuItem("americano", "Americano", "Espresso + hot water", 3.00, ("S", "M", "L")),
    MenuItem("latte", "Latte", "Espresso + steamed milk", 3.50, ("M", "L")),
    MenuItem("cappuccino", "Cappuccino", "Espresso + milk foam", 3.75, ("M", "L")),
    MenuItem("flat-white", "Flat White", "Smooth and creamy", 3.60, ("M",)),
    MenuItem("mocha", "Mocha", "Espresso + chocolate", 4.00, ("M", "L")),
    MenuItem("cold-brew", "Cold Brew", "Chilled and refreshing", 3.75, ("M", "L")),
)


class MenuRepository(ABC):
    """Abstract source of menu items."""

    @abstractmethod
    def list_items(self) -> list[MenuItem]:
        """Return all available menu items."""


class StaticMenuRepository(MenuRepository):
    """Serves the built-in coffee catalog."""

    def list_items(self) -> list[MenuItem]:
        return list(_DEFAULT_MENU)
