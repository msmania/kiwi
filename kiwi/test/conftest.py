import pytest
from kiwi import create_app

@pytest.fixture(scope = 'session')
def app():
  app = create_app()
  return app
