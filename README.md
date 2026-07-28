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
├── dags/                  # Airflow DAG Pipeline logic (fetch, validate, transform, load)
├── data/                  # Local data (gitignored)
├── docker-compose.yaml
├── Dockerfile
├── .env.example
├── CONTRIBUTING.md
└── requirements.txt
```

## Setup

1. Clone and configure
    ```bash
    git clone https://github.com/ykwada/tokyo-weather-pipeline
    cd tokyo-weather-pipeline
    cp .env.example .env # copy `.env.example` to `.env` and edit if necessary
    ```

2. Generate a Fernet key

    ```bash
    python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
    ```

    This assumes that the `cryptography` library is installed in the Python environment on the host. The process will fail if it is missing, so please run `pip install cryptography` if necessary.
    
    Paste the output into FERNET_KEY= in the .env file.
    
3. Build and start
    
    ```bash
    docker compose build
    docker compose up -d
    ```

4. Access the UI
    Open http://localhost:8080 in your browser and log in with `airflow` / `airflow`

5. Trigger the DAG
    DAG menu → `weather_daily` → Trigger DAG

## Why retries are safe
`fetch_weather` overwrites the same `{ds}.json` file, and `load_to_db` deletes rows
for the given `ds` before inserting. Both tasks are idempotent, so re-running them
produces the same result rather than duplicating data.

This is what makes automatic retries safe here: with a plain `INSERT`, a retry after
a partial failure would duplicate rows. Idempotency is a precondition for retries,
not just a nice property.

## Development flow
Branching strategy, commit conventions, and PR flow: [CONTRIBUTING.md](./CONTRIBUTING.md)
