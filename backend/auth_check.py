from .jwt_manager import verify_token


def is_authenticated():
    try:
        with open(".token", "r") as f:
            token = f.read().strip()
    except FileNotFoundError:
        return {"error": "Non connecté. Faites `login` d'abord."}

    decoded = verify_token(token)
    if "error" in decoded:
        return decoded
    else:
        return decoded
