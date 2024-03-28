import sys

import pytest
from alembic import command as alembic_command
from alembic.config import Config
from fastapi.testclient import TestClient
from opentelemetry import trace

sys.path = ["", ".."] + sys.path[1:]
from config import settings  # noqa: E402
from main import app  # noqa: E402

alembic_config = Config("alembic.ini")
alembic_config.set_main_option("script_location", "security/alembic")
alembic_config.set_main_option("sqlalchemy.url", settings.security_url)
alembic_config.set_section_option("logger_alembic", "level", "ERROR")


@pytest.fixture(scope="session", autouse=True)
def _prepare_database():
    assert settings.mode == "TEST"
    print("\n* TEST mode check == True")
    alembic_command.upgrade(alembic_config, "4187b8e8ecea")
    yield
    alembic_command.downgrade(alembic_config, "base")


@pytest.fixture(name="client", scope="session", autouse=True)
def client_fixture():
    with TestClient(app) as client:
        print(f"* Test Client created, id = {id(client)}")
        yield client
        print(f"\n* Test Client closed, id = {id(client)}")


@pytest.fixture(scope="session", autouse=True)
def _register(client):
    client.post(
        "/register/",
        headers={"accept": "application/json", "Content-Type": "application/json"},
        json={
            "username": settings.test_username,
            "email": settings.test_email,
            "password": settings.test_password,
            "role": settings.test_role,
        },
    )
    print("* Test user registered")


@pytest.fixture(scope="session")
def registry_token(client):
    response = client.post(
        "/login/",
        data={"username": settings.test_username, "password": settings.test_password},
    )
    print("* First login to take token to register")
    return response.json()["access_token"]


@pytest.fixture(scope="session", autouse=True)
def _verify_token(client, registry_token):
    client.get(f"/verify/{registry_token}")
    print("* User activated (verify token)")


@pytest.fixture(scope="session")
def token(client):
    """Log in and take token once for all tests that require authentication."""
    response = client.post(
        "/login/",
        data={"username": settings.test_username, "password": settings.test_password},
    )
    return response.json()["access_token"]


trace.get_tracer_provider().shutdown()
