"""Currency formatting for DevBrew (single source of truth).

Prices are held as whole Rwandan Francs (RWF) and formatted in one place so the
menu, customization, and order totals stay consistent (DVBRW-21).
"""

from __future__ import annotations

CURRENCY = "RWF"


def format_price(amount: float) -> str:
    """Format an amount in Rwandan Francs, e.g. 3000 -> 'RWF 3,000'."""
    return f"{CURRENCY} {amount:,.0f}"
