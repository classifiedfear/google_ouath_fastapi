import os
import json

from typing import Any, Dict


def init_blacklist_file():
    with open("fake_db/last_user_info.json", "w", encoding="utf-8") as file_1, open(
        "fake_db/blacklist_db.txt", "a", encoding="utf-8"
    ) as file_2:
        json.dump({}, file_1, indent=4)
    return True


def add_blacklist_token(token):
    with open("fake_db/blacklist_db.txt", "a", encoding="utf-8") as file:
        file.write(f"{token}")
    return True


def is_token_blacklisted(token):
    with open("fake_db/blacklist_db.txt", encoding="utf-8") as file:
        content = file.read()
        array = content[:-1].split(",")
        for value in array:
            if value == token:
                return True

    return False


def add_user_info(user_info: Dict[str, Any]):
    with open("fake_db/last_user_info.json", "w", encoding="utf-8") as file:
        json.dump(user_info, file, indent=4)

def remove_user_info():
    with open("fake_db/last_user_info.json", "w", encoding="utf-8") as file:
        json.dump({}, file, indent=4)


def get_last_user_info() -> Dict[str, Any] | None:
    with open("fake_db/last_user_info.json", "r", encoding="utf-8") as file:
        json_data = json.load(file)
        if len(json_data) == 0:
            return None
    return json_data
