# AI Planner

AI Planner is a Streamlit-based application designed to automate business planning workflows using AI and Google Sheets integration.

It enables users to generate, refine, and structure plans dynamically while interacting with external data sources.

---

## 🚀 Live Demo

https://revaiplanner.streamlit.app
(It will ask for login, causing you to not be able to see the app. However, it is indeed deployed, and you can configure it according to your own needs!)

---

## ✨ Features

* AI-powered planning and refinement
* Google Sheets integration
* Authentication system
* Configurable prompts and workflows
* PDF export support

---

## 🛠 Tech Stack

* Python
* Streamlit
* Google Sheets API (`gspread`)
* LLM APIs (Ollama / others)

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/RevantProgrammer/AIPlanner
cd AIPlanner
```

### 2. Create virtual environment & install dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Create `.env` file

Use `.env.example` as a template.

---

### 4. Configure environment variables

#### Required:

* `OLLAMA_API_KEY`
* `WORKBOOK_ID`
* `SHEET_NAME`
* `SCOPES`

#### Google Credentials:

Either:

* Provide `GOOGLE_CREDENTIALS` as a JSON string
  **OR**
* Provide `CREDENTIALS_FILE` path

---

### 5. Configure users (IMPORTANT)

Authentication is environment-based.

#### Option A — Local (`.env`)

```env
USERS='{
  "ADMIN": {
    "name": "Your Name",
    "password": "your_hashed_password"
  }
}'
```

#### Option B — Streamlit Cloud (`secrets.toml`)

```toml
[AUTHORISATION.USERS]
ADMIN = { name = "Your Name", password = "your_hashed_password" }
```

---

### 6. Run the app

```bash
streamlit run app.py
```

---

## 🔐 Authentication Notes

* User credentials are not stored in the repository
* Local development uses `.env`
* Deployment uses `secrets.toml`
* Future versions will support OAuth-based authentication

---

## 📦 Deployment

The app is designed to run on:

* Streamlit Cloud
* Google Cloud Run (planned)

Environment variables and secrets are automatically resolved across environments.

---

## 🧠 Architecture Overview

* **UI Layer**: Streamlit interface
* **Service Layer**: PlannerApplicationService (business logic abstraction)
* **Model Layer**: Handles AI, validation, and data operations

---

## ⚠️ Known Limitations

* Static user authentication (not scalable)
* No database integration yet
* Limited logging and monitoring

---

## 🔮 Future Improvements

* OAuth (Google / Microsoft) authentication
* Database-backed user management
* Full Cloud Run deployment
* Enhanced logging and observability

---

## 👤 Author

Developed by Revant Pandey to help increase productivity by automating time taking tasks and help increase the adoption of AI!