"""DevBrew Textual application shell (terminal console + arrow-key menu)."""

from __future__ import annotations

from pathlib import Path

from textual.app import App
from textual.binding import Binding

from devbrew.models.cart import Cart
from devbrew.repositories.factory import build_user_repository
from devbrew.services.auth_service import AuthService
from devbrew.services.menu_service import MenuService
from devbrew.ui.screens.console import ConsoleScreen


class DevBrewApp(App):
    """Top-level app: owns the auth session and menu, routes screens."""

    CSS_PATH = Path(__file__).parent / "styles.tcss"
    TITLE = "DevBrew"

    BINDINGS = [Binding("ctrl+q", "quit", "Quit")]

    def __init__(self, auth_service: AuthService | None = None) -> None:
        super().__init__()
        # Configured backend: MongoDB Atlas if a URI is set, else in-memory.
        self.auth = auth_service or AuthService(build_user_repository())
        self.menu = MenuService()
        self.cart = Cart()

    def on_mount(self) -> None:
        self.push_screen(ConsoleScreen())

    def show_menu(self) -> None:
        """Open the arrow-key menu on top of the console (Esc returns)."""
        from devbrew.ui.screens.menu import MenuScreen

        self.push_screen(MenuScreen())

    def show_cart(self) -> None:
        """Open the shopping cart on top of the current screen (Esc returns)."""
        from devbrew.ui.screens.cart import CartScreen

        self.push_screen(CartScreen())
