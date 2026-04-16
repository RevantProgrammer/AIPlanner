import bcrypt
import yaml


class Authenticator:
    def __init__(self, user_data: dict) -> None:
        self.user_data = user_data

    def check_login(self, username: str|None, password: str|None) -> tuple[str, bool]:
        if username not in self.user_data:
            return "", False
        stored_hash = self.user_data[username]["password"].encode()
        return self.user_data[username]["name"], bcrypt.checkpw(password.encode(), stored_hash)
