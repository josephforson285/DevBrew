"""Menu service: browse the coffee menu (DVBRW-7)."""

from __future__ import annotations

from devbrew.models.menu import MenuItem
from devbrew.repositories.menu_repository import MenuRepository, StaticMenuRepository


class MenuService:
    """Provides the coffee menu to the UI and CLI."""

    def __init__(self, repository: MenuRepository | None = None) -> None:
        self._repository = repository or StaticMenuRepository()

    def list_items(self) -> list[MenuItem]:
        """Return all available coffee items."""
        return self._repository.list_items()
