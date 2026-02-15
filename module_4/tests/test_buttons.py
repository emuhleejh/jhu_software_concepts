import pytest
from _pytest.monkeypatch import MonkeyPatch
from src.flask_app import page
from src.data_processing.query_data import Query

import src.flask_app
@pytest.fixture()
def app():
    app = page
    app.config.update({"TESTING" : True,})
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_pull_data(client):

    monkeypatch = MonkeyPatch()
    def mock_run_parser():
        print("Success")
    
    monkeypatch.setattr(src.flask_app, 'run_parser', mock_run_parser)
    pull_return = client.post("/pull-data/")
    assert pull_return.status_code == 200

def test_pull_data_busy(client):

    monkeypatch = MonkeyPatch()
    def mock_run_parser():
        src.flask_app.cache["pull-in-progress"] = True
    
    monkeypatch.setattr(src.flask_app, 'run_parser', mock_run_parser)
    client.post("/pull-data/")
    assert client.post("/pull-data/").status_code == 409


def test_update_analysis(client):

    monkeypatch = MonkeyPatch()
    def mock_update_query():
        src.flask_app.cache["update-in-progress"] = False
        src.flask_app.cache["pull-in-progress"] = False
        return Query(src.flask_app.dbname, src.flask_app.user, src.flask_app.password)
        
    
    monkeypatch.setattr(src.flask_app, 'update_query', mock_update_query)

    update_return = client.post("/update-analysis/")
    assert update_return.status_code == 200

def test_update_analysis_busy(client):

    monkeypatch = MonkeyPatch()
    def mock_update_query():
        src.flask_app.cache["pull-in-progress"] = True
    
    monkeypatch.setattr(src.flask_app, 'update_query', mock_update_query)

    client.post("/update-analysis/")
    update_return = client.post("/update-analysis/")
    assert update_return.status_code == 409
