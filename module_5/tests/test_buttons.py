import sys
from os.path import dirname
sys.path.append(dirname(__file__))

import pytest
import src.flask_app as flask_app
from _pytest.monkeypatch import MonkeyPatch
from src.flask_app import create_app
from src.data_processing.query_data import Query
import src.data_processing.clean as clean
import src.data_processing.load_data as load_data

# Preliminary setup for testing app
import src.flask_app
@pytest.fixture()
def app():
    app = create_app()
    app.config.update({"TESTING" : True,})
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.mark.buttons
def test_pull_data(client):

    # Create and run mock function for running parser in test database with test data
    monkeypatch = MonkeyPatch()
    def mock_run_parser():
        print("Success")
    monkeypatch.setattr(src.flask_app, 'run_parser', mock_run_parser)
    pull_return = client.post("/pull-data/")

    # Check that clicking 'Pull Data' returns a status code of 200 when not busy
    assert pull_return.status_code == 200

@pytest.mark.buttons
def test_pull_data_busy(client):

    # Create and run mock function for running parser in test database with test data
    monkeypatch = MonkeyPatch()
    def mock_run_parser():
        src.flask_app.cache["pull-in-progress"] = True
    monkeypatch.setattr(src.flask_app, 'run_parser', mock_run_parser)
    client.post("/pull-data/")

    # Check that clicking 'Pull Data' returns a status code of 409 when busy
    assert client.post("/pull-data/").status_code == 409


@pytest.mark.buttons
def test_update_analysis(client):

    # Create and run mock function for updating query in test database with test data
    monkeypatch = MonkeyPatch()
    flask_app.cache["update-in-progress"] = False
    flask_app.cache["pull-in-progress"] = False
    def mock_update_query():
        return Query(src.flask_app.DBNAME, src.flask_app.USER, src.flask_app.PASSWORD)
    monkeypatch.setattr(src.flask_app, 'update_query', mock_update_query)
    update_return = client.post("/update-analysis/")

    # Check that clicking 'Update analysis' returns a status code of 200 when not busy
    assert update_return.status_code == 200

@pytest.mark.buttons
def test_update_analysis_busy(client):

    # Create and run mock function for updating query in test database with test data
    monkeypatch = MonkeyPatch()
    def mock_update_query():
        src.flask_app.cache["pull-in-progress"] = True
    monkeypatch.setattr(src.flask_app, "update_query", mock_update_query)
    client.post("/update-analysis/")
    update_return = client.post("/update-analysis/")

    # Check that clicking 'Update analysis' returns a status code of 409 when busy
    assert update_return.status_code == 409
