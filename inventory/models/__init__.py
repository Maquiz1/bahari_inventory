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

__all__ = [
    "Brand",
    "ItemCategory",
    "Manufacturer",
    "Store",
    "Supplier",
    "Unit",
    "Warehouse",
]
