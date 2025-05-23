import os
import click
import sentry_sdk
from dotenv import load_dotenv
from backend.auth_check import is_authenticated
from backend.controllers.client_controller import get_all_clients_controller, create_client_controller, \
    get_client_controller, update_client_controller, delete_client_controller
from backend.controllers.contrat_controller import get_all_contrats_controller, create_contrat_controller, \
    get_contrat_controller, update_contrat_controller, delete_contrat_controller
from backend.controllers.evenement_controller import create_evenement_controller, get_all_evenements_controller, \
    get_evenement_controller, update_evenement_controller, delete_evenement_controller
from backend.controllers.user_controller import create_user_controller, get_all_users_controller, \
    update_user_controller, delete_user_controller, get_user_controller
from backend.repository.user_repository import authenticate_user
from backend.utils import get_valid_name, get_valid_email, get_valid_password, get_valid_user_type, get_valid_int, \
    get_valid_string, get_valid_phone_number, get_valid_amount, get_valid_boolean

# Load environment variables from .env file
load_dotenv()
DSN = os.getenv("DSN")
if not DSN:
    raise ValueError("DSN is not set in the .env file")

# is_authenticated() verify if the user is connected and if so, it returns dict with the email, type and id of the user
connected_user = is_authenticated()
connected_user_type = None
connected_user_id = None
if not 'error' in connected_user:
    connected_user_type = get_valid_user_type(connected_user["type"])
    connected_user_id = get_valid_int(connected_user["user_id"])


@click.group()
def cli():
    """CRM CLI Application"""
    pass


@click.command()
def list_users():
    """Get all users"""

    if connected_user_type in ("gestion", "commercial", "support"):
        result = get_all_users_controller()

        if not is_valid(result):
            return
        else:
            click.echo(f"--- Users List: ---")
            for user in result:
                click.echo(f"[{user.id}] - {user.name} - {user.email} - [{user.type}]")
    else:
        lackRightError()
        return


@click.command()
@click.argument("user_id", type=int)  # type is used to specify the type (generate automatically an error)
def get_user(user_id):
    """Get a user"""

    if connected_user_type in ("gestion", "commercial", "support"):
        result = get_user_controller(user_id)

        if not is_valid(result):
            return
        else:
            user = result
            click.echo(f"User: [{user.id}] - {user.name} - {user.email} - [{user.type}]")
    else:
        lackRightError()
        return


@click.command()
@click.argument("name")
@click.argument("email")
@click.argument("user_type")
@click.argument("password")
def create_user(name, email, user_type, password):
    """Create a new user"""

    if connected_user_type == "gestion":
        name = get_valid_name(name)
        email = get_valid_email(email)
        user_type = get_valid_user_type(user_type)
        password = get_valid_password(password)

        # Vérifie chaque champ
        if (not is_valid(name)
                or not is_valid(email)
                or not is_valid(user_type)
                or not is_valid(password)):
            return

        result = create_user_controller(name=name, email=email, user_type=user_type, password=password)
        if isinstance(result, dict):
            click.echo(f"Erreur: {result['error']}")
        else:
            click.echo(f"User {result.name} created successfully.")
    else:
        lackRightError()
        return


@click.command()
@click.argument("user_id", type=int)  # type is used to specify the type (generate automatically an error)
@click.option("--name", help="New name")  # Optional arguments, help is the description for --help
@click.option("--email", help="New email")
@click.option("--user_type", help="New user type")
def update_user(user_id, name, email, user_type):
    """Update a user's details"""

    if connected_user_type == "gestion":
        user_id = get_valid_int(user_id)
        if name:
            name = get_valid_name(name)
        if email:
            email = get_valid_email(email)
        if user_type:
            user_type = get_valid_user_type(user_type)

        # Vérifie chaque champ
        if (not is_valid(user_id)
                or not is_valid(name)
                or not is_valid(email)
                or not is_valid(user_type)):
            return

        result = update_user_controller(user_id=user_id, name=name, email=email, user_type=user_type)
        if isinstance(result, dict):
            click.echo(f"Erreur: {result['error']}")
        else:
            click.echo(f"User {result.name} updated successfully.")
    else:
        lackRightError()
        return


