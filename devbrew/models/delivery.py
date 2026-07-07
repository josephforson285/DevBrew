"""Delivery details model (DVBRW-10)."""

from __future__ import annotations

from dataclasses import dataclass

from devbrew.errors import ValidationError
from devbrew.models.user import is_valid_phone


@dataclass(frozen=True)
class DeliveryDetails:
    """Where an order should be delivered."""

    name: str
    phone: str
    address: str
    instructions: str = ""

    @classmethod
    def create(
        cls, name: str, phone: str, address: str, instructions: str = ""
    ) -> DeliveryDetails:
        """Validate delivery input. Name, phone, and address are required.

        Raises:
            ValidationError: if a required field is missing or the phone is invalid.
        """
        name = name.strip()
        phone = phone.strip()
        address = address.strip()
        instructions = instructions.strip()

        if not name:
            raise ValidationError("Name is required.")
        if not is_valid_phone(phone):
            raise ValidationError("Please enter a valid phone number.")
        if not address:
            raise ValidationError("Address is required.")

        return cls(name=name, phone=phone, address=address, instructions=instructions)

    def summary_lines(self) -> list[str]:
        lines = [
            f"Name         {self.name}",
            f"Phone        {self.phone}",
            f"Address      {self.address}",
        ]
        if self.instructions:
            lines.append(f"Instructions {self.instructions}")
        return lines
