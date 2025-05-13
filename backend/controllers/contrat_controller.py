from backend.repository.contrat_repository import get_contrats, get_a_contrat, add_contrat, update_contrat, \
    delete_contrat


def get_all_contrats_controller(not_signed=False, signed=False, not_paid=False, paid=False):
    """Retrieve all contrats."""
    if not_signed:
        contrats = get_contrats(not_signed=not_signed)
    elif signed:
        contrats = get_contrats(signed=signed)
    elif not_paid:
        contrats = get_contrats(not_paid=not_paid)
    elif paid:
        contrats = get_contrats(paid=paid)
    else:
        contrats = get_contrats()

    if not contrats:
        return {"error": "Aucun Contrat trouvé."}
    return contrats


def get_contrat_controller(contrat_id):
    """Retrieve a contrat."""
    contrat = get_a_contrat(contrat_id)

    if not contrat:
        return {"error": "Aucun Contrat trouvé."}
    return contrat


def create_contrat_controller(client_id, commercial_id, total_amount, outstanding_amount, signed):
    contrat = add_contrat(client_id, commercial_id, total_amount, outstanding_amount, signed)
    return contrat


def update_contrat_controller(contrat_id, client_id=None, commercial_id=None, total_amount=None,
                              outstanding_amount=None, signed=None):
    contrat = update_contrat(contrat_id, client_id, commercial_id, total_amount, outstanding_amount, signed)
    if not contrat:
        return {"error": "Aucun Contrat trouvé ou la modification a échouée."}
    else:
        return contrat


def delete_contrat_controller(contrat_id):
    contrat_deleted = delete_contrat(contrat_id)

    if not contrat_deleted:
        return {"error": "Aucun Contrat trouvé ou ne peut pas être supprimé.."}
    else:
        return contrat_deleted
