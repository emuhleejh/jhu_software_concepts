import requests

def test_pull_data():
    assert requests.get().status_code == 200