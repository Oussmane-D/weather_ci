# tests/test_dags.py
import pytest
from airflow.models import DagBag

def test_no_import_errors():
    dag_bag = DagBag(dag_folder="dags/", include_examples=False)
    assert not dag_bag.import_errors, f"Import errors: {dag_bag.import_errors}"
