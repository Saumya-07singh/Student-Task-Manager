import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app")))

from app import app

def test_home_page():
    response = app.test_client().get("/")
    assert response.status_code == 200