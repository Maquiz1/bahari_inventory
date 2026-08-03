"""Reference-data models used throughout the inventory domain."""

from .base import NamedReferenceModel


class ItemCategory(NamedReferenceModel):
    """A grouping used to classify inventory items."""


class Unit(NamedReferenceModel):
    """A unit of measure used when tracking inventory quantities."""


class Brand(NamedReferenceModel):
    """A commercial brand associated with inventory items."""


class Manufacturer(NamedReferenceModel):
    """An organization that manufactures inventory items."""


class Supplier(NamedReferenceModel):
    """An organization that supplies inventory items."""


class Warehouse(NamedReferenceModel):
    """A warehouse in which inventory can be held."""


class Store(NamedReferenceModel):
    """A store from which inventory can be sold or issued."""
