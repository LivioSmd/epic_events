from backend.db import SessionLocal
from backend.models.evenement import Evenement


def get_evenements(no_support=False, support=False, support_id=None):
    """Retrieve all evenements."""
    session = SessionLocal()
    if no_support:
        evenements = session.query(Evenement).filter(Evenement.support_id.is_(None)).all()
    elif support:
        evenements = session.query(Evenement).filter(Evenement.support_id.is_not(None)).all()
    elif support_id:
        evenements = session.query(Evenement).filter(Evenement.support_id == support_id).all()
    else:
        evenements = session.query(Evenement).all()
    session.close()
    return evenements


def get_a_evenement(evenement_id):
    """Retrieve a evenement by id."""
    session = SessionLocal()
    evenement = session.query(Evenement).filter(Evenement.id == evenement_id).first()
    if evenement:
        session.close()
        return evenement


def add_evenement(contrat_id, client_name, client_contact_id, support_id, start_date, end_date,
                  location, expected, notes):
    """Add a new Evenement."""
    session = SessionLocal()
    new_evenement = Evenement(contrat_id=contrat_id, client_name=client_name, client_contact_id=client_contact_id,
                              support_id=support_id, start_date=start_date, end_date=end_date, location=location,
                              expected=expected, notes=notes)
    session.add(new_evenement)
    session.commit()
    session.refresh(new_evenement)
    session.close()
    return new_evenement


def update_evenement(evenement_id, contrat_id=None, client_name=None, client_contact_id=None, start_date=None,
                     end_date=None, support_id=None, location=None, expected=None, notes=None):
    """Update a evenement's details."""
    session = SessionLocal()
    evenement = session.query(Evenement).filter(Evenement.id == evenement_id).first()

    if not evenement:
        print("Evenement introuvable.")
        session.close()
        return None

    if contrat_id:
        evenement.contrat_id = contrat_id
    if client_name:
        evenement.client_name = client_name
    if client_contact_id:
        evenement.client_contact_id = client_contact_id
    if start_date:
        evenement.start_date = start_date
    if end_date:
        evenement.end_date = end_date
    if support_id:
        evenement.support_id = support_id
    if location:
        evenement.location = location
    if expected:
        evenement.expected = expected
    if notes:
        evenement.notes = notes

    session.commit()
    session.refresh(evenement)
    session.close()
    return evenement


def delete_evenement(evenement_id):
    """Delete a evenement by its ID."""
    session = SessionLocal()
    evenement = session.query(Evenement).filter(Evenement.id == evenement_id).first()
    if evenement:
        session.delete(evenement)
        session.commit()
    session.close()
    return evenement
