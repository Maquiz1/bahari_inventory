# Bahari Inventory — Technical Documentation

## Architecture

The repository provides a reusable Django application named `inventory`.

| Area | Location | Responsibility |
| --- | --- | --- |
| App configuration | `inventory/apps.py` | Registers the Inventory application. |
| Models | `inventory/models/` | Persistence and validation rules. |
| Admin | `inventory/admin/` | Django admin registrations. |
| Migrations | `inventory/migrations/` | Creates reference-data and Item catalog schema. |
| Services | `inventory/services/` | Reserved for future write-side workflows. |
| Selectors | `inventory/selectors/` | Reserved for future read-side queries. |
| API | `inventory/api/` | Reserved for future HTTP endpoints. |

## Model design

`AuditedSoftDeleteModel` is an abstract base class in
`inventory/models/base.py`. It provides UUID identifiers, audit fields,
soft-delete behavior, and active/all-record managers. `NamedReferenceModel`
extends it for the seven named reference-data models. `Item` inherits the
general base and defines catalog-specific fields and rules.

### Persistence contract

- `id` is a generated UUID primary key.
- `name` is a 255-character field.
- `created_at` is set automatically when a row is created.
- `updated_at` is updated automatically on each save.
- `deleted_at` is null for active rows and stores the deletion time otherwise.

### Validation and constraints

Reference-data `clean()` trims names and rejects blank values. Item validation
trims its code, barcode, name, and generic name; rejects blank code or name;
and checks stock-policy threshold ordering. `save()` calls `full_clean()` so
programmatic saves use the same validation as Django admin forms.

Each concrete table has a conditional unique constraint over `Lower(name)` for
rows whose `deleted_at` is null. Therefore `Brand.objects.create(name="Acme")`
and a second active `brand` conflict, while a new active record may reuse a
name after the old record is soft-deleted.

Item adds conditional active uniqueness for a case-insensitive `code` and a
non-empty `barcode`. It has required `category` and `unit` foreign keys and
optional `brand` and `manufacturer` foreign keys, all protected against
deletion while referenced. Its stock fields are optional policy thresholds;
there is deliberately no quantity field on the model.

### Managers and deletion

| Interface | Behavior |
| --- | --- |
| `objects` | Returns active rows only. |
| `all_objects` | Returns active and soft-deleted rows. |
| `instance.delete()` | Sets `deleted_at`; does not physically remove the row. |
| `QuerySet.delete()` | Soft-deletes every selected row. |
| `hard_delete()` | Physically deletes a row or queryset; use only under an explicit retention policy. |
| `restore()` | Clears `deleted_at`; validation still applies. |

### Indexes

Reference-data tables have indexes for `name`, `deleted_at`, and `created_at`,
in addition to their conditional active-name uniqueness index. Item has indexes
for `name`, `is_active` plus `name`, and `deleted_at`, in addition to its code
and barcode uniqueness indexes. Django generates database-safe index names
during migration creation.

## Admin

`inventory/admin/reference_data.py` registers reference data with a common
`NamedReferenceAdmin`. `ItemAdmin` shows code, name, category, unit, active
status, and last update; it supports code, barcode, name, and generic-name
search plus category, brand, manufacturer, and active-status filters.

## Host-project integration

1. Add `inventory` to `INSTALLED_APPS`.
2. Ensure the host project has the normal Django admin dependencies configured
   if the admin UI is used.
3. Apply migrations:

   ```bash
   python manage.py migrate inventory
   ```

4. Create an authorized Django admin user in the host project and grant the
   appropriate model permissions.

## Verification commands

Run these in the host Django project after integration:

```bash
python manage.py check
python manage.py makemigrations inventory --check --dry-run
python manage.py migrate inventory
```

## Extension guidance

Keep business workflows in `services`, read-oriented queries in `selectors`,
and HTTP transport logic in `api`. Do not bypass model validation with bulk
operations when name validation or audit behavior is required. New reference
data types should inherit `NamedReferenceModel` and receive a migration and
admin registration.
