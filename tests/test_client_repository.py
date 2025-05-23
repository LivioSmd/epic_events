import pytest
from backend.models import Client, Base
from .test_config import TestingSessionLocal
from backend.repository.client_repository import (
    add_client,
    get_clients,
    get_a_client,
    update_client,
    delete_client,
)

# Remplacer la session utilisée dans le repository par celle de test
import backend.repository.client_repository as repo
repo.SessionLocal = TestingSessionLocal


@pytest.fixture(autouse=True)
def setup_teardown():
    """Reinitialize the database before each test."""
    session = TestingSessionLocal()
    Base.metadata.drop_all(bind=session.bind)
    Base.metadata.create_all(bind=session.bind)
    yield
    session.close()


def fake_client_data(**overrides):
    """Returns fake client data."""
    data = {
        "name": "Client Test",
        "email": "client@example.com",
        "phone_number": "0600000000",
        "company_name": "Entreprise Test",
        "user_contact_id": 1,
        "information": "Contact important",
    }
    data.update(overrides)
    return data


def test_add_client():
    client = add_client(**fake_client_data())
    assert client.id is not None
    assert client.name == "Client Test"
    assert client.email == "client@example.com"


def test_get_clients():
    add_client(**fake_client_data(name="A"))
    add_client(**fake_client_data(name="B", email="b@example.com"))
    clients = get_clients()
    assert len(clients) == 2


def test_get_a_client():
    client = add_client(**fake_client_data(name="Unique Client"))
    fetched = get_a_client(client.id)
    assert fetched.id == client.id
    assert fetched.name == "Unique Client"


def test_update_client():
    client = add_client(**fake_client_data(name="Old Name"))
    updated = update_client(client.id, name="New Name", email="new@example.com",
                            phone_number="0707070707", company_name="NewCorp", information="Nouveau contact")
    assert updated.name == "New Name"
    assert updated.email == "new@example.com"
    assert updated.phone_number == "0707070707"
    assert updated.company_name == "NewCorp"
    assert updated.information == "Nouveau contact"


def test_delete_client():
    client = add_client(**fake_client_data())
    delete_client(client.id)
    remaining = get_clients()
    assert all(c.id != client.id for c in remaining)
