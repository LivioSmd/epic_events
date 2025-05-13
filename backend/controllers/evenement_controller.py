from backend.repository.evenement_repository import get_evenements, get_a_evenement, add_evenement, update_evenement, \
    delete_evenement


def get_all_evenements_controller(no_support=False, support=False, support_id=None):
    """Retrieve all evenements."""
    if no_support:
        evenements = get_evenements(no_support=no_support)
    elif support:
        evenements = get_evenements(support=support)
    elif support_id:
        evenements = get_evenements(support_id=support_id)
    else:
        evenements = get_evenements()

    if not evenements:
        return {"error": "Aucun Evenement trouvé."}
    return evenements


def get_evenement_controller(evenement_id):
    """Retrieve a evenement."""
    evenement = get_a_evenement(evenement_id)

    if not evenement:
        return {"error": "Aucun Evenement trouvé."}
    return evenement


def create_evenement_controller(contrat_id, client_name, client_contact_id, support_id, start_date, end_date, location,
                                expected, notes):
    evenement = add_evenement(contrat_id, client_name, client_contact_id, support_id, start_date, end_date, location,
                              expected, notes)
    return evenement


def update_evenement_controller(evenement_id, contrat_id=None, client_name=None, client_contact_id=None,
                                start_date=None, end_date=None, support_id=None, location=None, expected=None,
                                notes=None):
    evenement = update_evenement(evenement_id, contrat_id, client_name, client_contact_id, start_date, end_date,
                                 support_id, location, expected, notes)
    if not evenement:
        return {"error": "Aucun Evenement trouvé ou la modification a échouée."}
    else:
        return evenement


def delete_evenement_controller(evenement_id):
    evenement_deleted = delete_evenement(evenement_id)

    if not evenement_deleted:
        return {"error": "Aucun Evenement trouvé ou ne peut pas être supprimé."}
    else:
        return evenement_deleted
