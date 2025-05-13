from backend.db import SessionLocal
from backend.jwt_manager import generate_token
from backend.models.user import User


def get_users():
    """Retrieve all users."""
    session = SessionLocal()
    users = session.query(User).all()
    session.close()
    return users


def get_a_user(user_id):
    """Retrieve a user by id."""
    session = SessionLocal()
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        session.close()
        return user


def add_user(name, email, user_type, password):
    """Add a new user."""
    session = SessionLocal()
    new_user = User(name=name, email=email, type=user_type)
    new_user.set_password(password)  # Hashes and stores the password
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    session.close()
    return new_user


def update_user(user_id, name=None, email=None, user_type=None):
    """Update a user's details."""
    session = SessionLocal()
    user = session.query(User).filter(User.id == user_id).first()

    if not user:
        print("Utilisateur introuvable.")
        session.close()
        return None

    if name:
        user.name = name
    if email:
        user.email = email
    if user_type:
        user.type = user_type

    session.commit()
    session.refresh(user)
    session.close()
    return user


def delete_user(user_id):
    """Delete a user by its ID."""
    session = SessionLocal()
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        session.delete(user)
        session.commit()
    session.close()
    return user


def authenticate_user(email, password):
    """Authenticate a user and return a JWT token."""
    session = SessionLocal()
    user = session.query(User).filter(User.email == email).first()
    session.close()

    if user and user.check_password(password):  # Check password and User
        token = generate_token(user.email, user.type, user.id)
        with open(".token", "w") as f:  # Save the token to a file
            f.write(token)
        return True
