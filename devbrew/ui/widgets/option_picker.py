"""Keyboard option picker: up/down choose a field, left/right cycle its value.

A classic terminal settings control. Selection is shown with a '>' cursor and
'◂ value ▸' brackets - no highlight bar.
"""

from __future__ import annotations

from rich.text import Text
from textual import events
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Static


class OptionPicker(Static):
    """Rows of ``label: ◂ value ▸`` navigated with the arrow keys."""

    can_focus = True
    row: reactive[int] = reactive(0)

    class Changed(Message):
        """Posted whenever a value changes."""

    class Confirmed(Message):
        """Posted when the user presses Enter."""

    def __init__(self, options: list[tuple[str, tuple[str, ...]]], **kwargs) -> None:
        super().__init__(**kwargs)
        self._labels = [label for label, _ in options]
        self._values = [values for _, values in options]
        self._value_index = [0] * len(options)

    @property
    def choices(self) -> dict[str, str]:
        return {
            label: self._values[i][self._value_index[i]]
            for i, label in enumerate(self._labels)
        }

    def on_mount(self) -> None:
        self._redraw()

    def _redraw(self) -> None:
        out = Text()
        for i, label in enumerate(self._labels):
            selected = i == self.row
            out.append("> " if selected else "  ", style="bold #ff8c42" if selected else "")
            value = self._values[i][self._value_index[i]]
            line = Text(f"{label:<12} ◂ {value} ▸")
            if selected:
                line.stylize("bold")
            out.append_text(line)
            if i < len(self._labels) - 1:
                out.append("\n")
        self.update(out)

    def watch_row(self) -> None:
        self._redraw()

    def _cycle(self, delta: int) -> None:
        options = self._values[self.row]
        self._value_index[self.row] = (self._value_index[self.row] + delta) % len(options)
        self._redraw()
        self.post_message(self.Changed())

    def on_key(self, event: events.Key) -> None:
        if event.key in ("up", "k"):
            event.stop()
            self.row = (self.row - 1) % len(self._labels)
        elif event.key in ("down", "j"):
            event.stop()
            self.row = (self.row + 1) % len(self._labels)
        elif event.key in ("left", "h"):
            event.stop()
            self._cycle(-1)
        elif event.key in ("right", "l"):
            event.stop()
            self._cycle(1)
        elif event.key == "enter":
            event.stop()
            self.post_message(self.Confirmed())
