from ..backend.utils import (
    get_valid_name,
    get_valid_string,
    get_valid_email,
    get_valid_user_type,
    get_valid_password,
    get_valid_int,
    get_valid_phone_number,
    get_valid_amount,
    get_valid_boolean,
    get_valid_written_date,
)


def test_get_valid_name():
    assert get_valid_name("Jean Dupont") == "Jean Dupont"
    assert "error" in get_valid_name("")
    assert "error" in get_valid_name("Jean123")


def test_get_valid_string():
    assert get_valid_string("Some string - OK 123") == "Some string - OK 123"
    assert "error" in get_valid_string("")
    assert "error" in get_valid_string("Invalid@Value!")


def test_get_valid_email():
    assert get_valid_email("Test@Mail.com") == "test@mail.com"
    assert "error" in get_valid_email("")
    assert "error" in get_valid_email("invalid@com")


def test_get_valid_user_type():
    assert get_valid_user_type("commercial") == "commercial"
    assert get_valid_user_type("support") == "support"
    assert "error" in get_valid_user_type("")
    assert "error" in get_valid_user_type("invalid")


def test_get_valid_password():
    assert get_valid_password("  pass123 ") == "pass123"
    assert "error" in get_valid_password("")


def test_get_valid_int():
    assert get_valid_int("42") == 42
    assert get_valid_int(7) == 7
    assert "error" in get_valid_int("")
    assert "error" in get_valid_int("abc")
    assert "error" in get_valid_int(0)
    assert "error" in get_valid_int(-10)


def test_get_valid_phone_number():
    assert get_valid_phone_number("+33612345678") == "+33612345678"
    assert "error" in get_valid_phone_number("0612345678")
    assert "error" in get_valid_phone_number("")


def test_get_valid_amount():
    assert get_valid_amount("100.50") == 100.50
    assert get_valid_amount(0) == 0
    assert get_valid_amount(200) == 200
    assert "error" in get_valid_amount("")
    assert "error" in get_valid_amount("abc")
    assert "error" in get_valid_amount(-1)


def test_get_valid_boolean():
    assert get_valid_boolean("True") is True
    assert get_valid_boolean("false") is False
    assert "error" in get_valid_boolean("yes")


def test_get_valid_written_date():
    assert get_valid_written_date("6 mai 2025") == "6 mai 2025"
    assert get_valid_written_date("12 janvier 2023") == "12 janvier 2023"
    assert "error" in get_valid_written_date("2023-01-12")
    assert "error" in get_valid_written_date("")
