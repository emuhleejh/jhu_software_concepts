import pytest
from src.flask_app import create_app

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

@pytest.mark.web
def test_flask_app_created(client):
    app_return = client.get("/")
    assert app_return.status_code == 200

@pytest.mark.web
def test_flask_app_contains_update_button(client):
    response = client.get("/")
    assert b"<form action=\"/update-analysis/\">" in response.data

@pytest.mark.web
def test_flask_app_contains_pull_button(client):
    response = client.get("/")
    assert b"<form action=\"/pull-data/\">" in response.data

@pytest.mark.web
def test_flask_app_contains_analysis(client):
    response = client.get("/")
    assert b"Analysis" in response.data

@pytest.mark.web
def test_flask_app_contains_answer(client):
    response = client.get("/")
    assert b"Answer:" in response.data
