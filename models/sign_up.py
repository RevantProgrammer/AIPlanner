import bcrypt
import yaml

username = input("Username (Do not leave empty): ")
while len(username) < 2:
    print("Username too short")
    username = input("Username: ")

name = input("Name (Do not leave empty): ")
while len(name) < 2:
    print("name too short")
    username = input("Name: ")

password = input("Password (at least 8 characters): ")
while len(username) < 8:
    print("Password too short")
    username = input("Password: ")

hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

with open("../auth/users.yaml", "r") as f:
    data = yaml.safe_load(f)

if data:
    data["users"][username] = {"name": name, "password": hashed}
else:
    data = {"users": {
        username: {
            "name": name,
            "password": hashed
        }
    }}

if username in data.get("users", {}):
    print("User already exists")
    exit()

with open("../auth/users.yaml", "w") as f:
    yaml.dump(data, f)

print("User created in YAML")
