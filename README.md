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

## Deployment

Deploy to Railway - it will auto-deploy from this GitHub repo.
