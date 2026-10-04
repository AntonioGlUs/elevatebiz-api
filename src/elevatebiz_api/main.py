import logging
from datetime import UTC, datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.exceptions import OutputParserException
from openai import OpenAIError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from .classifier import classify_lead
from .db import leads
from .models import LeadIn

logger = logging.getLogger(__name__)

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://elevatebiz.ai",
        "https://www.elevatebiz.ai",
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/leads", status_code=201)
@limiter.limit("3/day")
async def create_lead(request: Request, lead: LeadIn):
    doc = lead.model_dump()
    doc["created_at"] = datetime.now(UTC)

    try:
        result_ai = await classify_lead(lead)
        doc.update(result_ai.model_dump())
    except (OpenAIError, OutputParserException):
        logger.exception("AI classification failed")
        doc["department"] = "unassigned"

    result = await leads.insert_one(doc)
    return {"id": str(result.inserted_id), "department": doc["department"]}