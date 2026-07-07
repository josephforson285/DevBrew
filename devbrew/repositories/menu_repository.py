"""Menu repository: source of coffee menu data (DVBRW-7).

The menu is static reference data for the prototype, so a built-in catalog is
used. It sits behind a repository interface like the other stores, so it could
later be sourced from MongoDB without changing the service or UI.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from devbrew.models.menu import MenuItem

# Prices are in Rwandan Francs (RWF).
_DEFAULT_MENU: tuple[MenuItem, ...] = (
    MenuItem("espresso", "Espresso", "Strong and bold shot", 2500, ("S", "M")),
    MenuItem("americano", "Americano", "Espresso + hot water", 3000, ("S", "M", "L")),
    MenuItem("latte", "Latte", "Espresso + steamed milk", 3500, ("M", "L")),
    MenuItem("cappuccino", "Cappuccino", "Espresso + milk foam", 3750, ("M", "L")),
    MenuItem("flat-white", "Flat White", "Smooth and creamy", 3600, ("M",)),
    MenuItem("mocha", "Mocha", "Espresso + chocolate", 4000, ("M", "L")),
    MenuItem("cold-brew", "Cold Brew", "Chilled and refreshing", 3750, ("M", "L")),
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
