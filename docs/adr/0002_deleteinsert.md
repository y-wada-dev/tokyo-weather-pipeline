# 0002. Delete-insert pattern for database updates

## Context
I needed to ensure that no duplicate rows were created when re-running the process for the same date.

Using the `date` column (a string containing the time) as the condition for the `DELETE` operation failed because the comparison `'2026-07-25T00:00' = '2026-07-25'` evaluated to false, preventing the row from being deleted.

Using `LIKE` for a prefix match worked, but it was unstable because it relied on a specific date format—meaning it would break if the time format returned by the API changed.

## Decision
Add an explicit `ds` partition column, and delete rows matching the run's `ds`
before inserting the new batch.

## Consequences
An additional column is added. By incorporating the same concept as the `{ds}` in the filename into the table itself, the unit of partitioning is explicitly defined. 