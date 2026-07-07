"""Coffee menu domain model (DVBRW-7)."""

from __future__ import annotations

from dataclasses import dataclass

from devbrew.money import format_price


@dataclass(frozen=True)
class MenuItem:
    """A single coffee on the menu. Price is in Rwandan Francs (RWF)."""

    id: str
    name: str
    description: str
    price: float
    sizes: tuple[str, ...]

    @property
    def price_label(self) -> str:
        return format_price(self.price)

    @property
    def sizes_label(self) -> str:
        return " / ".join(self.sizes)
