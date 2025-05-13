from backend.db import SessionLocal
from backend.models.client import Client


def get_clients():
    """Retrieve all clients."""
    session = SessionLocal()
    clients = session.query(Client).all()
    session.close()
    return clients


def get_a_client(client_id):
    """Retrieve a client by id."""
    session = SessionLocal()
    client = session.query(Client).filter(Client.id == client_id).first()
    if client:
        session.close()
        return client


def add_client(name, email, phone_number, company_name, user_contact_id, information):
    """Add a new user."""
    session = SessionLocal()
    new_client = Client(name=name, email=email, phone_number=phone_number, company_name=company_name,
                        user_contact_id=user_contact_id, information=information)
    session.add(new_client)
    session.commit()
    session.refresh(new_client)
    session.close()
    return new_client


def update_client(client_id, name=None, email=None, phone_number=None, company_name=None, information=None):
    """Update a client's details."""
    session = SessionLocal()
    client = session.query(Client).filter(Client.id == client_id).first()

    if not client:
        print("Client introuvable.")
        session.close()
        return None

    if name:
        client.name = name
    if email:
        client.email = email
    if phone_number:
        client.phone_number = phone_number
    if company_name:
        client.company_name = company_name
    if information:
        client.information = information

    session.commit()
    session.refresh(client)
    session.close()
    return client


def delete_client(client_id):
    """Delete a client by its ID."""
    session = SessionLocal()
    client = session.query(Client).filter(Client.id == client_id).first()
    if client:
        session.delete(client)
        session.commit()
    session.close()
    return client
