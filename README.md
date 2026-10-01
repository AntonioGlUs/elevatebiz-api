# ElevateBiz API

REST API that receives contact form leads from the [ElevateBiz](https://elevatebiz.ai) website and stores them in MongoDB Atlas.

## Tech stack

- **Python 3.12** + **FastAPI**
- **MongoDB Atlas** (async PyMongo driver)
- **Pydantic** for request validation
- **uv** for dependency management

## Endpoints

| Method | Route        | Description                          |
|--------|--------------|--------------------------------------|
| GET    | `/health`    | Health check                         |
| POST   | `/api/leads` | Validates and stores a contact lead  |

## Getting started

1. Install dependencies:
   ```bash
   uv sync
   ```
2. Create a `.env` file in the project root:
   ```
   MONGODB_URI=your-mongodb-atlas-connection-string
   ```
3. Run the server:
   ```bash
   uv run uvicorn elevatebiz_api.main:app --reload
   ```
4. Open the interactive docs at http://localhost:8000/docs

## Roadmap

- [ ] Classify each lead with AI (department + urgency)
- [ ] Route leads to the right department
- [ ] Connect the website's contact form
- [ ] Deploy to a VPS
