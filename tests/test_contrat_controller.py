import pytest
from backend.models import Contrat, Base
from .test_config import TestingSessionLocal
from backend.controllers.contrat_controller import (
    create_contrat_controller,
    get_all_contrats_controller,
    get_contrat_controller,
    update_contrat_controller,
    delete_contrat_controller,
)

# Rediriger la session du repository vers la base de test
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
    data = {
        "client_id": 1,
        "commercial_id": 2,
        "total_amount": 1000.0,
        "outstanding_amount": 500.0,
        "signed": False
    }
    data.update(overrides)
    return data


def test_create_contrat_controller():
    contrat = create_contrat_controller(**fake_contrat_data())
    assert contrat.id is not None
    assert contrat.total_amount == 1000.0


def test_get_all_contrats_controller():
    create_contrat_controller(**fake_contrat_data())
    create_contrat_controller(**fake_contrat_data(outstanding_amount=0, signed=True))
    result = get_all_contrats_controller()
    assert isinstance(result, list)
    assert len(result) == 2


def test_get_all_contrats_empty():
    result = get_all_contrats_controller()
    assert isinstance(result, dict)
    assert result["error"] == "Aucun Contrat trouvé."


def test_get_contrat_controller():
    contrat = create_contrat_controller(**fake_contrat_data(client_id=42))
    result = get_contrat_controller(contrat.id)
    assert result.id == contrat.id
    assert result.client_id == 42


def test_get_contrat_controller_not_found():
    result = get_contrat_controller(999)
    assert isinstance(result, dict)
    assert result["error"] == "Aucun Contrat trouvé."


def test_get_contrats_signed():
    create_contrat_controller(**fake_contrat_data(signed=False))
    create_contrat_controller(**fake_contrat_data(signed=True))
    result = get_all_contrats_controller(signed=True)
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].signed == 1


def test_get_contrats_not_signed():
    create_contrat_controller(**fake_contrat_data(signed=True))
    create_contrat_controller(**fake_contrat_data(signed=False))
    result = get_all_contrats_controller(not_signed=True)
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].signed == 0


def test_get_contrats_paid():
    create_contrat_controller(**fake_contrat_data(outstanding_amount=100))
    create_contrat_controller(**fake_contrat_data(outstanding_amount=0))
    result = get_all_contrats_controller(paid=True)
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].outstanding_amount == 0


def test_get_contrats_not_paid():
    create_contrat_controller(**fake_contrat_data(outstanding_amount=0))
    create_contrat_controller(**fake_contrat_data(outstanding_amount=250))
    result = get_all_contrats_controller(not_paid=True)
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].outstanding_amount > 0


def test_update_contrat_controller():
    contrat = create_contrat_controller(**fake_contrat_data())
    updated = update_contrat_controller(
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


def test_update_contrat_controller_not_found():
    result = update_contrat_controller(999, client_id=1)
    assert isinstance(result, dict)
    assert result["error"] == "Aucun Contrat trouvé ou la modification a échouée."


def test_delete_contrat_controller():
    contrat = create_contrat_controller(**fake_contrat_data())
    deleted = delete_contrat_controller(contrat.id)
    assert deleted.id == contrat.id


def test_delete_contrat_controller_not_found():
    result = delete_contrat_controller(999)
    assert isinstance(result, dict)
    assert result["error"] == "Aucun Contrat trouvé ou ne peut pas être supprimé.."
