"""Delivery details screen: guided '>' prompt entry (DVBRW-10)."""

from __future__ import annotations

from collections.abc import Callable

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Footer, Header, Input, Label, RichLog, Static

from devbrew.models.delivery import DeliveryDetails
from devbrew.models.user import is_valid_phone


def _required(label: str) -> Callable[[str], str | None]:
    def validate(value: str) -> str | None:
        return None if value.strip() else f"{label} is required."

    return validate


def _phone(value: str) -> str | None:
    return None if is_valid_phone(value) else "Please enter a valid phone number."


def _optional(value: str) -> str | None:
    return None


class DeliveryScreen(Screen):
    """Collect name, phone, address, and optional instructions, one field at a time."""

    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def __init__(self) -> None:
        super().__init__()
        self._fields: list[tuple[str, str, Callable[[str], str | None]]] = [
            ("name", "Name", _required("Name")),
            ("phone", "Phone", _phone),
            ("address", "Address", _required("Address")),
            ("instructions", "Instructions (optional)", _optional),
        ]
        self._index = 0
        self._collected: dict[str, str] = {}

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(id="delivery-frame"):
            yield Static("DELIVERY DETAILS", id="menu-title")
            yield RichLog(id="delivery-log", markup=True, wrap=True)
            with Horizontal(id="delivery-row"):
                yield Label("> ", id="delivery-sym")
                yield Input(id="delivery-input")
            yield Static(id="delivery-summary")
        yield Static("type each field   Enter to submit   Esc back", id="menu-hint")
        yield Footer()

    def on_mount(self) -> None:
        self._print("Enter your delivery details.")
        self._set_prompt()
        self.query_one("#delivery-input", Input).focus()

    def _print(self, text: str) -> None:
        self.query_one("#delivery-log", RichLog).write(text)

    def _set_prompt(self) -> None:
        _, label, _ = self._fields[self._index]
        self.query_one("#delivery-sym", Label).update(f"{label} > ")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        value = event.value
        self.query_one("#delivery-input", Input).value = ""

        key, label, validate = self._fields[self._index]
        error = validate(value)
        if error:
            self._print(f"[red]✗[/] {error}")
            return

        self._collected[key] = value.strip()
        self._print(f"[dim]{label} >[/] {value.strip() or '—'}")
        self._index += 1
        if self._index < len(self._fields):
            self._set_prompt()
        else:
            self._finish()

    def _finish(self) -> None:
        details = DeliveryDetails.create(**self._collected)
        self.app.delivery = details
        self.query_one("#delivery-summary", Static).update("\n".join(details.summary_lines()))
        self.query_one("#delivery-sym", Label).update("✓ ")
        self.query_one("#delivery-input", Input).disabled = True
        self._print("[green]✓[/] Delivery details saved.")
