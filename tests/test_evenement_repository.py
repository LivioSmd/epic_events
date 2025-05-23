import pytest
from datetime import datetime, timedelta
from backend.models import Evenement, Base
from .test_config import TestingSessionLocal
from backend.repository.evenement_repository import (
    add_evenement,
    get_evenements,
    get_a_evenement,
    update_evenement,
    delete_evenement,
)
# Remplacer la session utilisée dans le repository par celle de test
import backend.repository.evenement_repository as repo
repo.SessionLocal = TestingSessionLocal


@pytest.fixture(autouse=True)
def setup_teardown():
    """Reinitialize the database before each test."""
    session = TestingSessionLocal()
    Base.metadata.drop_all(bind=session.bind)
    Base.metadata.create_all(bind=session.bind)
    yield
    session.close()


def fake_evenement_data(**overrides):
    """Returns fake event data."""
    now = datetime.now()
    data = {
        "contrat_id": 1,
        "client_name": "Test Client",
        "client_contact_id": 101,
        "support_id": None,
        "start_date": now,
        "end_date": now + timedelta(hours=2),
        "location": "Paris",
        "expected": 50,
        "notes": "Note de test",
    }
    data.update(overrides)
    return data


def test_add_evenement():
    data = fake_evenement_data()
    ev = add_evenement(**data)
    assert ev.id is not None
    assert ev.client_name == "Test Client"


def test_get_evenements_all():
    add_evenement(**fake_evenement_data(client_name="A"))
    add_evenement(**fake_evenement_data(client_name="B", support_id=42))
    evts = get_evenements()
    assert len(evts) == 2


def test_get_evenements_no_support():
    add_evenement(**fake_evenement_data(support_id=None))
    add_evenement(**fake_evenement_data(support_id=12))
    result = get_evenements(no_support=True)
    assert len(result) == 1
    assert result[0].support_id is None


def test_get_evenements_with_support():
    add_evenement(**fake_evenement_data(support_id=None))
    add_evenement(**fake_evenement_data(support_id=24))
    result = get_evenements(support=True)
    assert len(result) == 1
    assert result[0].support_id == '24'


def test_get_evenements_by_support_id():
    add_evenement(**fake_evenement_data(support_id=1))
    add_evenement(**fake_evenement_data(support_id=2))
    result = get_evenements(support_id=2)
    assert len(result) == 1
    assert result[0].support_id == '2'


def test_get_a_evenement():
    ev = add_evenement(**fake_evenement_data(client_name="Unique Client"))
    fetched = get_a_evenement(ev.id)
    assert fetched.id == ev.id
    assert fetched.client_name == "Unique Client"


def test_update_evenement():
    ev = add_evenement(**fake_evenement_data(client_name="Old Name", support_id=None))
    updated = update_evenement(ev.id, client_name="New Name", support_id=99)
    assert updated.client_name == "New Name"
    assert updated.support_id == '99'


def test_delete_evenement():
    ev = add_evenement(**fake_evenement_data())
    delete_evenement(ev.id)
    result = get_evenements()
    assert all(e.id != ev.id for e in result)
