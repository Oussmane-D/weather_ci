# dags/weather_pipeline.py
from datetime import datetime
from airflow import DAG
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

DEFAULT_ARGS = {
    "owner": "ouss",
    "retries": 1,
}

with DAG(
    dag_id="weather_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="0 * * * *",
    catchup=False,
    template_searchpath="/opt/airflow/sql",
    default_args=DEFAULT_ARGS,
    tags=["portfolio", "weather"],
) as dag:

    airbyte_sync = AirbyteTriggerSyncOperator(
        task_id="airbyte_sync",
        airbyte_conn_id="airbyte_cloud",
        connection_id="4443efaa-f1b0-4ae6-99d8-965471e0cdba",
        asynchronous=False,
        timeout=3600,
    )

    refresh_silver = SQLExecuteQueryOperator(
        task_id="refresh_silver",
        conn_id="snowflake_conn",
        sql="refresh_silver.sql",
    )

    refresh_gold = SQLExecuteQueryOperator(
        task_id="refresh_gold",
        conn_id="snowflake_conn",
        sql="refresh_gold.sql",
    )

    airbyte_sync >> refresh_silver >> refresh_gold