@click.command()
@click.argument("user_id", type=int)
def delete_user(user_id):
    """Delete a user"""
    if connected_user_type == "gestion":
        user_id = get_valid_int(user_id)
        if not is_valid(user_id):
            return

        result = delete_user_controller(user_id)
        if isinstance(result, dict):
            click.echo(f"Erreur: {result['error']}")
        else:
            click.echo(f"User {result.name} deleted successfully.")
    else:
        lackRightError()
        return


@click.command()
@click.argument("email")
@click.argument("password")
def login(email, password):
    """Authenticate user and return a token"""

    email = get_valid_email(email)
    password = get_valid_password(password)

    # Vérifie chaque champ
    if not is_valid(email) or not is_valid(password):
        return

    result = authenticate_user(email=email, password=password)
    if result:
        click.echo(f"Login successful.")
    else:
        click.echo("Login fails.")  #


@click.command()
def logout():
    """Disconnect user"""
    try:
        os.remove(".token")
        click.echo("Utilisateur Déconnecté avec succès.")
    except FileNotFoundError:
        click.echo("Aucun utilisateur connecté.")


@click.command()
def me():
    """display the connected user"""
    if connected_user is not None:
        click.echo(f"--> Type: {connected_user_type}, Id: {connected_user_id}")
        return
    else:
        click.echo("Aucun utilisateur connecté.")


@click.command()
def list_clients():
    """Get all clients"""

    if connected_user_type in ("gestion", "commercial", "support"):
        result = get_all_clients_controller()

        if not is_valid(result):
            return
        else:
            click.echo(f"--- Clients List: ---")
            for client in result:
                click.echo(
                    f"[{client.id}] - {client.name} - {client.email} - Company: {client.company_name} - Contact: {client.user_contact_id}")
    else:
        lackRightError()
        return


@click.command()
@click.argument("client_id", type=int)  # type is used to specify the type (generate automatically an error)
def get_client(client_id):
    """Get a user"""

    if connected_user_type in ("gestion", "commercial", "support"):
        result = get_client_controller(client_id)

        if not is_valid(result):
            return
        else:
            client = result
            click.echo(f"Name: {client.name}, Email: {client.email}, Phone: {client.phone_number}, "
                       f"Company: {client.company_name}, Contact: {client.user_contact_id}, Info: {client.information}")
    else:
        lackRightError()
        return


@click.command()
@click.argument("name")
@click.argument("email")
@click.argument("phone_number")
@click.argument("company_name")
@click.argument("information")
def create_client(name, email, phone_number, company_name, information):
    """Create a new client"""

    if connected_user_type == "commercial" and connected_user_id is not None:
        name = get_valid_name(name)
        email = get_valid_email(email)
        phone_number = get_valid_phone_number(phone_number)
        company_name = get_valid_string(company_name)
        user_contact_id = connected_user_id  # give the connected user id
        information = get_valid_string(information)

        print(
            f"Name: {name}, Email: {email}, Phone: {phone_number}, Company: {company_name}, Contact: {user_contact_id}, Info: {information}")

        # Vérifie chaque champ
        if (not is_valid(name)
                or not is_valid(email)
                or not is_valid(phone_number)
                or not is_valid(company_name)
                or not is_valid(information)):
            return

        result = create_client_controller(name=name, email=email, phone_number=phone_number,
                                          company_name=company_name, user_contact_id=user_contact_id,
                                          information=information)
        if isinstance(result, dict):
            click.echo(f"Erreur: {result['error']}")
        else:
            click.echo(f"Client {result.name} created successfully.")
    else:
        lackRightError()
        return


