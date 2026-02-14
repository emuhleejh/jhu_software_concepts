import pytest
import requests
from src.flask_app import page
# from src.flask_app import create_app

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

def test_flask_app_created(client):
    assert client.get("/").status_code == 200

def test_flask_app_contains_update_button(client):
    response = client.get("/")
    assert b"<form action=\"/update-analysis/\">" in response.data

def test_flask_app_contains_pull_button(client):
    response = client.get("/")
    assert b"<form action=\"/pull-data/\">" in response.data

def test_flask_app_contains_analysis(client):
    response = client.get("/")
    assert b"Analysis" in response.data

def test_flask_app_contains_answer(client):
    response = client.get("/")
    assert b"Answer:" in response.data
