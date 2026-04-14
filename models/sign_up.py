import bcrypt
import yaml

username = input("Username: ")
name = input("Name: ")
password = input("Password: ")

hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

with open("../auth/users.yaml", "r") as f:
    data = yaml.safe_load(f)

data["users"][username] = {"name": name, "password": hashed}

with open("../auth/users.yaml", "w") as f:
    yaml.dump(data, f)

print("User created in YAML")