@click.command()
@click.argument("client_id", type=int)  # type is used to specify the type (generate automatically an error)
@click.option("--name", help="New name")  # Optional arguments, help is the description for --help
@click.option("--email", help="New email")
@click.option("--phone_number", help="New phone number")
@click.option("--company_name", help="New company name")
@click.option("--information", help="New information")
def update_client(client_id, name, email, phone_number, company_name, information):
    """Update a client's details"""

    if connected_user_type == "commercial" and connected_user_id == get_client_controller(client_id).user_contact_id:
        client_id = get_valid_int(client_id)
        if name:
            name = get_valid_name(name)
        if email:
            email = get_valid_email(email)
        if phone_number:
            phone_number = get_valid_phone_number(phone_number)
        if company_name:
            company_name = get_valid_string(company_name)
        if information:
            information = get_valid_string(information)

        # Vérifie chaque champ
        if (not is_valid(client_id)
                or not is_valid(name)
                or not is_valid(email)
                or not is_valid(phone_number)
                or not is_valid(company_name)
                or not is_valid(information)):
            return

        result = update_client_controller(client_id=client_id, name=name, email=email, phone_number=phone_number,
                                          company_name=company_name, information=information)
        if isinstance(result, dict):
            click.echo(f"Erreur: {result['error']}")
        else:
            click.echo(f"Client {result.name} updated successfully.")
    else:
        lackRightError()
        return


@click.command()
@click.argument("client_id", type=int)
def delete_client(client_id):
    """Delete a client"""
    if connected_user_type == "commercial" and connected_user_id == get_client_controller(client_id).user_contact_id:
        client_id = get_valid_int(client_id)
        if not is_valid(client_id):
            return

        result = delete_client_controller(client_id)
        if isinstance(result, dict):
            click.echo(f"Erreur: {result['error']}")
        else:
            click.echo(f"Client {result.name} deleted successfully.")
    else:
        lackRightError()
        return


@click.command()
@click.option("--not_signed", is_flag=True, help="Filter evenements not signed")
@click.option("--signed", is_flag=True, help="Filter evenements signed")
@click.option("--not_paid", is_flag=True, help="Filter evenements with no support assigned")
@click.option("--paid", is_flag=True, help="Filter evenements with no support assigned")
def list_contrats(not_signed, signed, not_paid, paid):
    """Get all contrats"""

    if connected_user_type in ("gestion", "commercial", "support"):
        if not_signed or signed or not_paid or paid:
            result = get_all_contrats_controller(not_signed, signed, not_paid, paid)
        else:
            result = get_all_contrats_controller()

        if not is_valid(result):
            return
        else:
            click.echo(f"--- Contrats List: ---")
            for contrat in result:
                click.echo(
                    f"[{contrat.id}] - Client: {contrat.client_id} - Total: {contrat.total_amount} - "
                    f"Outstanding: {contrat.outstanding_amount} - Signed: {contrat.signed}")
    else:
        lackRightError()
        return


@click.command()
@click.argument("contrat_id", type=int)  # type is used to specify the type (generate automatically an error)
def get_contrat(contrat_id):
    """Get a contrat"""

    if connected_user_type in ("gestion", "commercial", "support"):
        result = get_contrat_controller(contrat_id)

        if not is_valid(result):
            return
        else:
            contrat = result
            click.echo(
                f"[{contrat.id}] - Client: {contrat.client_id} - Commercial: {contrat.commercial_id} "
                f"- Total: {contrat.total_amount} - Outstanding: {contrat.outstanding_amount} "
                f"- Signed: {contrat.signed}")
    else:
        lackRightError()
        return


