import bcrypt
import json
import os
from dotenv import load_dotenv

load_dotenv()
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

existing = os.getenv("USERS")

if existing:
    users = json.loads(existing)
else:
    users = {}

users[username] = {
    "name": name,
    "password": hashed
}

print("Add this to your .env:\n")
print("\n⚠️ NOTE: This should overwrite USERS in your .env\n")
print(f"USERS='{json.dumps(users)}'")
