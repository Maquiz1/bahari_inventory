# Bahari Inventory — Technical Documentation

## Architecture

The repository provides a reusable Django application named `inventory`.

| Area | Location | Responsibility |
| --- | --- | --- |
| App configuration | `inventory/apps.py` | Registers the Inventory application. |
| Models | `inventory/models/` | Persistence and validation rules. |
| Admin | `inventory/admin/` | Django admin registrations. |
| Migration | `inventory/migrations/0001_reference_data.py` | Creates the initial reference-data schema. |
| Services | `inventory/services/` | Reserved for future write-side workflows. |
| Selectors | `inventory/selectors/` | Reserved for future read-side queries. |
| API | `inventory/api/` | Reserved for future HTTP endpoints. |

## Model design

`NamedReferenceModel` is an abstract base class in
`inventory/models/base.py`. Each of the seven concrete reference-data models
inherits it without adding fields. This keeps common validation, lifecycle,
and indexing rules identical across the model set.

### Persistence contract

- `id` is a generated UUID primary key.
- `name` is a 255-character field.
- `created_at` is set automatically when a row is created.
- `updated_at` is updated automatically on each save.
- `deleted_at` is null for active rows and stores the deletion time otherwise.

### Validation and constraints

`clean()` trims names and rejects blank values. `save()` calls `full_clean()`
so programmatic saves use the same validation as Django admin forms.

Each concrete table has a conditional unique constraint over `Lower(name)` for
rows whose `deleted_at` is null. Therefore `Brand.objects.create(name="Acme")`
and a second active `brand` conflict, while a new active record may reuse a
name after the old record is soft-deleted.

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

Each concrete table has indexes for `name`, `deleted_at`, and `created_at`, in
addition to the conditional active-name uniqueness index. Django generates
database-safe index names during migration creation.

## Admin

`inventory/admin/reference_data.py` registers every model with a common
`NamedReferenceAdmin`. The list screen shows the name and audit timestamps,
supports name search, orders by name, and presents UUID and audit fields as
read-only.

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
