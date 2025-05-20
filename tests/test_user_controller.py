import os
import pytest

os.environ["SECRET_KEY"] = "test_secret_key"
os.environ["DSN"] = "dummy_dsn"

from backend.models import User, Base
from .test_config import TestingSessionLocal
from backend.controllers.user_controller import (
    get_all_users_controller,
    get_user_controller,
    create_user_controller,
    update_user_controller,
    delete_user_controller,
)

# Remplacer la session du repository utilisé par les controllers
import backend.repository.user_repository as repo
repo.SessionLocal = TestingSessionLocal

@pytest.fixture(autouse=True)
def setup_teardown():
    """Réinitialise la base avant chaque test."""
    session = TestingSessionLocal()
    Base.metadata.drop_all(bind=session.bind)
    Base.metadata.create_all(bind=session.bind)
    yield
    session.close()


def test_create_user_controller():
    user = create_user_controller("Alice", "alice@example.com", "support", "password123")
    assert user.id is not None
    assert user.email == "alice@example.com"


def test_get_all_users_controller():
    create_user_controller("Bob", "bob@example.com", "support", "pass")
    create_user_controller("Charlie", "charlie@example.com", "commercial", "pass")
    result = get_all_users_controller()
    assert isinstance(result, list)
    assert len(result) == 2


def test_get_all_users_empty():
    result = get_all_users_controller()
    assert isinstance(result, dict)
    assert result["error"] == "Aucun User trouvé."


def test_get_user_controller():
    user = create_user_controller("Diane", "diane@example.com", "management", "pass")
    fetched = get_user_controller(user.id)
    assert fetched.id == user.id
    assert fetched.email == "diane@example.com"


def test_get_user_controller_not_found():
    result = get_user_controller(999)
    assert isinstance(result, dict)
    assert result["error"] == "Aucun User trouvé."


def test_update_user_controller():
    user = create_user_controller("Eve", "eve@example.com", "support", "pass")
    updated = update_user_controller(user.id, name="Eve Updated", email="eve@new.com", user_type="commercial")
    assert updated.name == "Eve Updated"
    assert updated.email == "eve@new.com"
    assert updated.type == "commercial"


def test_update_user_controller_not_found():
    result = update_user_controller(999, name="Ghost")
    assert isinstance(result, dict)
    assert result["error"] == "Aucun User trouvé ou la modification a échouée."


def test_delete_user_controller():
    user = create_user_controller("Frank", "frank@example.com", "support", "pass")
    deleted = delete_user_controller(user.id)
    assert deleted.id == user.id


def test_delete_user_controller_not_found():
    result = delete_user_controller(999)
    assert isinstance(result, dict)
    assert result["error"] == "Aucun User trouvé ou ne peut pas être supprimé."
