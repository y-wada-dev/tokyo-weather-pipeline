# 0001. Pass file paths through XCom, not data payloads

## Context
It was necessary to pass data between tasks. XCom operates by storing data in a metadata database (PostgreSQL).

## Decision
Pass the file path instead of the actual data.

## Consequences
Passing only the path implies that the tasks must share access to the same storage. While this currently works with local mounts, migrating to a configuration where tasks run on separate machines (such as with KubernetesExecutor) would make shared storage (like S3) essential.    