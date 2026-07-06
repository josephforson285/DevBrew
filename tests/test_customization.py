"""Unit tests for coffee customization (DVBRW-8)."""

from devbrew.models.customization import (
    EXTRA_SHOT_PRICE,
    MILK_OPTIONS,
    SUGAR_LEVELS,
    Customization,
    CustomizedDrink,
)
from devbrew.models.menu import MenuItem

LATTE = MenuItem("latte", "Latte", "Espresso + steamed milk", 3.50, ("M", "L"))


def _drink(extra_shot: bool = False) -> CustomizedDrink:
    return CustomizedDrink(
        LATTE, Customization(size="M", milk="Oat", sugar="Low", extra_shot=extra_shot)
    )


def test_options_available():
    assert "Oat" in MILK_OPTIONS
    assert "None" in SUGAR_LEVELS


def test_extra_shot_adds_to_price():
    assert _drink(extra_shot=False).total_price == 3.50
    assert _drink(extra_shot=True).total_price == 3.50 + EXTRA_SHOT_PRICE


def test_price_label_formatting():
    assert _drink(extra_shot=True).price_label == "$4.00"


def test_summary_includes_every_choice():
    summary = "\n".join(_drink(extra_shot=True).summary_lines())
    assert "Latte" in summary
    assert "M" in summary
    assert "Oat" in summary
    assert "Low" in summary
    assert "Yes" in summary          # extra shot
    assert "$4.00" in summary
