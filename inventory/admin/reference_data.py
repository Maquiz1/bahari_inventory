"""Django admin configuration for inventory reference data."""

from django.contrib import admin

from inventory.models import (
    Brand,
    ItemCategory,
    Manufacturer,
    Store,
    Supplier,
    Unit,
    Warehouse,
)


class NamedReferenceAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at", "deleted_at")
    search_fields = ("name",)
    readonly_fields = ("id", "created_at", "updated_at", "deleted_at")
    ordering = ("name",)


admin.site.register(
    (ItemCategory, Unit, Brand, Manufacturer, Supplier, Warehouse, Store),
    NamedReferenceAdmin,
)
