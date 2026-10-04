from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class LeadIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    is_community: bool = False
    comments: str = Field(default="", max_length=5000)


class LeadClassification(BaseModel):
    department: Literal["sales", "support", "partnerships", "other"]
    urgency: Literal["low", "medium", "high"]
    summary: str = Field(description="One or two sentences about what the lead wants")