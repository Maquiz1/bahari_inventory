# bahari_inventory
# Inventory

The repository contains the `inventory` Django application, a modular starting
point for an enterprise inventory-management system.

## Layout

- `inventory/models/` — Django persistence models
- `inventory/services/` — write-side use cases and workflows
- `inventory/selectors/` — read-side queries and reporting access
- `inventory/api/` — HTTP API routing and transport concerns
- `inventory/admin/` — Django admin registrations
- `inventory/tests/` — tests grouped by application boundary
- `inventory/migrations/` — Django schema migrations

No inventory business rules or data models have been implemented yet. Add
`inventory` to `INSTALLED_APPS` in the host project's Django settings when the
application is integrated.
