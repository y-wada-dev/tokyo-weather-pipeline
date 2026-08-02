SELECT 
    CAST(date as TIMESTAMP) AS observed_at,
    temperature AS temperature_c,
    ds,
    created_at
FROM {{ source('airflow', 'TEMPERATURE') }}