CREATE OR REPLACE TABLE GOLD.WEATHER_DAILY AS
SELECT
    DATE_TRUNC('day', observation_ts)      AS day_utc,
    AVG(temp_c)                            AS avg_temp_c,
    MIN(temp_c)                            AS min_temp_c,
    MAX(temp_c)                            AS max_temp_c,
    AVG(humidity_pct)                      AS avg_humidity_pct
FROM   SILVER.WEATHER_CURRENT
GROUP  BY day_utc;
