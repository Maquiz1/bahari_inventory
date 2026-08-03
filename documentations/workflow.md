# Bahari Inventory — Reference Data Workflow

## Purpose

This workflow describes the reference-data lifecycle currently implemented in
the `inventory` application. It applies equally to ItemCategory, Unit, Brand,
Manufacturer, Supplier, Warehouse, and Store.

## Lifecycle

```text
Administrator creates record
          |
          v
Name is trimmed and validated
          |
          +-- invalid / duplicate active name --> show validation error
          |
          v
Active record saved (created_at and updated_at set)
          |
          +-- edit --> validate and update updated_at --> active record
          |
          +-- remove --> set deleted_at --> soft-deleted record
                                                   |
                                                   +-- future maintenance workflow --> restore --> active record
```

## Detailed steps

1. An authorized administrator opens the relevant model in Django admin.
2. The administrator enters a name and saves the form.
3. The system trims surrounding whitespace and rejects a blank name.
4. The system rejects the save if another active record of that same type has
   the same name, ignoring letter case.
5. On success, the system creates a UUID and records `created_at` and
   `updated_at`.
6. Normal application queries use `objects`, which returns only active
   records.
7. A delete action calls the model's soft-delete behavior, setting
   `deleted_at`; normal queries no longer return the record.
8. Audit or maintenance code can use `all_objects` to find all records. A
   future authorized maintenance workflow may call `restore()`; restoration is
   subject to the same active-name uniqueness rule.

## Example: adding a unit

1. Go to **Inventory → Units** in Django admin.
2. Select **Add Unit**.
3. Enter `Box` as the name and save.
4. The new unit is available through `Unit.objects` to future inventory
   features.
5. Attempting to add ` box ` while `Box` remains active is rejected.

## Exception handling

| Situation | System behavior | User action |
| --- | --- | --- |
| Blank name | Rejects the record with a validation error. | Enter a meaningful name. |
| Whitespace-only name | Rejects the record with a validation error. | Enter a meaningful name. |
| Duplicate active name | Rejects the record. | Reuse the existing record or choose a distinct name. |
| Delete a record | Soft-deletes the record. | Escalate to an authorized maintainer if restoration is required. |
| Restore conflicts with an active name | Rejects restoration. | Rename or remove the conflicting active record through an approved process. |
