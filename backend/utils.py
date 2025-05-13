import re


def get_valid_name(name):
    """Validate and return a name (only letters, spaces, or hyphens)."""
    name = name.strip()

    if not name or name == "":
        return {"error": "Le nom ne peut pas être vide."}
    elif not re.match(r"^[a-zA-ZÀ-ÿ\s-]+$", name):
        return {"error": "Le nom ne doit contenir que des lettres et des espaces."}
    else:
        return name


def get_valid_string(value):
    """Validate and return a generic string matching a pattern (default: letters, numbers, spaces, hyphens)."""
    value = value.strip()

    if not value or value == "":
        return {"error": "Le champ ne peut pas être vide."}
    elif not re.match(r"^[\w\s-]+$", value):
        return {"error": "Le champ contient des caractères invalides."}
    else:
        return value


def get_valid_email(email):
    """Validate and return an email address."""
    email = email.lower().strip()

    if not email or email == "":
        return {"error": "L'email ne peut pas être vide."}
    elif not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        return {"error": "Veuillez entrer un email valide (ex: exemple@mail.com)."}
    else:
        return email


def get_valid_user_type(user_type):
    """Validate and return a user type (commercial, gestion, or support)."""
    user_type = user_type.strip()
    valid_types = ["commercial", "gestion", "support"]

    if not user_type or user_type == "":
        return {"error": "Le type d'utilisateur ne peut pas être vide."}
    elif user_type not in valid_types:
        return {"error": f"Invalid user type. Choose from {valid_types}"}
    else:
        return user_type


def get_valid_password(password):
    """Validate and return password."""
    password = password.strip()

    if not password or password == "":
        return {"error": "Le mot de passe ne peut pas être vide."}
    else:
        return password


def get_valid_int(the_int):
    """Validate and return a name (only letters, spaces, or hyphens)."""
    if isinstance(the_int, str):
        amount = the_int.strip()
        if amount == "":
            return {"error": "Le Int ne peut pas être vide."}
        try:
            the_int = int(amount)
        except ValueError:
            return {"error": "Le Int doit être un nombre valide."}

    if not isinstance(the_int, int) or the_int <= 0:
        return {"error": "Invalid Int."}
    else:
        return the_int


def get_valid_phone_number(phone):
    """Validate and return a phone number starting with '+' followed by digits."""
    phone = phone.strip()

    if not phone or phone == "":
        return {"error": "Le numéro de téléphone ne peut pas être vide."}
    elif not re.match(r"^\+\d{6,15}$", phone):
        return {"error": "Veuillez entrer un numéro valide commençant par '+' suivi de chiffres (ex: +33612345678)."}
    else:
        return phone


def get_valid_amount(amount):
    """Validate and return a positive amount (integer or float)."""
    if isinstance(amount, str):
        amount = amount.strip()
        if amount == "":
            return {"error": "Le montant ne peut pas être vide."}
        try:
            amount = float(amount)
        except ValueError:
            return {"error": "Le montant doit être un nombre valide."}

    if not isinstance(amount, (int, float)) or amount < 0:
        return {"error": "Le montant doit être un nombre positif."}
    else:
        return amount


def get_valid_boolean(boolean):
    """Validate and return a positive amount (integer or float)."""
    if boolean == "True" or boolean == "true":
        boolean = True
        return boolean
    elif boolean == "False" or boolean == "false":
        boolean = False
        return boolean
    else:
        return {"error": "Le champ doit être un booléen (True ou False)."}


def get_valid_written_date(value):
    """
    Valide que la date est au format : '1 janvier 2024' ou '12 mai 2025' (jour lettre année)
    """
    value = value.strip()

    # Regex : day (1-2 digits), space, month (letters), space, years (4 digits)
    if re.match(r"^\d{1,2} [a-zA-Zéèêàùûôîçäëïü\-]+ \d{4}$", value):
        return value
    else:
        return {"error": "Le format de la date est invalide. Utilisez une date comme '6 mai 2025'."}

