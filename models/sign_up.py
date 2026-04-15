import bcrypt
import yaml

username = input("Username (Do not leave empty): ")
while len(username) < 2:
    print("Username too short")
    username = input("Username: ")

name = input("Name (Do not leave empty): ")
while len(name) < 2:
    print("Name too short")
    name = input("Name: ")

password = input("Password (at least 8 characters): ")
while len(password) < 8:
    print("Password too short")
    password = input("Password: ")

hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

with open("../auth/users.yaml", "r") as f:
    data = yaml.safe_load(f)

if data is None:
    data = {"users": {}}
if username in data.get("users", {}):
    print("User already exists")
    exit()


data["users"][username] = {"name": name, "password": hashed}

with open("../auth/users.yaml", "w") as f:
    yaml.dump(data, f)

print("User created in YAML")
