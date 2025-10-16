# Job Application AI - Backend API

FastAPI backend service for the AI Job Application Assistant.

## Setup

```bash
# Install dependencies
poetry install

# Install Playwright browsers
poetry run playwright install

# Run development server
poetry run uvicorn app.main:app --reload

# Run tests
poetry run pytest

# Format code
poetry run black .
poetry run isort .
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
