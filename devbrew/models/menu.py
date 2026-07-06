"""Coffee menu domain model (DVBRW-7)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MenuItem:
    """A single coffee on the menu."""

    id: str
    name: str
    description: str
    price: float
    sizes: tuple[str, ...]

    @property
    def price_label(self) -> str:
        return f"${self.price:.2f}"

    @property
    def sizes_label(self) -> str:
        return " / ".join(self.sizes)
