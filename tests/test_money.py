"""Tests for currency formatting (DVBRW-21)."""

from devbrew.money import format_price


def test_formats_in_rwandan_francs():
    assert format_price(3000) == "RWF 3,000"


def test_thousands_separator_and_no_decimals():
    assert format_price(3750) == "RWF 3,750"
    assert format_price(500) == "RWF 500"


def test_no_dollar_sign():
    assert "$" not in format_price(2500)
