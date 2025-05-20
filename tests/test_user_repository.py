import os
import pytest

os.environ["SECRET_KEY"] = "test_secret_key"
os.environ["DSN"] = "dummy_dsn"

from backend.models import User, Base
from .test_config import TestingSessionLocal
from backend.repository.user_repository import (
    add_user,
    get_users,
    get_a_user,
    update_user,
    delete_user,
    authenticate_user,
)
# Remplacer SessionLocal dans les fonctions testées par notre session de test
import backend.repository.user_repository as repo

repo.SessionLocal = TestingSessionLocal


@pytest.fixture(autouse=True)
def setup_teardown():
    """Reset la base avant chaque test."""
    session = TestingSessionLocal()
    Base.metadata.drop_all(bind=session.bind)
    Base.metadata.create_all(bind=session.bind)
    yield
    session.close()


def test_add_user():
    user = add_user("Alice", "alice@example.com", "support", "password123")
    assert user.id is not None
    assert user.email == "alice@example.com"
    assert user.check_password("password123")


def test_get_users():
    add_user("User1", "u1@test.com", "support", "pass1")
    add_user("User2", "u2@test.com", "commercial", "pass2")
    users = get_users()
    assert len(users) == 2


def test_get_a_user():
    user = add_user("Unique", "unique@test.com", "support", "pass")
    fetched = get_a_user(user.id)
    assert fetched.email == "unique@test.com"


def test_update_user():
    user = add_user("Old Name", "old@test.com", "support", "pass")
    updated = update_user(user.id, name="New Name", email="new@test.com", user_type="commercial")
    assert updated.name == "New Name"
    assert updated.email == "new@test.com"
    assert updated.type == "commercial"


def test_delete_user():
    user = add_user("Temp", "temp@test.com", "support", "pass")
    delete_user(user.id)
    users = get_users()
    assert all(u.id != user.id for u in users)


def test_authenticate_user_failure():
    add_user("FailUser", "fail@test.com", "support", "rightpass")
    result = authenticate_user("fail@test.com", "wrongpass")
    assert result is None or result is False
