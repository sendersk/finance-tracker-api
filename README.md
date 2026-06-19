# Finance Tracker API

REST API for personal finance management built with FastAPI and SQLAlchemy.

## Features

- Create transactions
- Delete transactions
- List transactions
- Filter by category
- Filter by transaction type
- Balance calculation
- Monthly summary
- CSV export
- Database migrations with Alembic
- Docker support
- Automated tests

## Tech Stack

- Python 3.13+
- FastAPI
- SQLAlchemy 2.0
- SQLite
- Alembic
- Pytest
- Docker

## Project Structure

```text
app/
├── core/
├── db/
├── models/
├── repositories/
├── routes/
├── schemas/
├── services/
└── main.py

tests/
├── conftest.py
├── test_summary.py
└── test_transactions.py
```

## Installation

```bash
git clone https://github.com/sendersk/finance-tracker-api.git

cd finance-tracker-api

python -m venv .venv

source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create:

```text
.env
```

Example:

```env
APP_NAME=Finance Tracker API
DATABASE_URL=sqlite:///finance.db
DEBUG=True
```

## Database Migrations

Apply migrations:

```bash
alembic upgrade head
```

Create migration:

```bash
alembic revision --autogenerate -m "message"
```

Rollback:

```bash
alembic downgrade -1
```

## Run Application

```bash
python run.py
```

Swagger:

```text
http://localhost:8000/docs
```

## Docker

```bash
docker compose up --build
```

## Testing

```bash
pytest -v
```