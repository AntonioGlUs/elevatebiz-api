from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field
import os
from dotenv import load_dotenv
from pymongo import AsyncMongoClient

load_dotenv()
client = AsyncMongoClient(os.environ["MONGODB_URI"])
db = client["elevatebiz"]
leads = db["leads"]

app = FastAPI()

class LeadIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    is_community: bool = False
    comments: str = Field(default="", max_length=5000)

@app.get("/health")
def health():
    return{"status": "ok"}

@app.post("/api/leads", status_code=201)
async def create_lead(lead: LeadIn):
    result = await leads.insert_one(lead.model_dump())
    return {"id": str(result.inserted_id)}