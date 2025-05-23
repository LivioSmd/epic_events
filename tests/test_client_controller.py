import pytest
from backend.models import Client, Base
from .test_config import TestingSessionLocal
from backend.controllers.client_controller import (
    create_client_controller,
    get_all_clients_controller,
    get_client_controller,
    update_client_controller,
    delete_client_controller,
)

# Rediriger les sessions vers la base de test
import backend.repository.client_repository as repo
repo.SessionLocal = TestingSessionLocal


@pytest.fixture(autouse=True)
def setup_teardown():
    """Réinitialize the database before each test."""
    session = TestingSessionLocal()
    Base.metadata.drop_all(bind=session.bind)
    Base.metadata.create_all(bind=session.bind)
    yield
    session.close()


def test_create_client_controller():
    client = create_client_controller(
        name="Client Test",
        email="client@test.com",
        phone_number="0600000000",
        company_name="TestCorp",
        user_contact_id=1,
        information="Info test"
    )
    assert client.id is not None
    assert client.name == "Client Test"
    assert client.email == "client@test.com"


def test_get_all_clients_controller():
    create_client_controller("A", "a@test.com", "0600000001", "A Corp", 1, "Info A")
    create_client_controller("B", "b@test.com", "0600000002", "B Corp", 2, "Info B")
    result = get_all_clients_controller()
    assert isinstance(result, list)
    assert len(result) == 2


def test_get_all_clients_empty():
    result = get_all_clients_controller()
    assert isinstance(result, dict)
    assert result["error"] == "Aucun Client trouvé."


def test_get_client_controller():
    client = create_client_controller("C", "c@test.com", "0600000003", "C Corp", 3, "Info C")
    result = get_client_controller(client.id)
    assert result.id == client.id
    assert result.name == "C"


def test_get_client_controller_not_found():
    result = get_client_controller(999)
    assert isinstance(result, dict)
    assert result["error"] == "Aucun Client trouvé."


def test_update_client_controller():
    client = create_client_controller("D", "d@test.com", "0600000004", "D Corp", 4, "Info D")
    updated = update_client_controller(
        client.id,
        name="D Updated",
        email="d@new.com",
        phone_number="0707070707",
        company_name="New D Corp",
        information="Updated info"
    )
    assert updated.name == "D Updated"
    assert updated.email == "d@new.com"
    assert updated.phone_number == "0707070707"
    assert updated.company_name == "New D Corp"
    assert updated.information == "Updated info"


def test_update_client_controller_not_found():
    result = update_client_controller(999, name="Ghost")
    assert isinstance(result, dict)
    assert result["error"] == "Aucun Client trouvé ou la modification a échouée."


def test_delete_client_controller():
    client = create_client_controller("E", "e@test.com", "0600000005", "E Corp", 5, "Info E")
    deleted = delete_client_controller(client.id)
    assert deleted.id == client.id


def test_delete_client_controller_not_found():
    result = delete_client_controller(999)
    assert isinstance(result, dict)
    assert result["error"] == "Aucun Client trouvé ou ne peut pas être supprimé."
