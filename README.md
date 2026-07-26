# Tokyo Weather Pipeline

Daily batch pipeline that fetches Tokyo weather data from the
Open-Meteo API, validates and transforms it, and loads it into
DuckDB — orchestrated with Apache Airflow.

## Architecture

fetch → validate → transform → load

- **fetch**: pulls daily weather data, stores raw JSON partitioned by date
- **validate**: schema and completeness checks; fails fast on bad data
- **transform**: flattens JSON into tabular format
- **load**: idempotent delete-insert into DuckDB

## Directory structure
```
├── dags/                  # Airflow DAG definitions
├── src/                   # Pipeline logic (fetch, validate, transform, load)
├── data/                  # Local data (gitignored)
├── docker-compose.yml
├── CONTRIBUTING.md
└── requirements.txt
```

## Development flow

Branching strategy, commit conventions, and PR flow: [CONTRIBUTING.md](./CONTRIBUTING.md)

## Why retries are safe

`fetch_weather` overwrites the same `{ds}.json` file, and `load_to_db` deletes rows
for the given `ds` before inserting. Both tasks are idempotent, so re-running them
produces the same result rather than duplicating data.

This is what makes automatic retries safe here: with a plain `INSERT`, a retry after
a partial failure would duplicate rows. Idempotency is a precondition for retries,
not just a nice property.