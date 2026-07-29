# 0003. Max active runs for tasks

## Context
Two scheduled runs executed simultaneously and registered data under the same name, `tmp_df`, causing one to insert the other's data. All tasks were reported as successful.

## Decision
Set max_active_runs=1 in the DAG definition.

## Consequences
DuckDB is a single-file database and is not inherently suited for concurrent writes.

Idempotency ensures safety for re-executing the *same* run, but not for the concurrent execution of *separate* runs; isolation is a different matter.

Backfilling becomes sequential, so it takes a long time.