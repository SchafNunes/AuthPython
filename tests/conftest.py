import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from main import create_app
from app.extensions import db

class TestConfig:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:@localhost/noticersstest'
    TESTING = True
    SECRET_KEY = 'supersecretkey'
    JWT_SECRET_KEY = 'superjwtsecretkey'

@pytest.fixture(scope="module")
def test_client():

    flask_app = create_app(TestConfig)

    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    db.create_all()

    yield testing_client  

    db.session.remove()
    db.drop_all()
    ctx.pop()

@pytest.fixture(scope="module")
def test_model():

    flask_app = create_app(TestConfig)

    testing_model = flask_app.test_model()

    ctx = flask_app.app_context()
    ctx.push()

    db.create_all()

    yield testing_model  

    db.session.remove()
    db.drop_all()
    ctx.pop()
