from backend.repository.user_repository import add_user, get_users, update_user, delete_user, get_a_user


def get_all_users_controller():
    """Retrieve all users."""
    users = get_users()

    if not users:
        return {"error": "Aucun User trouvé."}
    return users


def get_user_controller(user_id):
    """Retrieve a user."""
    user = get_a_user(user_id)

    if not user:
        return {"error": "Aucun User trouvé."}
    return user


def create_user_controller(name, email, user_type, password):
    user = add_user(name, email, user_type, password)
    return user


def update_user_controller(user_id, name=None, email=None, user_type=None):
    user = update_user(user_id, name, email, user_type)
    if not user:
        return {"error": "Aucun User trouvé ou la modification a échouée."}
    else:
        return user


def delete_user_controller(user_id):
    user_deleted = delete_user(user_id)

    if not user_deleted:
        return {"error": "Aucun User trouvé ou ne peut pas être supprimé."}
    else:
        return user_deleted
