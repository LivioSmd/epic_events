from backend.repository.client_repository import get_clients, add_client, get_a_client, update_client, delete_client


def get_all_clients_controller():
    """Retrieve all clients."""
    clients = get_clients()

    if not clients:
        return {"error": "Aucun Client trouvé."}
    return clients


def get_client_controller(client_id):
    """Retrieve a client."""
    user = get_a_client(client_id)

    if not user:
        return {"error": "Aucun Client trouvé."}
    return user


def create_client_controller(name, email, phone_number, company_name, user_contact_id, information):
    client = add_client(name, email, phone_number, company_name, user_contact_id, information)
    return client


def update_client_controller(client_id, name=None, email=None, phone_number=None, company_name=None, information=None):
    client = update_client(client_id, name, email, phone_number, company_name, information)
    if not client:
        return {"error": "Aucun Client trouvé ou la modification a échouée."}
    else:
        return client


def delete_client_controller(client_id):
    client_deleted = delete_client(client_id)

    if not client_deleted:
        return {"error": "Aucun Client trouvé ou ne peut pas être supprimé."}
    else:
        return client_deleted
