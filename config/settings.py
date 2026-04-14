import os
from dotenv import load_dotenv
import json


def get_settings():
    load_dotenv()
    return {
        "OLLAMA_API_KEY": os.getenv("OLLAMA_API_KEY"),
        "SCOPES": json.loads(os.getenv("SCOPES")),
        "WORKBOOK_ID": os.getenv("WORKBOOK_ID"),
        "SHEET_NAME": os.getenv("SHEET_NAME"),
        "CREDENTIALS_FILE": os.getenv("CREDENTIALS_FILE"),
        "GENERATE_PROMPT_FILE": os.getenv("GENERATE_PROMPT_FILE"),
        "REFINE_PROMPT_FILE": os.getenv("REFINE_PROMPT_FILE"),
        "STRUCTURE_PROMPT_FILE": os.getenv("STRUCTURE_PROMPT_FILE"),
        "LOGIN_USERS_FILE": os.getenv("LOGIN_USERS_FILE")
    }
