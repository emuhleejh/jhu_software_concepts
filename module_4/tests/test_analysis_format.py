import sys
from os.path import dirname
sys.path.append(dirname(__file__))

import pytest
from src.flask_app import create_app
import re

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

@pytest.mark.analysis
def test_check_for_answer(client):
    # Call website open
    response = client.get("/")
    response_text = response.data.decode("utf-8")

    # Count number of times 'Answer' appears in page
    count_answer = response_text.count("Answer")

    # Assert the count is greater than or equal to 13
    # 13 is the expected number as there are 13 questions and 13 answers
    assert count_answer >= 13

@pytest.mark.analysis
def test_check_percent_format(client):
    # Call website open
    response = client.get("/")
    response_text = response.data.decode("utf-8")
    
    # Count number of times a percent regex appears in page
    percent_re = ("\.\d{2}%")
    count_regex = re.compile(percent_re)
    formatted_percent_count = len(count_regex.findall(response_text))

    # Assert the count equals two
    # Two is the expected number as there are only two questions with percent answers
    assert formatted_percent_count == 2
    