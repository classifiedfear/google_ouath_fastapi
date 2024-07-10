from typing import Any, Dict


from sub_apps.auth_app.exceptions import CREDENTIALS_EXCEPTION

FAKE_DB = {
    "igorek9960@gmail.com": {"name": "Ihor Annenko"},
    "ihor.annenko@gmail.com": {"name": "Ihor Annenko"},
}


def get_current_user_email(payload: Dict[str, Any]):
    email = payload.get("sub")
    if email is None:
        raise CREDENTIALS_EXCEPTION

    if valid_email_from_db(email):
        return email
    raise CREDENTIALS_EXCEPTION


def valid_email_from_db(email: str) -> bool:
    return email in FAKE_DB
