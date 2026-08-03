# Bahari Inventory — User Acceptance Testing Template

## Test run information

| Field | Value |
| --- | --- |
| UAT cycle / release | |
| Test environment | |
| Test date | |
| Tester name and role | |
| Build / commit | |
| Product owner | |
| Overall result | Pass / Fail / Pass with observations |

## Preconditions

- The host Django project has `inventory` installed and migrations applied.
- The tester has a Django admin account with the required Inventory model
  permissions.
- The test environment contains no active duplicate test records, or the
  tester has selected unique names for this run.

## Test cases

Use each applicable reference-data record type: Item category, Unit, Brand,
Manufacturer, Supplier, Warehouse, and Store. Run the Item cases after
creating an Item Category and Unit.

| ID | Scenario | Steps | Expected result | Actual result | Status | Evidence / notes |
| --- | --- | --- | --- | --- | --- | --- |
| UAT-01 | Open reference list | Sign in; open Inventory; select a record type. | The list is visible to an authorized user. | | | |
| UAT-02 | Create record | Add a record with a unique valid name. | Record saves and appears in the alphabetical list. | | | |
| UAT-03 | Trim name | Add a record with spaces around a unique name. | Record saves with surrounding spaces removed. | | | |
| UAT-04 | Reject blank name | Add a record with no name. | Save is rejected with a name validation error. | | | |
| UAT-05 | Reject whitespace-only name | Add a record with only spaces. | Save is rejected with a name validation error. | | | |
| UAT-06 | Reject case-insensitive duplicate | Create `Sample`; try to create `sample` in the same list. | Second save is rejected while `Sample` is active. | | | |
| UAT-07 | Edit record | Open a created record; change its name; save. | New name is displayed and the record remains active. | | | |
| UAT-08 | Search | Search for a known active name. | Matching record is returned. | | | |
| UAT-09 | Verify audit fields | Open a saved record. | UUID, created timestamp, and updated timestamp are visible and read-only. | | | |
| UAT-10 | Soft delete | Delete a test record and return to the list. | Record no longer appears in the normal list. | | | |
| UAT-11 | Reuse deleted name | Create a new record using the deleted record's name. | New active record saves successfully. | | | |
| UAT-12 | Create Item | Add an Item with code, name, category, and unit. | Item saves and appears in the Item list. | | | |
| UAT-13 | Item identifiers | Add surrounding spaces to a unique Item code and barcode. | Identifiers are trimmed; duplicate active code or barcode is rejected. | | | |
| UAT-14 | Item tracking | Enable batch, expiry, and serial tracking on an Item. | Selected tracking settings save and display correctly. | | | |
| UAT-15 | Stock-policy validation | Enter a maximum stock lower than minimum stock or reorder level. | Item save is rejected with a validation error. | | | |
| UAT-16 | No Item quantity | Open the Item add and edit screens. | No stock quantity field is displayed. | | | |
| UAT-17 | Item search and filters | Search by Item code, barcode, name, and generic name; use filters. | Matching Items and expected filtered results are displayed. | | | |

## Defects and observations

| ID | Test case | Severity | Description | Owner | Resolution / retest result |
| --- | --- | --- | --- | --- | --- |
| | | Critical / High / Medium / Low | | | |

## Sign-off

| Role | Name | Decision | Date | Signature / approval reference |
| --- | --- | --- | --- | --- |
| Business tester | | Approve / reject | | |
| Product owner | | Approve / reject | | |
| Technical representative | | Approve / reject | | |
