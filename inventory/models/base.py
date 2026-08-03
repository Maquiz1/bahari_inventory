"""Shared persistence primitives for inventory reference data."""

from __future__ import annotations

import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    """A queryset whose delete operation marks records as deleted."""

    def delete(self):
        return super().update(deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()


class ActiveManager(models.Manager.from_queryset(SoftDeleteQuerySet)):
    """Returns only records that have not been soft deleted."""

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class NamedReferenceModel(models.Model):
    """Base for named reference records with audit and soft-delete support."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = ActiveManager()
    all_objects = models.Manager.from_queryset(SoftDeleteQuerySet)()

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                condition=Q(deleted_at__isnull=True),
                name="%(app_label)s_%(class)s_active_name_uniq",
            ),
        ]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["deleted_at"]),
            models.Index(fields=["created_at"]),
        ]

    def clean(self):
        super().clean()
        if self.name is not None:
            self.name = self.name.strip()
        if not self.name:
            raise ValidationError({"name": "Name cannot be blank or whitespace only."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at", "updated_at"])

    def hard_delete(self, using=None, keep_parents=False):
        return super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        self.deleted_at = None
        self.save(update_fields=["deleted_at", "updated_at"])

    def __str__(self):
        return self.name
