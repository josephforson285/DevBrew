"""Classic terminal console: a '>' prompt REPL (DVBRW-6 UI / DevEx).

Auth and commands happen by typing at the prompt, like a real shell. The menu
(DVBRW-7) is a separate arrow-key screen opened with the ``menu`` command.
"""

from __future__ import annotations

from collections.abc import Callable

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Footer, Header, Input, Label, RichLog, Static

from devbrew.errors import DevBrewError
from devbrew.ui.logo import DEVBREW_ASCII

WELCOME = "coffee-4-devs  ·  type 'help' to begin."
HELP = "commands:  help  ·  register  ·  login <email>  ·  menu  ·  cart  ·  clear  ·  quit"


class ConsoleScreen(Screen):
    """A scrolling console with a single input prompt."""

    BINDINGS = [("ctrl+q", "app.quit", "Quit")]

    def __init__(self) -> None:
        super().__init__()
        # Guided input state (for multi-field register / login).
        self._pending: list[tuple[str, str]] = []
        self._collected: dict[str, str] = {}
        self._on_complete: Callable[[dict[str, str]], None] | None = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(id="console"):
            yield Static(DEVBREW_ASCII.strip("\n"), id="logo")
            yield RichLog(id="output", markup=True, wrap=True)
            with Horizontal(id="prompt-row"):
                yield Label("> ", id="prompt-sym")
                yield Input(id="prompt-input")
        yield Footer()

    def on_mount(self) -> None:
        self._print(WELCOME)
        self.query_one("#prompt-input", Input).focus()

    # --- output helpers ---------------------------------------------------

    def _print(self, text: str) -> None:
        self.query_one("#output", RichLog).write(text)

    def _set_prompt(self, symbol: str) -> None:
        self.query_one("#prompt-sym", Label).update(symbol)

    # --- input handling ---------------------------------------------------

    def on_input_submitted(self, event: Input.Submitted) -> None:
        value = event.value.strip()
        self.query_one("#prompt-input", Input).value = ""

        if self._pending:
            self._handle_collection(value)
            return

        if not value:
            return
        self._print(f"[dim]>[/] {value}")
        self._dispatch(value)

    # --- guided multi-field collection ------------------------------------

    def _begin_collection(
        self,
        fields: list[tuple[str, str]],
        on_complete: Callable[[dict[str, str]], None],
    ) -> None:
        self._collected = {}
        self._pending = list(fields)
        self._on_complete = on_complete
        field, label = self._pending[0]
        self._set_prompt(f"{label} > ")

    def _handle_collection(self, value: str) -> None:
        field, label = self._pending.pop(0)
        self._collected[field] = value
        self._print(f"[dim]{label} >[/] {value}")

        if self._pending:
            next_label = self._pending[0][1]
            self._set_prompt(f"{next_label} > ")
            return

        self._set_prompt("> ")
        complete, self._on_complete = self._on_complete, None
        if complete is not None:
            complete(self._collected)

    # --- command dispatch -------------------------------------------------

    def _dispatch(self, line: str) -> None:
        parts = line.split()
        command, args = parts[0].lower(), parts[1:]

        if command == "help":
            self._print(HELP)
        elif command == "clear":
            self.query_one("#output", RichLog).clear()
        elif command in ("quit", "exit"):
            self.app.exit()
        elif command == "login":
            if args:
                self._do_login(args[0])
            else:
                self._begin_collection([("email", "email")], lambda d: self._do_login(d["email"]))
        elif command == "register":
            self._begin_collection(
                [("name", "name"), ("email", "email"), ("phone", "phone")],
                self._do_register,
            )
        elif command == "menu":
            if self.app.auth.is_authenticated:
                self.app.show_menu()
            else:
                self._print("[yellow]log in first:  login <email>[/]")
        elif command == "cart":
            if self.app.auth.is_authenticated:
                self.app.show_cart()
            else:
                self._print("[yellow]log in first:  login <email>[/]")
        else:
            self._print(f"[red]unknown command:[/] {command}   (try 'help')")

    def _do_login(self, email: str) -> None:
        try:
            user = self.app.auth.login(email)
        except DevBrewError as error:
            self._print(f"[red]✗[/] {error}")
            return
        self._print(f"[green]✓[/] signed in as {user.name}")
        self.app.show_menu()

    def _do_register(self, data: dict[str, str]) -> None:
        try:
            user = self.app.auth.register(
                name=data["name"], email=data["email"], phone=data["phone"]
            )
        except DevBrewError as error:
            self._print(f"[red]✗[/] {error}")
            return
        self._print(f"[green]✓[/] registered & signed in as {user.name}")
        self.app.show_menu()
