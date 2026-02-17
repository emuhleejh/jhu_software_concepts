import pytest
from _pytest.monkeypatch import MonkeyPatch
from src.flask_app import create_app
import src.flask_app as flask_app
import src.data_processing.load_data as load_data

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({"TESTING" : True,})
    flask_app.dbname = "test_database"
    load_data.applicant_data_file = "tests\\sample_llm_extend_applicant_data.json"
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.mark.db
def test_insert(client):

    flask_app.cache["pull-in-progress"]=False
    flask_app.cache["update-in-progress"]=False
    monkeypatch = MonkeyPatch()

    def mock_run_parser():
        load_data.clear_data()
        load_data.load_data(flask_app.dbname, flask_app.user, flask_app.password)

    monkeypatch.setattr(flask_app, 'run_parser', mock_run_parser)

    response = client.post("/pull-data/")
    assert b"Average GPA: 3.80" in response.data

@pytest.mark.db
def test_insert_duplicate(client):

    load_data.clear_data()
    flask_app.cache["pull-in-progress"]=False
    flask_app.cache["update-in-progress"]=False

    monkeypatch = MonkeyPatch()
    def mock_run_parser():
        load_data.load_data(flask_app.dbname, flask_app.user, flask_app.password)
        

    monkeypatch.setattr(flask_app, 'run_parser', mock_run_parser)

    response = client.post("/pull-data/")
    response = client.post("/pull-data/")

    assert b"Applicant Count: 1" in response.data
    
@pytest.mark.db
def test_query_dict(client):

    load_data.clear_data()
    flask_app.cache["pull-in-progress"]=False
    flask_app.cache["update-in-progress"]=False
    
    monkeypatch = MonkeyPatch()
    def mock_run_parser():
        load_data.load_data(flask_app.dbname, flask_app.user, flask_app.password)

    monkeypatch.setattr(flask_app, 'run_parser', mock_run_parser)

    response = client.post("/pull-data/")

    test_data = flask_app.update_query()

    assert hasattr(test_data, "avg_gpa") == True