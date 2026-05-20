# Riftbound Stats V2 - API

FastAPI backend for Riftbound Stats V2.

## Setup

1. Install dependencies:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. Run the API:
```bash
uvicorn app.main:app --reload --port 8001
```

4. Visit the docs:
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## Project Structure

```
app/
├── main.py              # FastAPI app
├── config.py            # Settings
├── database.py          # DB connection
├── models/              # SQLAlchemy models
├── schemas/             # Pydantic schemas
├── api/                 # API routes
└── utils/               # Utilities
```

## API Endpoints

### Cards
- `GET /api/v2/cards` - List/search cards
- `GET /api/v2/cards/{id}` - Get card details
- `GET /api/v2/sets` - List all sets

### Decks
- `GET /api/v2/decks` - List decks
- `GET /api/v2/decks/{id}` - Get deck details
- `POST /api/v2/decks` - Create deck
- `POST /api/v2/decks/{id}/validate` - Validate deck

### Events
- `GET /api/v2/events` - List events
- `GET /api/v2/events/{id}` - Get event details

### Formats
- `GET /api/v2/formats` - List formats
- `GET /api/v2/formats/{id}` - Get format details

## Deployment

Deploy to Railway:
```bash
git push origin main
# Railway will auto-deploy
```

## Testing

```bash
pytest tests/
```
