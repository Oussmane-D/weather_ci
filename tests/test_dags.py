import pathlib
import pytest
from airflow.models import DagBag

# 1) On repère le dossier 'dags' à partir de la racine du projet
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
DAGS_FOLDER = PROJECT_ROOT / "dags"

@pytest.fixture(scope="session")
def dagbag():
    """
    Charge tous les DAGs depuis le dossier DAGS_FOLDER
    sans prendre en compte les exemples fournis par Airflow.
    """
    return DagBag(dag_folder=str(DAGS_FOLDER), include_examples=False)

def test_no_import_errors(dagbag):
    """
    Aucun import de DAG ne doit planter.
    """
    errors = dagbag.import_errors
    assert not errors, f"Import errors: {errors}"

def test_at_least_one_dag_loaded(dagbag):
    """
    On s'assure qu'au moins un DAG a bien été découvert.
    """
    dag_ids = dagbag.dag_ids
    assert dag_ids, "Aucun DAG n'a été chargé dans le dossier 'dags'"
