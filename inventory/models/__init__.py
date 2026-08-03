"""Persistence models for the inventory domain.

Keep concrete Django models in focused modules as the domain grows, and import
their public interfaces here when Django needs to discover them.
"""

from .reference_data import (
    Brand,
    ItemCategory,
    Manufacturer,
    Store,
    Supplier,
    Unit,
    Warehouse,
)
from .item import Item

__all__ = [
    "Brand",
    "Item",
    "ItemCategory",
    "Manufacturer",
    "Store",
    "Supplier",
    "Unit",
    "Warehouse",
]
