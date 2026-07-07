"""Tests for application event logging (DVBRW-18)."""

import logging

import pytest

import devbrew.logging_config as logging_config
from devbrew.errors import ValidationError
from devbrew.logging_config import get_logger, setup_logging
from devbrew.models.cart import Cart
from devbrew.models.customization import Customization, CustomizedDrink
from devbrew.models.delivery import DeliveryDetails
from devbrew.models.menu import MenuItem
from devbrew.models.user import User
from devbrew.repositories.order_repository import InMemoryOrderRepository
from devbrew.repositories.user_repository import InMemoryUserRepository
from devbrew.services.auth_service import AuthService
from devbrew.services.order_service import OrderService

LATTE = MenuItem("latte", "Latte", "Espresso + steamed milk", 3500, ("M", "L"))


def _cart() -> Cart:
    cart = Cart()
    cart.add(CustomizedDrink(LATTE, Customization("M", "Oat", "Low", False)))
    return cart


def test_logger_namespace():
    assert get_logger("auth").name == "devbrew.auth"


def test_login_and_registration_are_logged(caplog):
    caplog.set_level(logging.INFO, logger="devbrew")
    auth = AuthService(InMemoryUserRepository())

    auth.register(name="Joseph", email="j@example.com", phone="0551234567")
    auth.logout()
    auth.login("j@example.com")

    messages = [r.getMessage() for r in caplog.records]
    assert any("user registered" in m for m in messages)
    assert any("user logged in" in m for m in messages)


def test_validation_errors_are_logged(caplog):
    caplog.set_level(logging.WARNING, logger="devbrew")
    auth = AuthService(InMemoryUserRepository())

    with pytest.raises(ValidationError):
        auth.register(name="  ", email="j@example.com", phone="0551234567")

    assert any(r.levelno == logging.WARNING for r in caplog.records)


def test_order_creation_is_logged(caplog):
    caplog.set_level(logging.INFO, logger="devbrew")
    service = OrderService(InMemoryOrderRepository())
    user = User(name="Joseph", email="j@example.com", phone="0551234567")
    delivery = DeliveryDetails.create(name="Joseph", phone="0551234567", address="KG 11 Ave")

    order = service.place_order(user=user, cart=_cart(), delivery=delivery)

    assert any(f"order created: {order.id}" in r.getMessage() for r in caplog.records)


def test_order_status_change_is_logged(caplog):
    caplog.set_level(logging.INFO, logger="devbrew")
    service = OrderService(InMemoryOrderRepository())
    user = User(name="Joseph", email="j@example.com", phone="0551234567")
    delivery = DeliveryDetails.create(name="Joseph", phone="0551234567", address="KG 11 Ave")
    order = service.place_order(user=user, cart=_cart(), delivery=delivery)

    service.update_status(order, "Preparing")

    assert order.status == "Preparing"
    assert any("status changed" in r.getMessage() for r in caplog.records)


def test_setup_logging_writes_a_file(tmp_path, monkeypatch):
    monkeypatch.setattr(logging_config, "_configured", False)
    monkeypatch.setattr(logging_config, "LOG_DIR", tmp_path / "logs")

    log_file = setup_logging()
    get_logger("test").info("hello log")

    assert log_file.exists()

    # Clean up the file handler so it doesn't leak into other tests.
    logger = logging.getLogger("devbrew")
    for handler in list(logger.handlers):
        if isinstance(handler, logging.FileHandler):
            logger.removeHandler(handler)
            handler.close()
