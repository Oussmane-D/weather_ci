# dags/weather_pipeline.py
from datetime import datetime
from airflow import DAG
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

# ──────────────────────────────────────────────────────────────
# 1. Paramètres généraux
# ──────────────────────────────────────────────────────────────
DEFAULT_ARGS = {
    "owner": "ouss",
    "retries": 1,
}

with DAG(
    dag_id="weather_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule_interval="0 * * * *",     # ⇒ toutes les heures pile
    catchup=False,
    template_searchpath="/opt/airflow/sql",
    default_args=DEFAULT_ARGS,
    tags=["portfolio", "weather"],
) as dag:
    # ──────────────────────────────────────────────────────────
    # 2. Tâche : déclenchement Airbyte Cloud
    # ──────────────────────────────────────────────────────────
    airbyte_sync = AirbyteTriggerSyncOperator(
        task_id="airbyte_sync",
        airbyte_conn_id="airbyte_cloud",              # ← Connexion définie dans Airflow
        connection_id="4443efaa-f1b0-4ae6-99d8-965471e0cdba",
        asynchronous=False,                           # on attend la fin de la sync
        timeout=3600,
    )

    # ──────────────────────────────────────────────────────────
    # 3. Tâche : rafraîchissement SILVER
    # ──────────────────────────────────────────────────────────
    refresh_silver = SnowflakeOperator(
        task_id="refresh_silver",
        snowflake_conn_id="snowflake_conn",           # ← Connexion Snowflake
        sql="refresh_silver.sql",                 # chemin relatif dans le conteneur
    )

    # ──────────────────────────────────────────────────────────
    # 4. Tâche : reconstruction GOLD
    # ──────────────────────────────────────────────────────────
    refresh_gold = SnowflakeOperator(
        task_id="refresh_gold",
        snowflake_conn_id="snowflake_conn",
        sql="refresh_gold.sql",
    )

    # ──────────────────────────────────────────────────────────
    # 5. Dépendances
    # ──────────────────────────────────────────────────────────
    airbyte_sync >> refresh_silver >> refresh_gold
