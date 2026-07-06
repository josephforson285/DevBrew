"""Unit tests for the coffee menu (DVBRW-7)."""

from devbrew.services.menu_service import MenuService


def test_menu_lists_available_items():
    items = MenuService().list_items()
    assert len(items) >= 3


def test_each_item_has_required_fields():
    # Acceptance: each item displays name, price, size options, and description.
    for item in MenuService().list_items():
        assert item.name
        assert item.description
        assert item.price > 0
        assert len(item.sizes) >= 1


def test_labels_are_formatted():
    latte = next(i for i in MenuService().list_items() if i.id == "latte")
    assert latte.price_label == "$3.50"
    assert latte.sizes_label == "M / L"
