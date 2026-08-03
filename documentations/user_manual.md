# Bahari Inventory — User Manual

## Who this is for

This guide is for administrators who maintain the reference lists used by
Bahari Inventory. You need a Django admin account with permission to view and
change the relevant Inventory records.

## Available reference lists

Under **Inventory** in Django admin, you can manage:

- Item categories
- Units
- Brands
- Manufacturers
- Suppliers
- Warehouses
- Stores

Each list works in the same way.

## Add a record

1. Sign in to the Django admin site.
2. Open **Inventory**, then select the list you want to update.
3. Choose **Add**.
4. Enter a name.
5. Select **Save**.

The system removes spaces at the beginning and end of the name. Names cannot
be empty, and you cannot create two active records with the same name even if
the capitalization differs.

## Edit a record

1. Open the appropriate Inventory list.
2. Select the record name.
3. Change the name and select **Save**.

The Created, Updated, Deleted, and ID fields are maintained by the system and
cannot be edited.

## Find a record

Use the search box at the top of the list to search by name. Lists are ordered
alphabetically by name.

## Remove a record

1. Select the record in the list.
2. Select **Delete** and confirm.

The system soft-deletes the record: it is hidden from normal inventory queries
but retained for audit purposes. Contact a system maintainer if a deleted
record must be restored; restoration is not exposed as a standard admin action
in this release.

## Common messages

| Message or result | What to do |
| --- | --- |
| Name cannot be blank | Enter a non-empty name. |
| A duplicate-name validation error | Use the existing active record or use a unique name. |
| Record no longer appears after deletion | This is expected soft-delete behavior. Contact a maintainer if restoration is needed. |
| You cannot see an Inventory list | Ask an administrator to grant you the appropriate Django permission. |