@click.command()
@click.argument("client_id")
@click.argument("total_amount")
@click.argument("outstanding_amount")
@click.argument("signed")
def create_contrat(client_id, total_amount, outstanding_amount, signed):
    """Create a new contrat"""

    if connected_user_type == "gestion" and connected_user_id is not None:
        client_id = get_valid_int(client_id)
        commercial_id = connected_user_id
        total_amount = get_valid_amount(total_amount)
        outstanding_amount = get_valid_amount(outstanding_amount)
        signed = get_valid_boolean(signed)

        print(f"Client: {client_id}, Commercial: {commercial_id}, Total: {total_amount},"
              f" Outstanding: {outstanding_amount}, Signed: {signed}")

        # Vérifie chaque champ
        if (not is_valid(client_id)
                or not is_valid(commercial_id)
                or not is_valid(total_amount)
                or not is_valid(outstanding_amount)
                or not is_valid(signed)):
            return

        result = create_contrat_controller(client_id=client_id, commercial_id=commercial_id,
                                           total_amount=total_amount, outstanding_amount=outstanding_amount,
                                           signed=signed)
        if isinstance(result, dict):
            click.echo(f"Erreur: {result['error']}")
        else:
            click.echo(f"Contrat ID number: {result.id}  created successfully.")
    else:
        lackRightError()
        return


@click.command()
@click.argument("contrat_id", type=int)
@click.option("--client_id", help="New client id")
@click.option("--total_amount", help="New total amount")
@click.option("--outstanding_amount", help="New outstanding amount")
@click.option("--signed", help="New signed")
def update_contrat(contrat_id, client_id, total_amount, outstanding_amount, signed):
    """Update a contrat's details"""

    if (connected_user_type == "gestion" or
            connected_user_type == "commercial" and connected_user_id == get_contrat_controller(
                contrat_id).commercial_id):
        contrat_id = get_valid_int(contrat_id)
        if client_id:
            client_id = get_valid_int(client_id)
        if total_amount:
            total_amount = get_valid_amount(total_amount)
        if outstanding_amount:
            outstanding_amount = get_valid_amount(outstanding_amount)
        if signed:
            signed = get_valid_boolean(signed)

        # Vérifie chaque champ
        if (not is_valid(contrat_id)
                or not is_valid(client_id)
                or not is_valid(total_amount)
                or not is_valid(outstanding_amount)
                or not is_valid(signed)):
            return

        result = update_contrat_controller(contrat_id=contrat_id, client_id=client_id, total_amount=total_amount,
                                           outstanding_amount=outstanding_amount, signed=signed)
        if isinstance(result, dict):
            click.echo(f"Erreur: {result['error']}")
        else:
            click.echo(f"Contrat ID number: {result.id} updated successfully.")
    else:
        lackRightError()
        return


@click.command()
@click.argument("contrat_id", type=int)
def delete_contrat(contrat_id):
    """Delete a contrat"""
    if (connected_user_type == "gestion" or
            connected_user_type == "commercial" and connected_user_id == get_contrat_controller(
                contrat_id).commercial_id):
        contrat_id = get_valid_int(contrat_id)
        if not is_valid(contrat_id):
            return

        result = delete_contrat_controller(contrat_id)
        if isinstance(result, dict):
            click.echo(f"Erreur: {result['error']}")
        else:
            click.echo(f"Contrat ID number: {result.id} deleted successfully.")
    else:
        lackRightError()
        return


@click.command()
@click.option("--no_support", is_flag=True, help="Filter evenements with no support assigned")
@click.option("--support", is_flag=True, help="Filter evenements with support assigned")
@click.option("--my_evenements", is_flag=True, help="Filter evenements with support assigned")
def list_evenements(no_support, support, my_evenements):
    """Get all evenements"""

    if connected_user_type in ("gestion", "commercial", "support"):
        if no_support or support:
            result = get_all_evenements_controller(no_support, support)
        elif my_evenements and connected_user_type == "support":
            result = get_all_evenements_controller(support_id=connected_user_id)
        else:
            result = get_all_evenements_controller()

        if not is_valid(result):
            return
        else:
            click.echo(f"--- Evenements List: ---")
            for evenement in result:
                click.echo(f"[{evenement.id}] Evenement: Contrat {evenement.contrat_id}, Client name: "
                           f"{evenement.client_name}, Client contact: {evenement.client_contact_id},"
                           f" Start date: {evenement.start_date}, End date: {evenement.end_date}, "
                           f"Support contact: {evenement.support_id}, "
                           f"Location: {evenement.location}, Expected: {evenement.expected}")
    else:
        lackRightError()
        return


