"""Unit tests for delivery details (DVBRW-10)."""

import pytest

from devbrew.errors import ValidationError
from devbrew.models.delivery import DeliveryDetails


def test_create_valid_details():
    d = DeliveryDetails.create(
        name="Joseph", phone="0551234567", address="KG 11 Ave", instructions="Gate 2"
    )
    assert d.name == "Joseph"
    assert d.phone == "0551234567"
    assert d.address == "KG 11 Ave"
    assert d.instructions == "Gate 2"


def test_instructions_optional():
    d = DeliveryDetails.create(name="Joseph", phone="0551234567", address="KG 11 Ave")
    assert d.instructions == ""


def test_missing_name_rejected():
    with pytest.raises(ValidationError, match="Name is required"):
        DeliveryDetails.create(name="  ", phone="0551234567", address="KG 11 Ave")


def test_invalid_phone_rejected():
    with pytest.raises(ValidationError, match="valid phone"):
        DeliveryDetails.create(name="Joseph", phone="abc", address="KG 11 Ave")


def test_missing_address_rejected():
    with pytest.raises(ValidationError, match="Address is required"):
        DeliveryDetails.create(name="Joseph", phone="0551234567", address="")


def test_summary_includes_fields():
    summary = "\n".join(
        DeliveryDetails.create(
            name="Joseph", phone="0551234567", address="KG 11 Ave", instructions="Gate 2"
        ).summary_lines()
    )
    assert "Joseph" in summary
    assert "0551234567" in summary
    assert "KG 11 Ave" in summary
    assert "Gate 2" in summary
