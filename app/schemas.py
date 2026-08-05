from pydantic import BaseModel, EmailStr
from typing import Optional


# -------------------------------
# Complaint Schemas
# -------------------------------

class ComplaintCreate(BaseModel):
    customer_name: str
    email: EmailStr
    product: str
    complaint: str


class ComplaintUpdate(BaseModel):
    customer_name: str
    email: EmailStr
    product: str
    complaint: str


class ComplaintResponse(BaseModel):
    id: int
    customer_name: str
    email: str
    product: str
    complaint: str

    complaint_summary: Optional[str] = None
    category: Optional[str] = None
    severity: Optional[str] = None
    root_cause: Optional[str] = None
    capa: Optional[str] = None
    suggested_response: Optional[str] = None

    status: str

    class Config:
        from_attributes = True


# -------------------------------
# Status Update
# -------------------------------

class StatusUpdate(BaseModel):
    status: str


# -------------------------------
# Authentication Schemas
# -------------------------------

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str