## Flask MVP Demo — JWT Auth, PostgreSQL, and ElevenLabs TTS

This is a fully functional **Minimum Viable Product (MVP)** backend built with Flask to demonstrate my expertise as python developer.

---

##  Tech Stack

- **Flask** — Backend Framework
- **PostgreSQL** — I have used Supabase's free POSTGRESQL db
- **SQLAlchemy + Alembic** — ORM + Migrations
- **Flask-JWT-Extended** — Secure authentication via JWT
- **ElevenLabs API** — Real-time text-to-speech (TTS) integration
- **Postman-tested** — All routes tested and working

---

## 📚 Features

### ✅ User Auth
- Register a new user
- Login and get JWT token
- Role support (`user`, `admin`, etc.)

### ✅ Scenario Management
- Create new scenarios
- List your scenarios
- Add steps (text + TTS audio) to scenarios
- Retrieve scenario steps

### ✅ ElevenLabs Integration
- Each step’s text is sent to ElevenLabs API
- MP3 audio is generated and saved locally
- Returned as `audio_url` in API response

---


| File/Folder                 | Description                                                                                                                   |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `run.py`                    | Entry point of the app. It loads environment variables, creates the Flask app, and starts the server.                         |
| `app/__init__.py`           | Initializes the Flask app with configuration, database, JWT auth, and registers blueprints.                                   |
| `app/models.py`             | Defines database models: `User`, `Scenario`, and `ScenarioStep` using SQLAlchemy ORM.                                         |
| `app/routes/auth.py`        | Handles user registration and login APIs. Uses hashed passwords and returns JWT tokens.                                       |
| `app/routes/scenarios.py`   | CRUD APIs for scenario management and steps. Secured via JWT. Also integrates text-to-speech (TTS).                           |
| `app/services/tts.py`       | Connects to ElevenLabs API to convert text into speech and saves the audio file.                                              |                                          |
| `migrations/`               | Auto-generated database migration files via Flask-Migrate. Helps manage schema updates.                                       |
| `requirements.txt`          | Python dependencies needed to run the project.                                                                                |
| `.env`                      | Environment variables like DB credentials, JWT secret, and ElevenLabs API key. (This is excluded from Git using `.gitignore`) |
| `.gitignore`                | Ignores sensitive and non-essential files like `.env`, `__pycache__/`, and virtual environments.                              |


## Testing APIs
Use Postman to test endpoints. All JWT-protected routes require the Authorization header with the token received from login.
