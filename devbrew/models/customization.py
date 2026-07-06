"""Coffee customization model (DVBRW-8)."""

from __future__ import annotations

from dataclasses import dataclass

from devbrew.models.menu import MenuItem

MILK_OPTIONS: tuple[str, ...] = ("Whole", "Skim", "Oat", "Almond", "None")
SUGAR_LEVELS: tuple[str, ...] = ("None", "Low", "Medium", "High")
EXTRA_SHOT_PRICE = 0.50


@dataclass(frozen=True)
class Customization:
    """The choices a user makes for a drink."""

    size: str
    milk: str
    sugar: str
    extra_shot: bool


@dataclass(frozen=True)
class CustomizedDrink:
    """A menu item plus the customization applied to it."""

    item: MenuItem
    customization: Customization

    @property
    def total_price(self) -> float:
        price = self.item.price
        if self.customization.extra_shot:
            price += EXTRA_SHOT_PRICE
        return price

    @property
    def price_label(self) -> str:
        return f"${self.total_price:.2f}"

    def summary_lines(self) -> list[str]:
        """Human-readable order summary lines."""
        c = self.customization
        return [
            f"Drink       {self.item.name}",
            f"Size        {c.size}",
            f"Milk        {c.milk}",
            f"Sugar       {c.sugar}",
            f"Extra shot  {'Yes' if c.extra_shot else 'No'}",
            f"Total       {self.price_label}",
        ]
