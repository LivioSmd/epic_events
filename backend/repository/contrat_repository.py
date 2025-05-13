from backend.db import SessionLocal
from backend.models.contrat import Contrat


def get_contrats(not_signed=False, signed=False, not_paid=False, paid=False):
    """Retrieve all contrats."""
    session = SessionLocal()

    if not_signed:
        contrats = session.query(Contrat).filter(Contrat.signed.is_(False)).all()
    elif signed:
        contrats = session.query(Contrat).filter(Contrat.signed.is_(True)).all()
    elif not_paid:
        contrats = session.query(Contrat).filter(Contrat.outstanding_amount > 0).all()
    elif paid:
        contrats = session.query(Contrat).filter(Contrat.outstanding_amount == 0).all()
    else:
        contrats = session.query(Contrat).all()

    session.close()
    return contrats


def get_a_contrat(contrat_id):
    """Retrieve a contrat by id."""
    session = SessionLocal()
    contrat = session.query(Contrat).filter(Contrat.id == contrat_id).first()
    if contrat:
        session.close()
        return contrat


def add_contrat(client_id, commercial_id, total_amount, outstanding_amount, signed):
    """Add a new contrat."""
    session = SessionLocal()
    new_contrat = Contrat(client_id=client_id, commercial_id=commercial_id, total_amount=total_amount,
                          outstanding_amount=outstanding_amount, signed=signed)
    session.add(new_contrat)
    session.commit()
    session.refresh(new_contrat)
    session.close()
    return new_contrat


def update_contrat(contrat_id, client_id=None, commercial_id=None, total_amount=None, outstanding_amount=None,
                   signed=None):
    """Update a contrat's details."""
    session = SessionLocal()
    contrat = session.query(Contrat).filter(Contrat.id == contrat_id).first()

    if not contrat:
        print("Contrat introuvable.")
        session.close()
        return None

    if client_id:
        contrat.client_id = client_id
    if commercial_id:
        contrat.commercial_id = commercial_id
    if total_amount:
        contrat.total_amount = total_amount
    if outstanding_amount:
        contrat.outstanding_amount = outstanding_amount
    if signed:
        contrat.signed = signed

    session.commit()
    session.refresh(contrat)
    session.close()
    return contrat


def delete_contrat(contrat_id):
    """Delete a contrat by its ID."""
    session = SessionLocal()
    contrat = session.query(Contrat).filter(Contrat.id == contrat_id).first()
    if contrat:
        session.delete(contrat)
        session.commit()
    session.close()
    return contrat
