import os
from datetime import UTC, datetime

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from pymongo import AsyncMongoClient

load_dotenv()
client = AsyncMongoClient(os.environ["MONGODB_URI"])
db = client["elevatebiz"]
leads = db["leads"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://elevatebiz.ai"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class LeadIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    is_community: bool = False
    comments: str = Field(default="", max_length=5000)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/leads", status_code=201)
async def create_lead(lead: LeadIn):
    doc = lead.model_dump()
    doc["created_at"] = datetime.now(UTC)
    result = await leads.insert_one(doc)
    return {"id": str(result.inserted_id)}
