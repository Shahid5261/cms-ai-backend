from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import UserRegister, UserLogin, Token
from app.crud import register_user, login_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    user: UserRegister,
    db: Session = Depends(get_db),
):
    created = register_user(db, user)

    if created is None:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    return {
        "message": "Registration successful"
    }


@router.post("/login", response_model=Token)
def login(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    token = login_user(db, user)

    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return token