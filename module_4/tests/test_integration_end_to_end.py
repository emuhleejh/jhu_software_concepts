import sys
from os.path import dirname
sys.path.append(dirname(__file__))

import pytest
from _pytest.monkeypatch import MonkeyPatch
from src.flask_app import create_app
import src.flask_app as flask_app
import src.data_processing.load_data as load_data

# Preliminary setup for testing app
@pytest.fixture()
def app():
    app = create_app()
    app.config.update({"TESTING" : True,})
    flask_app.dbname = "test_database"
    load_data.applicant_data_file = "tests\\sample_llm_extend_applicant_data_multiple.json"
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.mark.integration
def test_end_to_end(client):

    # Clear data
    load_data.clear_data()

    # Create and run mock function for running parser in test database with test data
    monkeypatch = MonkeyPatch()
    def mock_run_parser():
        load_data.load_data(flask_app.dbname, flask_app.user, flask_app.password)
    monkeypatch.setattr(flask_app, 'run_parser', mock_run_parser)
    client.post("/pull-data/")

    # Set cache statuses to not busy
    flask_app.cache["pull-in-progress"]=False
    flask_app.cache["update-in-progress"]=False

    # Update analysis from test database
    client.post("/update-analysis/")
    response = client.get("/")

    # Only four entries in test database, applicant count must = 4
    assert b"Applicant Count: 4" in response.data

@pytest.mark.integration
def test_end_to_end_uniqueness(client):
    
    # Create and run mock function for running parser in test database with test data
    monkeypatch = MonkeyPatch()
    def mock_run_parser():
        load_data.load_data(flask_app.dbname, flask_app.user, flask_app.password)
    monkeypatch.setattr(flask_app, 'run_parser', mock_run_parser)
    response = client.post("/pull-data/")

    # Set cache statuses to not busy
    flask_app.cache["pull-in-progress"]=False
    flask_app.cache["update-in-progress"]=False

    # Attempt to post duplicate data
    response = client.post("/pull-data/")

    # Only four entries in test database
    # If uniqueness requirements are imposed, applicant count must = 4
    assert b"Applicant Count: 4" in response.data