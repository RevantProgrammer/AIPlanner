# CURRENT: Static auth via secrets / env
# FUTURE: Replace with Microsoft OAuth or Google Workspace SSO
# Do not extend this system beyond MVP use cases

# SECURITY NOTE: This is NOT production-grade authentication.
# Intended only for internal MVP access control.


import bcrypt


class Authenticator:
    def __init__(self, user_data: dict) -> None:
        self.user_data = user_data

    def check_login(self, username: str|None, password: str|None) -> tuple[str, bool]:
        if username not in self.user_data:
            return "", False
        stored_hash = self.user_data[username]["password"].encode()
        return self.user_data[username]["name"], bcrypt.checkpw(password.encode(), stored_hash)
