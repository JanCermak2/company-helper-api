# Company Helper API (Internal Tools API)

Minimalist internal tools API built with FastAPI + SQLAlchemy (SQLite).

## Features
- Ticket CRUD (`/api/v1/tickets`)
- API key auth via `X-API-Key`
- Filtering (`status`, `q`, `created_from`, `created_to`)
- Reporting (`/api/v1/reports/summary`)
- Logging + consistent error responses

## Tech
- Python 3.11+
- FastAPI, Uvicorn
- SQLAlchemy 2.0 (sync)
- SQLite (`app.db` in project root)

## Setup (Windows PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
