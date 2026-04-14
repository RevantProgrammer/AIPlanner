import bcrypt
import yaml


class Authenticator:
    def __init__(self, auth_file):
        self.auth_file = auth_file

    def __load_users(self):
        with open(self.auth_file, "r") as f:
            return yaml.safe_load(f)["users"]

    def check_login(self, username, password):
        users = self.__load_users()
        if username not in users:
            return None, False
        stored_hash = users[username]["password"].encode()
        return users[username]["name"], bcrypt.checkpw(password.encode(), stored_hash)
