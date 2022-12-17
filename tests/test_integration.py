import pytest
import requests
import subprocess
import time
import atexit

server = subprocess.Popen(['python3', 'app.py'])
time.sleep(1) # Server startup time. There's better ways to do this, but not easier.

def close_server():
    server.terminate()
    server.wait(10)
atexit.register(close_server)

# -----------------------------------------------------------------------------
# Endpoints that you need to implement
# -----------------------------------------------------------------------------

def test_get_ships():
    '''
    You need to create the endpoint: GET/ships
    It should produce a JSON response in the format: {
        "ships": [
            { "imo": 1, ... },
            ...
            { "imo": n, ... },
        ]
    }
    This should reflect the current state of the ship table.
    '''
    r = requests.get('http://localhost:8080/ships')
    assert r.status_code == 200, r.text
    assert r.headers['content-type'].startswith('application/json')
    assert r.json() == {
        "ships": [
            { "imo": "9632179", "ship_name": "Mathilde Maersk" },
            { "imo": "9247455", "ship_name": "Australian Spirit" },
            { "imo": "9595321", "ship_name": "MSC Preziosa" },
        ],
    }

def test_get_positions():
    '''
    You need to create the endpoint: get/positions/<imo>
    It should:
    1. Accept string arguments `imo`
    3. Produce a JSON response with all the data for the given imo
    '''
    def get(**kwargs):
        return requests.post('http://localhost:8080/positions', data = kwargs)
    
    pass


@pytest.mark.parametrize('method', ['PUT', 'PATCH', 'DELETE', 'FARFAGNUGEN'])
def test_unsupported_methods(method):
    '''
    For other methods, the ships endpoint should respond with a 405 error.
    '''
    r = requests.request(method, 'http://localhost:8080/ships')
    assert r.status_code == 405, r.text
    assert "Method Not Allowed" in r.text

# -----------------------------------------------------------------------------
# Starter behavior, that you just don't want to damage
# -----------------------------------------------------------------------------
def test_get_root():
    '''
    The root endpoint (GET /) should return a simple text response.
    '''
    r = requests.get('http://localhost:8080/')
    assert r.status_code == 200, r.text
    assert r.headers['content-type'].startswith('text/plain')
    assert r.text == 'Pole Star Candidate Exercise for Amit Kumar Dubey :)'

def test_404():
    '''
    Other routes should result in 404 responses.
    '''
    r = requests.get('http://localhost:8080/nowhere')
    assert r.status_code == 404