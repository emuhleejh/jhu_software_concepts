import pytest
from src.flask_app import page
import re

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

def test_check_for_answer(client):
    response = client.get("/")
    response_text = response.data.decode("utf-8")
    count_answer = response_text.count("Answer")
    assert count_answer > 10

def test_check_percent_format(client):
    response = client.get("/")
    response_text = response.data.decode("utf-8")
    
    percent_re = ("\.\d{2}%")
    count_regex = re.compile(percent_re)
    formatted_percent_count = len(count_regex.findall(response_text))

    assert formatted_percent_count == 2
    