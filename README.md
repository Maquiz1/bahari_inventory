# Bahari Inventory

The repository contains the `inventory` Django application for catalog and
reference-data management. It currently provides the reference records and
Item catalog definition needed before inventory balances and transactions are
introduced.

## Current scope

- Reference data: ItemCategory, Unit, Brand, Manufacturer, Supplier,
  Warehouse, and Store.
- Catalog items: code, barcode, names, category, brand, manufacturer, unit,
  tracking options, stock-policy thresholds, active status, and description.
- UUID primary keys, audit fields, soft deletion, validation, indexes,
  migrations, and Django admin registration.
- Stock quantity is intentionally not part of `Item`; it belongs to a future
  stock-balance or transaction model.

## Layout

- `inventory/models/` — Django persistence models
- `inventory/services/` — write-side use cases and workflows
- `inventory/selectors/` — read-side queries and reporting access
- `inventory/api/` — HTTP API routing and transport concerns
- `inventory/admin/` — Django admin registrations
- `inventory/tests/` — tests grouped by application boundary
- `inventory/migrations/` — Django schema migrations
- `documentations/` — SRS, workflows, technical documentation, user manual,
  and UAT template

## Integration

Add `inventory` to `INSTALLED_APPS`, then apply its migrations:

```bash
python manage.py migrate inventory
```

For full implementation and acceptance guidance, see the
[documentation set](documentations/).
