FROM apache/airflow:2.9.1-python3.10

USER root
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# ajoute tes DAGs dans l’image (facultatif ; sinon volume mount)
COPY dags/ /opt/airflow/dags
COPY sql/  /opt/airflow/sql

USER airflow
