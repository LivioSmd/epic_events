import pytest
from datetime import datetime, timedelta
from backend.models import Evenement, Base
from .test_config import TestingSessionLocal
from backend.controllers.evenement_controller import (
    create_evenement_controller,
    get_all_evenements_controller,
    get_evenement_controller,
    update_evenement_controller,
    delete_evenement_controller,
)

# Rediriger la session utilisée dans le repository vers la session de test
import backend.repository.evenement_repository as repo
repo.SessionLocal = TestingSessionLocal


@pytest.fixture(autouse=True)
def setup_teardown():
    """Réinitialise la base avant chaque test."""
    session = TestingSessionLocal()
    Base.metadata.drop_all(bind=session.bind)
    Base.metadata.create_all(bind=session.bind)
    yield
    session.close()


def fake_evenement_data(**overrides):
    now = datetime.now()
    data = {
        "contrat_id": 1,
        "client_name": "Client Test",
        "client_contact_id": 100,
        "support_id": None,
        "start_date": now,
        "end_date": now + timedelta(hours=2),
        "location": "Paris",
        "expected": 50,
        "notes": "Réunion de test",
    }
    data.update(overrides)
    return data


def test_create_evenement_controller():
    data = fake_evenement_data()
    ev = create_evenement_controller(**data)
    assert ev.id is not None
    assert ev.client_name == "Client Test"


def test_get_all_evenements_controller():
    create_evenement_controller(**fake_evenement_data(client_name="A"))
    create_evenement_controller(**fake_evenement_data(client_name="B", support_id=2))
    result = get_all_evenements_controller()
    assert isinstance(result, list)
    assert len(result) == 2


def test_get_all_evenements_empty():
    result = get_all_evenements_controller()
    assert isinstance(result, dict)
    assert result["error"] == "Aucun Evenement trouvé."


def test_get_evenement_controller():
    ev = create_evenement_controller(**fake_evenement_data(client_name="Unique"))
    fetched = get_evenement_controller(ev.id)
    assert fetched.id == ev.id
    assert fetched.client_name == "Unique"


def test_get_evenement_controller_not_found():
    result = get_evenement_controller(999)
    assert isinstance(result, dict)
    assert result["error"] == "Aucun Evenement trouvé."


def test_get_evenements_by_support_id():
    create_evenement_controller(**fake_evenement_data(support_id=1))
    create_evenement_controller(**fake_evenement_data(support_id=2))
    result = get_all_evenements_controller(support_id=2)
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].support_id == '2'


def test_get_evenements_with_support():
    create_evenement_controller(**fake_evenement_data(support_id=None))
    create_evenement_controller(**fake_evenement_data(support_id=10))
    result = get_all_evenements_controller(support=True)
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].support_id == '10'


def test_get_evenements_no_support():
    create_evenement_controller(**fake_evenement_data(support_id=None))
    create_evenement_controller(**fake_evenement_data(support_id=99))
    result = get_all_evenements_controller(no_support=True)
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].support_id is None


def test_update_evenement_controller():
    ev = create_evenement_controller(**fake_evenement_data(client_name="Old"))
    updated = update_evenement_controller(ev.id, client_name="New", location="Lyon", expected=100)
    assert updated.client_name == "New"
    assert updated.location == "Lyon"
    assert updated.expected == 100


def test_update_evenement_controller_not_found():
    result = update_evenement_controller(999, client_name="Ghost")
    assert isinstance(result, dict)
    assert result["error"] == "Aucun Evenement trouvé ou la modification a échouée."


def test_delete_evenement_controller():
    ev = create_evenement_controller(**fake_evenement_data())
    deleted = delete_evenement_controller(ev.id)
    assert deleted.id == ev.id


def test_delete_evenement_controller_not_found():
    result = delete_evenement_controller(999)
    assert isinstance(result, dict)
    assert result["error"] == "Aucun Evenement trouvé ou ne peut pas être supprimé."
