"""Django admin configuration for inventory reference data."""

from django.contrib import admin

from inventory.models import (
    Brand,
    Item,
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


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "category",
        "unit",
        "is_active",
        "updated_at",
    )
    list_filter = ("is_active", "category", "brand", "manufacturer")
    search_fields = ("code", "barcode", "name", "generic_name")
    readonly_fields = ("id", "created_at", "updated_at", "deleted_at")
    ordering = ("name",)


admin.site.register(
    (ItemCategory, Unit, Brand, Manufacturer, Supplier, Warehouse, Store),
    NamedReferenceAdmin,
)
