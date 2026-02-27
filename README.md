# Paragraph Analytics API (Django + DRF)

A containerized Django REST project implementing:
- Custom user registration/login
- Paragraph ingestion with whitespace tokenization
- User-level word frequency maintenance
- Top-10 paragraph search by word occurrence
- Async and scheduled processing with Celery + Redis

## Tech Stack
- Django + Django REST Framework
- PostgreSQL (relational DB)
- Celery (task queue)
- Celery Beat (task scheduler)
- Redis (message broker + result backend)
- Docker + Docker Compose

## Project Structure
- `users/`: custom user model and auth APIs
- `paragraphs/`: paragraph ingestion, tokenization, search, frequency tasks
- `config/`: project settings, URL config, celery config

## Setup (Docker)
1. Copy env file:
   ```bash
   cp .env.example .env
   ```
2. Build and run services:
   ```bash
   docker compose up --build
   ```
3. Create superuser (optional):
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

Services started:
- API: `http://localhost:8000`
- Swagger docs: `http://localhost:8000/swagger/`
- ReDoc docs: `http://localhost:8000/redoc/`
- Admin: `http://localhost:8000/admin/`

## Setup (without Docker)
> Ensure PostgreSQL and Redis are available and env vars are configured.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

In separate terminals:
```bash
celery -A config worker -l info
celery -A config beat -l info
```

## API Documentation
### 1) Register
`POST /api/auth/register/`

Request:
```json
{
  "name": "Ram Sharma",
  "email": "ram@example.com",
  "date_of_birth": "1998-05-10",
  "password": "StrongPass123"
}
```

### 2) Login
`POST /api/auth/login/`

Request:
```json
{
  "email": "ram@example.com",
  "password": "StrongPass123"
}
```

Response contains JWT `access` and `refresh` tokens.

### 3) Refresh token
`POST /api/auth/token/refresh/`

### 4) Ingest paragraphs
`POST /api/paragraphs/ingest/`
(Requires Bearer access token)

Request:
```json
{
  "text": "First paragraph line.\n\nSecond paragraph line with words words.\n\nThird paragraph."
}
```

Processing behavior:
- Splits paragraphs by `\n\n`
- Tokenizes words by whitespace
- Normalizes case to lowercase
- Updates user-level word frequencies

### 5) Search top 10 paragraphs for a word
`GET /api/paragraphs/search/?word=words`
(Requires Bearer access token)

Response:
```json
[
  {
    "paragraph_id": 2,
    "sequence": 2,
    "occurrences": 2,
    "content": "Second paragraph line with words words."
  }
]
```

## Scheduled Task
A daily Celery Beat schedule runs:
- `paragraphs.tasks.recalculate_all_users_word_frequencies` at 00:00 UTC.

## Notes
- The environment used for this delivery may block outbound network access, so dependency installation and runtime checks may need to be run in your local/CI environment.
- The code is ready for private GitHub hosting; push using:
  ```bash
  git remote add origin <private-repo-url>
  git push -u origin <branch>
  ```