@click.command()
@click.argument("evenement_id", type=int)  # type is used to specify the type (generate automatically an error)
def get_evenement(evenement_id):
    """Get a evenement"""

    if connected_user_type in ("gestion", "commercial", "support"):
        result = get_evenement_controller(evenement_id)

        if not is_valid(result):
            return
        else:
            evenement = result
            click.echo(f"[{evenement.id}] Evenement: Contrat{evenement.contrat_id}, Client name: "
                       f"{evenement.client_name}, Client contact: {evenement.client_contact_id},"
                       f" Start date: {evenement.start_date}, End date: {evenement.end_date}, "
                       f"Support contact: {evenement.support_id}, "
                       f"Location: {evenement.location}, Expected: {evenement.expected}, Note: {evenement.notes}")
    else:
        lackRightError()
        return


@click.command()
@click.argument("contrat_id")
@click.argument("client_name")
@click.argument("client_contact_id")
@click.option("--support_id", help="Add optional support name")
@click.argument("start_date")
@click.argument("end_date")
@click.argument("location")
@click.argument("expected")
@click.argument("notes")
def create_evenement(contrat_id, client_name, client_contact_id, support_id, start_date, end_date, location, expected,
                     notes):
    """Create a new evenement"""

    if connected_user_type == "commercial" and connected_user_id is not None:
        contrat_id = get_valid_int(contrat_id)

        if get_contrat_controller(contrat_id).signed:
            client_name = get_valid_string(client_name)
            client_contact_id = get_valid_int(client_contact_id)
            start_date = get_valid_string(start_date)
            end_date = get_valid_string(end_date)
            if support_id:
                support_id = get_valid_string(support_id)
            location = get_valid_string(location)
            expected = get_valid_int(expected)
            notes = get_valid_string(notes)

            print(f"Evenement: Contrat: {contrat_id}, Client name: {client_name}, Client contact: {client_contact_id},"
                  f" Start date: {start_date}, End date: {end_date}, Support contact: {support_id}, Location: {location},"
                  f" Expected: {expected}")

            # Vérifie chaque champ
            if (not is_valid(contrat_id)
                    or not is_valid(client_name)
                    or not is_valid(client_contact_id)
                    or not is_valid(support_id)
                    or not is_valid(start_date)
                    or not is_valid(end_date)
                    or not is_valid(location)
                    or not is_valid(expected)
                    or not is_valid(notes)):
                return

            result = create_evenement_controller(contrat_id=contrat_id, client_name=client_name,
                                                 client_contact_id=client_contact_id, support_id=support_id,
                                                 start_date=start_date, end_date=end_date,
                                                 location=location, expected=expected, notes=notes)
            if isinstance(result, dict):
                click.echo(f"Erreur: {result['error']}")
            else:
                click.echo(f"Evenement ID number: {result.id}  created successfully.")
        else:
            click.echo("Error: Le Client n'a pas encore signé le contrat")
            return
    else:
        lackRightError()
        return


