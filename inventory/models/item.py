"""Catalog item model."""

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Q
from django.db.models.functions import Lower

from .base import AuditedSoftDeleteModel
from .reference_data import Brand, ItemCategory, Manufacturer, Unit


class Item(AuditedSoftDeleteModel):
    """A catalog definition for an inventory item, excluding stock quantity."""

    code = models.CharField(max_length=100)
    barcode = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=255)
    generic_name = models.CharField(max_length=255, blank=True)
    category = models.ForeignKey(
        ItemCategory, on_delete=models.PROTECT, related_name="items"
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name="items",
        null=True,
        blank=True,
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.PROTECT,
        related_name="items",
        null=True,
        blank=True,
    )
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name="items")
    track_batch = models.BooleanField(default=False)
    track_expiry = models.BooleanField(default=False)
    track_serial = models.BooleanField(default=False)
    minimum_stock = models.DecimalField(
        max_digits=14,
        decimal_places=3,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0"))],
    )
    maximum_stock = models.DecimalField(
        max_digits=14,
        decimal_places=3,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0"))],
    )
    reorder_level = models.DecimalField(
        max_digits=14,
        decimal_places=3,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0"))],
    )
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("code"),
                condition=Q(deleted_at__isnull=True),
                name="inventory_item_active_code_uniq",
            ),
            models.UniqueConstraint(
                fields=["barcode"],
                condition=Q(deleted_at__isnull=True) & Q(barcode__isnull=False),
                name="inventory_item_active_barcode_uniq",
            ),
            models.CheckConstraint(
                check=(
                    Q(minimum_stock__isnull=True)
                    | Q(maximum_stock__isnull=True)
                    | Q(minimum_stock__lte=F("maximum_stock"))
                ),
                name="inv_item_stock_levels_ck",
            ),
            models.CheckConstraint(
                check=(
                    Q(reorder_level__isnull=True)
                    | Q(maximum_stock__isnull=True)
                    | Q(reorder_level__lte=F("maximum_stock"))
                ),
                name="inv_item_reorder_level_ck",
            ),
        ]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["is_active", "name"]),
            models.Index(fields=["deleted_at"]),
        ]

    def clean(self):
        super().clean()
        self.code = self.code.strip() if self.code is not None else self.code
        self.name = self.name.strip() if self.name is not None else self.name
        self.generic_name = self.generic_name.strip() if self.generic_name else ""
        self.barcode = self.barcode.strip() if self.barcode else None

        errors = {}
        if not self.code:
            errors["code"] = "Code cannot be blank or whitespace only."
        if not self.name:
            errors["name"] = "Name cannot be blank or whitespace only."
        if (
            self.minimum_stock is not None
            and self.maximum_stock is not None
            and self.minimum_stock > self.maximum_stock
        ):
            errors["maximum_stock"] = "Maximum stock must be at least minimum stock."
        if (
            self.reorder_level is not None
            and self.maximum_stock is not None
            and self.reorder_level > self.maximum_stock
        ):
            errors["reorder_level"] = "Reorder level cannot exceed maximum stock."
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.code} — {self.name}"
