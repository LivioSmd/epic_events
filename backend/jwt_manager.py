import jwt
import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in the .env file")


def generate_token(user_email, user_type, user_id):
    payload = {
        "email": user_email,
        "type": user_type,
        "user_id": user_id,
        "exp": datetime.datetime.now() + datetime.timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def verify_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        os.remove(".token")  # automatic disconnection / delete token file
        return {"error": "Token expiré."}
    except jwt.InvalidTokenError:
        return {"error": "Token invalide."}