@click.command()
@click.argument("evenement_id", type=int)
@click.option("--client_name", help="New client_name")
@click.option("--client_contact_id", help="New client_contact_id")
@click.option("--support_id", help="New support_id")
@click.option("--start_date", help="New start_date")
@click.option("--end_date", help="New end_date")
@click.option("--location", help="New location")
@click.option("--expected", help="New expected")
@click.option("--notes", help="New notes")
def update_evenement(evenement_id, client_name, client_contact_id, support_id, start_date, end_date, location,
                     expected, notes):
    """Update a evenement's details"""

    if connected_user_type in ("gestion", "support"):
        if int(connected_user_id) != int(get_evenement_controller(evenement_id).support_id):
            lackRightError()
            return

        evenement_id = get_valid_int(evenement_id)
        if client_name:
            client_name = get_valid_string(client_name)
        if client_contact_id:
            client_contact_id = get_valid_int(client_contact_id)
        if support_id:
            support_id = get_valid_int(support_id)
        if start_date:
            start_date = get_valid_string(start_date)
        if end_date:
            end_date = get_valid_string(end_date)
        if location:
            location = get_valid_string(location)
        if expected:
            expected = get_valid_int(expected)
        if notes:
            notes = get_valid_string(notes)

        # Vérifie chaque champ
        if (not is_valid(evenement_id)
                or not is_valid(client_name)
                or not is_valid(client_contact_id)
                or not is_valid(support_id)
                or not is_valid(start_date)
                or not is_valid(end_date)
                or not is_valid(location)
                or not is_valid(expected)
                or not is_valid(notes)):
            return

        result = update_evenement_controller(evenement_id=evenement_id, client_name=client_name,
                                             client_contact_id=client_contact_id,
                                             support_id=support_id, start_date=start_date, end_date=end_date,
                                             location=location, expected=expected, notes=notes)
        if isinstance(result, dict):
            click.echo(f"Erreur: {result['error']}")
        else:
            click.echo(f"Evenement ID number: {result.id} updated successfully.")
    else:
        lackRightError()
        return


@click.command()
@click.argument("evenement_id", type=int)
def delete_evenement(evenement_id):
    """Delete a evenement"""

    if connected_user_type in ("gestion", "support"):
        event = get_evenement_controller(evenement_id)

        if (connected_user_type == "support"
                and (event.support_id is None
                     or int(connected_user_id) != int(event.support_id))):
            lackRightError()
            return

        contrat_id = get_valid_int(evenement_id)
        if not is_valid(contrat_id):
            return

        result = delete_evenement_controller(contrat_id)
        if isinstance(result, dict):
            click.echo(f"Erreur: {result['error']}")
        else:
            click.echo(f"Evenement ID number: {result.id} deleted successfully.")
    else:
        lackRightError()
        return


cli.add_command(login)
cli.add_command(logout)
cli.add_command(me)

cli.add_command(list_users)  # Access : All
cli.add_command(get_user)  # Access : All
cli.add_command(create_user)  # Access : Gestion
cli.add_command(update_user)  # Access : Gestion
cli.add_command(delete_user)  # Access : Gestion

cli.add_command(list_clients)  # Access : All
cli.add_command(get_client)  # Access : All
cli.add_command(create_client)  # Access : Commercial (client sera automatiquement associé)
cli.add_command(update_client)  # Access : Commercial (+ client dont il est responsable)
cli.add_command(delete_client)  # Access : Commercial (+ client dont il est responsable)

cli.add_command(list_contrats)  # Access : All
cli.add_command(get_contrat)  # Access : All
cli.add_command(create_contrat)  # Access : Gestion
cli.add_command(update_contrat)  # Access : Gestion / Commercial (contrats des clients dont il est responsable)
cli.add_command(delete_contrat)  # ?? Access : Gestion / Commercial (contrats des clients dont ils sont responsables)

cli.add_command(list_evenements)  # Access : All
cli.add_command(get_evenement)  # Access : All
cli.add_command(create_evenement)  # Access : Commercial
cli.add_command(update_evenement)  # Access : Gestion / Support
cli.add_command(delete_evenement)  # ?? Access : Gestion / Support


def is_valid(value):
    """Check if the value is valid."""
    if isinstance(value, dict):
        click.echo(f"Erreur: {value['error']}")
        return False
    return True


def lackRightError():
    """Return a lack of right error message."""
    return click.echo("Error: vous n'avez pas les droits pour effectuer cette action.")


sentry_sdk.init(
    dsn=DSN,
    send_default_pii=True,
)

if __name__ == "__main__":
    # Uncomment the following line and run main to test the sentry error handling
    # division_by_zero = 1 / 0
    cli()
