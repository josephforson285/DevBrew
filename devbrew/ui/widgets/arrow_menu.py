"""Classic keyboard menu: a '>' cursor points at the selected row.

No full-row highlight bar - selection is shown the old-school terminal way,
with a '>' marker and a bold row. Navigate with up/down (or k/j), Enter selects.
"""

from __future__ import annotations

from rich.text import Text
from textual import events
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Static


class ArrowMenu(Static):
    """A vertical list of rows navigated with the arrow keys."""

    can_focus = True
    index: reactive[int] = reactive(0)

    class Selected(Message):
        """Posted when the user presses Enter on a row."""

        def __init__(self, index: int) -> None:
            self.index = index
            super().__init__()

    def __init__(self, rows: list[Text], **kwargs) -> None:
        super().__init__(**kwargs)
        self._rows = rows

    @property
    def count(self) -> int:
        return len(self._rows)

    def on_mount(self) -> None:
        self._redraw()

    def _redraw(self) -> None:
        out = Text()
        for i, row in enumerate(self._rows):
            selected = i == self.index
            out.append("> " if selected else "  ", style="bold #ff8c42" if selected else "")
            if selected:
                emphasised = row.copy()
                emphasised.stylize("bold")
                out.append_text(emphasised)
            else:
                out.append_text(row)
            if i < self.count - 1:
                out.append("\n")
        # Static measures its size from the stored renderable, so set it here.
        self.update(out)

    def watch_index(self) -> None:
        self._redraw()

    def on_key(self, event: events.Key) -> None:
        if not self._rows:
            return
        if event.key in ("up", "k"):
            event.stop()
            self.index = (self.index - 1) % self.count
        elif event.key in ("down", "j"):
            event.stop()
            self.index = (self.index + 1) % self.count
        elif event.key == "enter":
            event.stop()
            self.post_message(self.Selected(self.index))
