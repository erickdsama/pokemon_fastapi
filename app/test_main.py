from starlette.testclient import TestClient

from main import app

# generate a TestClient for the FastApi session
client = TestClient(app)
