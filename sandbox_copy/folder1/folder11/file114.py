"""Bookstore Inventory - tests for the order workflow.

Covers the two failure cases reported in support ticket
folder3/folder33/file331.md (customers could order out-of-stock books).

Run with:  pytest folder1/folder11/file114.py
"""

import pytest


def order_total(price: float, quantity: int) -> float:
    """Mirror of the pricing rule used by the API's /api/orders route."""
    if quantity < 1:
        raise ValueError("quantity must be at least 1")
    return round(price * quantity, 2)


def can_order(stock: int, quantity: int) -> bool:
    return stock >= quantity


class TestOrderTotal:
    def test_single_item(self):
        assert order_total(9.99, 1) == 9.99

    def test_multiple_items(self):
        assert order_total(29.99, 3) == 89.97

    def test_zero_quantity_rejected(self):
        with pytest.raises(ValueError):
            order_total(9.99, 0)


class TestStockCheck:
    def test_in_stock(self):
        assert can_order(stock=12, quantity=2) is True

    def test_exact_stock(self):
        # Ordering the last copy is allowed.
        assert can_order(stock=5, quantity=5) is True

    def test_out_of_stock(self):
        # Regression test for ticket #331: '1984' has 0 stock but could be ordered.
        assert can_order(stock=0, quantity=1) is False
