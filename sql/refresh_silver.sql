MERGE INTO SILVER.WEATHER_CURRENT tgt
USING (
    SELECT
        TO_TIMESTAMP_LTZ("_airbyte_data":current.dt)       AS observation_ts,
        "_airbyte_data":lat::FLOAT                         AS lat,
        "_airbyte_data":lon::FLOAT                         AS lon,
        "_airbyte_data":timezone::STRING                   AS timezone,
        "_airbyte_data":current.temp::FLOAT                AS temp_c,
        "_airbyte_data":current.humidity::INT              AS humidity_pct,
        "_airbyte_data":current.wind_speed::FLOAT          AS wind_speed_ms,
        "_airbyte_data":current.weather[0].main::STRING    AS conditions,
        "_airbyte_extracted_at"                             AS extracted_at
    FROM AIRBYTE_INTERNAL."PUBLIC_raw__stream_onecall"
) src
ON  tgt.observation_ts = src.observation_ts
WHEN NOT MATCHED THEN
INSERT (
  observation_ts, lat, lon, timezone,
  temp_c, humidity_pct, wind_speed_ms, conditions, extracted_at
)
VALUES (
  src.observation_ts, src.lat, src.lon, src.timezone,
  src.temp_c, src.humidity_pct, src.wind_speed_ms, src.conditions, src.extracted_at
);
