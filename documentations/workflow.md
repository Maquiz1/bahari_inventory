# Bahari Inventory — Reference Data and Item Workflow

## Purpose

This workflow describes the reference-data lifecycle currently implemented in
the `inventory` application. It covers ItemCategory, Unit, Brand,
Manufacturer, Supplier, Warehouse, Store, and Item.

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

## Item catalog workflow

1. Create the required Item Category and Unit first. Optionally create Brand
   and Manufacturer records.
2. Go to **Inventory → Items** and select **Add Item**.
3. Enter a unique code and item name, then choose category and unit.
4. Optionally provide barcode, generic name, brand, manufacturer, description,
   tracking options, and stock-policy thresholds.
5. If a maximum stock threshold is entered, ensure it is not lower than the
   minimum stock or reorder level.
6. Save the item. The system trims the text identifiers and rejects duplicate
   active codes or barcodes.
7. Use the Item search box to find records by code, barcode, name, or generic
   name, and filters to narrow by active status or reference data.

Item records do not hold stock quantity. Quantity is introduced only by a
future stock-balance or stock-transaction workflow.

## Exception handling

| Situation | System behavior | User action |
| --- | --- | --- |
| Blank name | Rejects the record with a validation error. | Enter a meaningful name. |
| Whitespace-only name | Rejects the record with a validation error. | Enter a meaningful name. |
| Duplicate active name | Rejects the record. | Reuse the existing record or choose a distinct name. |
| Delete a record | Soft-deletes the record. | Escalate to an authorized maintainer if restoration is required. |
| Restore conflicts with an active name | Rejects restoration. | Rename or remove the conflicting active record through an approved process. |
| Duplicate Item code or barcode | Rejects the Item save while the matching record is active. | Use a unique identifier or reuse the existing Item. |
| Item maximum below minimum or reorder level | Rejects the Item save. | Correct the stock-policy thresholds. |
