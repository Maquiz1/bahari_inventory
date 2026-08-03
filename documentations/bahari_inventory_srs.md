# Bahari Inventory — Software Requirements Specification

## 1. Purpose

Bahari Inventory is a Django inventory-management application. This release
establishes reference data and the Item catalog that future stock, purchasing,
and sales features will use. It deliberately does not introduce stock
quantity, transactions, APIs, or reporting functionality.

## 2. Scope

The system shall manage the following reference-data records and catalog item:

| Record | Business purpose |
| --- | --- |
| Item category | Classifies inventory items. |
| Unit | Identifies a unit of measure for quantities. |
| Brand | Identifies an item's commercial brand. |
| Manufacturer | Identifies the organization that makes an item. |
| Supplier | Identifies the organization that supplies an item. |
| Warehouse | Identifies a location where inventory is held. |
| Store | Identifies a location from which inventory is sold or issued. |
| Item | Defines a catalog product without recording stock quantity. |

## 3. Functional requirements

### 3.1 Reference-data management

- **FR-01:** An authorized administrator shall be able to create, view, edit,
  and remove each reference-data record through Django admin.
- **FR-02:** Every record shall have a required `name` of at most 255
  characters.
- **FR-03:** Leading and trailing whitespace in a name shall be removed before
  saving; an empty or whitespace-only name shall be rejected.
- **FR-04:** Active records of the same type shall have case-insensitively
  unique names.
- **FR-05:** Removing a record shall soft-delete it. It must no longer appear
  in normal application queries, while remaining in the database for audit
  purposes.

### 3.2 Auditability and data integrity

- **FR-06:** Each record shall have a UUID primary key.
- **FR-07:** Each record shall record when it was created, last updated, and
  soft-deleted (`created_at`, `updated_at`, and `deleted_at`).
- **FR-08:** The data layer shall support restoring a soft-deleted record when
  a future authorized workflow requires it.

### 3.3 Item catalog management

- **FR-09:** An authorized administrator shall be able to create, view, edit,
  search, and soft-delete Items through Django admin.
- **FR-10:** An Item shall have a required `code`, `name`, `category`, and
  `unit`; `barcode`, `generic_name`, `brand`, `manufacturer`, and
  `description` are optional.
- **FR-11:** An Item shall provide `track_batch`, `track_expiry`, and
  `track_serial` options, all disabled by default.
- **FR-12:** An Item shall provide optional non-negative `minimum_stock`,
  `maximum_stock`, and `reorder_level` policy thresholds. Where maximum stock
  is supplied, it cannot be below minimum stock or the reorder level.
- **FR-13:** Active Item codes shall be unique without regard to letter case.
  Non-empty active barcodes shall also be unique.
- **FR-14:** An Item shall provide an `is_active` status and must not contain a
  stock quantity field. Quantity is owned by a future stock-balance or
  transaction capability.

## 4. Non-functional requirements

- **NFR-01:** Normal model queries must return active records only.
- **NFR-02:** A full-access manager must be available for audit, maintenance,
  and restore workflows.
- **NFR-03:** Database indexes must support common name lookup, active/deleted
  filtering, and created-date lookup.
- **NFR-04:** Schema changes must be supplied as Django migrations.
- **NFR-05:** The application must pass Django system checks when integrated
  into a correctly configured Django project.

## 5. Data requirements

The seven reference-data record types share the following fields:

| Field | Type | Rules |
| --- | --- | --- |
| `id` | UUID | Primary key; generated automatically. |
| `name` | text, 255 characters | Required; trimmed; case-insensitively unique among active records of the same type. |
| `created_at` | timestamp | Set at creation. |
| `updated_at` | timestamp | Updated on every save. |
| `deleted_at` | nullable timestamp | Set by soft delete; null for an active record. |

An Item has the same `id`, audit, and soft-delete fields plus the following
catalog fields:

| Field | Rules |
| --- | --- |
| `code`, `name` | Required; trimmed; active codes are case-insensitively unique. |
| `barcode`, `generic_name`, `description` | Optional descriptive fields. |
| `category`, `unit` | Required links to reference data. |
| `brand`, `manufacturer` | Optional links to reference data. |
| `track_batch`, `track_expiry`, `track_serial`, `is_active` | Boolean controls. |
| `minimum_stock`, `maximum_stock`, `reorder_level` | Optional non-negative policy thresholds; not inventory quantity. |

## 6. Assumptions and exclusions

- Django authentication and authorization are supplied by the host project.
- The host project adds `inventory` to `INSTALLED_APPS` and applies its
  migrations.
- Stock balances, stock movements, addresses, contacts, procurement, and sales
  are outside this release. In particular, Item does not store quantity.
- No API endpoints or custom user interface are included in this release.

## 7. Acceptance criteria

The release is accepted when all seven reference-data records and Item are
migrated and registered in Django admin; validation, audit timestamps, UUID
primary keys, soft deletion, indexes, and the defined uniqueness constraints
work; and Item contains no stock quantity field.
