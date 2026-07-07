"""Order model (DVBRW-11)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4

from devbrew.models.delivery import DeliveryDetails


def _new_order_id() -> str:
    return "DVB-" + uuid4().hex[:8].upper()


@dataclass
class Order:
    """A placed order: a snapshot of the cart plus delivery details."""

    user_email: str
    items: list[dict]
    delivery: DeliveryDetails
    total: float
    id: str = field(default_factory=_new_order_id)
    status: str = "Received"
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_document(self) -> dict:
        """Serialise to a plain dict for storage (e.g. MongoDB)."""
        return {
            "id": self.id,
            "user_email": self.user_email,
            "items": self.items,
            "delivery": {
                "name": self.delivery.name,
                "phone": self.delivery.phone,
                "address": self.delivery.address,
                "instructions": self.delivery.instructions,
            },
            "total": self.total,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }
