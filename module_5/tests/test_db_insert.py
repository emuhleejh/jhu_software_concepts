import sys
from os.path import dirname
sys.path.append(dirname(__file__))

import pytest
from _pytest.monkeypatch import MonkeyPatch
from src.flask_app import create_app
import src.flask_app as flask_app
import src.data_processing.load_data as load_data
from src.data_processing.query_data import Query
from src.flask_app import update_query

# Preliminary setup for testing app

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({"TESTING" : True,})
    flask_app.DBNAME = "test_database"
    load_data.APPLICANT_DATA_FILE = "tests\\sample_llm_extend_applicant_data.json"
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.mark.db
def test_insert(client):

    # Set cache statuses to not busy
    flask_app.cache["pull-in-progress"]=False
    flask_app.cache["update-in-progress"]=False
    
    # Create and run mock function for running parser in test database with test data
    monkeypatch = MonkeyPatch()
    def mock_run_parser():
        load_data.clear_data()
        load_data.load_data(flask_app.DBNAME, flask_app.USER, flask_app.PASSWORD)
    monkeypatch.setattr(flask_app, 'run_parser', mock_run_parser)
    response = client.post("/pull-data/")

    # Only one test entry in test database, has GPA = 3.80
    # Average GPA must be 3.80
    assert b"Average GPA: 3.80" in response.data

@pytest.mark.db
def test_insert_duplicate(client):

    # Clear table
    load_data.clear_data()

    # Set cache statuses to not busy
    flask_app.cache["pull-in-progress"]=False
    flask_app.cache["update-in-progress"]=False

    # Create and run mock function for running parser in test database with test data
    monkeypatch = MonkeyPatch()
    def mock_run_parser():
        load_data.load_data(flask_app.DBNAME, flask_app.USER, flask_app.PASSWORD)
    monkeypatch.setattr(flask_app, 'run_parser', mock_run_parser)

    # Attempt to add the same data to the test database twice
    response = client.post("/pull-data/")
    response = client.post("/pull-data/")

    # Only one test entry in test database, applicant count must = 1
    assert b"Applicant Count: 1" in response.data
    
@pytest.mark.db
def test_query_dict(client):

    # Clear table
    load_data.clear_data()

    # Set cache statuses to not busy
    flask_app.cache["pull-in-progress"]=False
    flask_app.cache["update-in-progress"]=False

    # Create and run mock function for running parser in test database with test data
    monkeypatch = MonkeyPatch()
    def mock_run_parser():
        load_data.load_data(flask_app.DBNAME, flask_app.USER, flask_app.PASSWORD)
    monkeypatch.setattr(flask_app, 'run_parser', mock_run_parser)
    response = client.post("/pull-data/")

    # Update the query to get a dictionary of column headers from table
    test_data = update_query()

    # Check that a given key is in the dictionary of column headers
    assert hasattr(test_data, "avg_gpa") == True

@pytest.mark.db
def test_empty_db_pull(client):

    # Clear table
    load_data.clear_data()

    # Access database and run query against empty table
    query = Query(flask_app.DBNAME, flask_app.USER, flask_app.PASSWORD)

    query.run_query()

    # Check that given values are all empty
    valid = True
    if query.avg_accept_gpa_f26 != "0.00" or query.ct_select_phd_cs != 0 or query.ct_select_phd_cs_llm != 0:
        valid = False
    assert valid == True
