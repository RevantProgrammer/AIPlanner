import bcrypt
import yaml
import os

class Authenticator:
    def __init__(self, auth_file):
        os.chdir("..")
        self.auth_file = auth_file

    def __load_users(self):
        with open(self.auth_file, "r") as f:
            return yaml.safe_load(f)["users"]

    def check_login(self, username, password):
        users = self.__load_users()

        if username not in users:
            return False

        stored_hash = users[username]["password"].encode()

        return bcrypt.checkpw(password.encode(), stored_hash)
