import importlib
import pathlib
import pytest
from airflow.models import DagBag

DAG_PATH = pathlib.Path(__file__).parents[1] / "dags"

@pytest.fixture(scope="session")
def dagbag():
    return DagBag(dag_folder=str(DAG_PATH), include_examples=False)

def test_no_import_errors(dagbag):
    assert len(dagbag.import_errors) == 0, f"Import errors: {dagbag.import_errors}"

def test_all_dags_loaded(dagbag):
    assert dagbag.dags, "Aucun DAG chargé !"
