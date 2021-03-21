import pytest
from coal_game_server.config import create_app
from coal_game_server.db import db


class TestConfig(object):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite://"  # in-memory
    # SQLALCHEMY_ECHO = True
    ENV = "test"


@pytest.fixture(scope="session")
def app():
    connex_app = create_app(TestConfig())
    connex_app.add_api("openapi.yaml", arguments={"title": "COAL Game Server"})

    yield connex_app.app


@pytest.fixture(scope="session")
def testapp(app):
    return app.test_client()


@pytest.fixture(scope="session")
def dbf(app):
    db.app = app
    db.create_all()

    yield db

    db.drop_all()


@pytest.fixture(scope="function", autouse=True)
def session(dbf):
    connection = dbf.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session_ = dbf.create_scoped_session(options=options)

    dbf.session = session_

    yield session_

    transaction.rollback()
    connection.close()
    session_.remove()
