from django.apps import AppConfig


class InventoryConfig(AppConfig):
    """Application configuration for the inventory domain."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "inventory"
    verbose_name = "Inventory Management"
