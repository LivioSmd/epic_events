import pytest
from backend.models import Contrat, Base
from .test_config import TestingSessionLocal
from backend.repository.contrat_repository import (
    add_contrat,
    get_contrats,
    get_a_contrat,
    update_contrat,
    delete_contrat,
)

# Remplace la session dans le repository par celle de test
import backend.repository.contrat_repository as repo
repo.SessionLocal = TestingSessionLocal


@pytest.fixture(autouse=True)
def setup_teardown():
    """Réinitialise la base de données avant chaque test."""
    session = TestingSessionLocal()
    Base.metadata.drop_all(bind=session.bind)
    Base.metadata.create_all(bind=session.bind)
    yield
    session.close()


def fake_contrat_data(**overrides):
    """Retourne des données factices pour un contrat."""
    data = {
        "client_id": 1,
        "commercial_id": 2,
        "total_amount": 1000.0,
        "outstanding_amount": 500.0,
        "signed": False,
    }
    data.update(overrides)
    return data


def test_add_contrat():
    contrat = add_contrat(**fake_contrat_data())
    assert contrat.id is not None
    assert contrat.total_amount == 1000.0
    assert contrat.signed == 0


def test_get_all_contrats():
    add_contrat(**fake_contrat_data())
    add_contrat(**fake_contrat_data(outstanding_amount=0, signed=True))
    contrats = get_contrats()
    assert len(contrats) == 2


def test_get_signed_contrats():
    add_contrat(**fake_contrat_data(signed=False))
    add_contrat(**fake_contrat_data(signed=True))
    result = get_contrats(signed=True)
    assert len(result) == 1
    assert result[0].signed == 1


def test_get_not_signed_contrats():
    add_contrat(**fake_contrat_data(signed=False))
    add_contrat(**fake_contrat_data(signed=True))
    result = get_contrats(not_signed=True)
    assert len(result) == 1
    assert result[0].signed == 0


def test_get_paid_contrats():
    add_contrat(**fake_contrat_data(outstanding_amount=100))
    add_contrat(**fake_contrat_data(outstanding_amount=0))
    result = get_contrats(paid=True)
    assert len(result) == 1
    assert result[0].outstanding_amount == 0


def test_get_not_paid_contrats():
    add_contrat(**fake_contrat_data(outstanding_amount=0))
    add_contrat(**fake_contrat_data(outstanding_amount=250))
    result = get_contrats(not_paid=True)
    assert len(result) == 1
    assert result[0].outstanding_amount > 0


def test_get_a_contrat():
    contrat = add_contrat(**fake_contrat_data(client_id=42))
    fetched = get_a_contrat(contrat.id)
    assert fetched.id == contrat.id
    assert fetched.client_id == 42


def test_update_contrat():
    contrat = add_contrat(**fake_contrat_data())
    updated = update_contrat(
        contrat.id,
        client_id=99,
        commercial_id=88,
        total_amount=5000,
        outstanding_amount=0,
        signed=True
    )
    assert updated.client_id == 99
    assert updated.commercial_id == 88
    assert updated.total_amount == 5000
    assert updated.outstanding_amount == 0
    assert updated.signed == 1


def test_delete_contrat():
    contrat = add_contrat(**fake_contrat_data())
    delete_contrat(contrat.id)
    remaining = get_contrats()
    assert all(c.id != contrat.id for c in remaining)
