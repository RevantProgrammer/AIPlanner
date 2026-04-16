import os
from typing import Any
from dotenv import load_dotenv
import json
import streamlit as st

load_dotenv()


def _get_secret(key: str, section=None, default=None) -> Any:
    # Streamlit Cloud
    try:
        if section:
            val = st.secrets[section].get(key)
        else:
            val = st.secrets.get(key)

        if val is not None and val != "":
            return val
    except Exception:
        pass

    # Local or Google Cloud
    val = os.getenv(key)
    if val is not None and val != "":
        return val

    return default


def _get_google_credentials() -> dict:
    # Streamlit Cloud
    try:
        creds = st.secrets["GOOGLE_CREDENTIALS"]
        return creds
    except Exception:
        pass

    # Google Cloud
    env = os.getenv("GOOGLE_CREDENTIALS")
    if env:
        return json.loads(env)

    # Local
    file_path = os.getenv("CREDENTIALS_FILE")
    if file_path:
        with open(file_path) as f:
            return json.load(f)

    raise ValueError("No Google credentials found")


def get_settings() -> dict:
    return {
        "OLLAMA_API_KEY": _get_secret("OLLAMA_API_KEY", section="API_KEYS"),
        "SCOPES": json.loads(_get_secret("SCOPES", section="SHEETS_DETAILS", default="[]")),
        "WORKBOOK_ID": _get_secret("WORKBOOK_ID", section="SHEETS_DETAILS"),
        "SHEET_NAME": _get_secret("SHEET_NAME", section="SHEETS_DETAILS"),
        "GOOGLE_CREDENTIALS": _get_google_credentials(),
        "GENERATE_PROMPT_FILE": _get_secret("GENERATE_PROMPT_FILE", section="PROMPTS"),
        "REFINE_PROMPT_FILE": _get_secret("REFINE_PROMPT_FILE", section="PROMPTS"),
        "STRUCTURE_PROMPT_FILE": _get_secret("STRUCTURE_PROMPT_FILE", section="PROMPTS"),
        "USER_DATA": _get_secret("USERS", "AUTHORISATION"),
    }
