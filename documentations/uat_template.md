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

Use each applicable record type: Item category, Unit, Brand, Manufacturer,
Supplier, Warehouse, and Store.

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
