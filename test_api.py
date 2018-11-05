import pytest
from api import create_app, db as _db
import config

@pytest.fixture(scope='session')
def app():
    app = create_app(config.TestingConfig)
    return app
