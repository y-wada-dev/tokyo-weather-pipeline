SELECT 
    CAST(observed_at AS DATE) AS observed_date,
    min(temperature_c) AS min_temperature_c,
    max(temperature_c) AS max_temperature_c,
    avg(temperature_c) AS avg_temperature_c
FROM {{ ref('stg_temperature') }}
GROUP BY
    CAST(observed_at AS DATE)