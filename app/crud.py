from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models import Complaint
from app.models_user import User
from app.schemas import ComplaintCreate, ComplaintUpdate
from app.services.ai_service import analyze_complaint
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
)


# ======================================================
# Complaint Functions
# ======================================================

def create_complaint(db: Session, complaint: ComplaintCreate):

    ai_result = analyze_complaint(complaint.complaint)

    db_complaint = Complaint(
        customer_name=complaint.customer_name,
        email=complaint.email,
        product=complaint.product,
        complaint=complaint.complaint,
        complaint_summary=ai_result.get("summary", ""),
        category=ai_result.get("category", ""),
        severity=ai_result.get("severity", ""),
        root_cause=ai_result.get("root_cause", ""),
        capa=ai_result.get("capa", ""),
        suggested_response=ai_result.get("suggested_response", ""),
        status="Pending",
    )

    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)

    return db_complaint


def get_all_complaints(
    db: Session,
    search: str = "",
    category: str = "",
    status: str = "",
):

    query = db.query(Complaint)

    if search:
        query = query.filter(
            or_(
                Complaint.customer_name.ilike(f"%{search}%"),
                Complaint.product.ilike(f"%{search}%"),
                Complaint.category.ilike(f"%{search}%"),
            )
        )

    if category:
        query = query.filter(Complaint.category == category)

    if status:
        query = query.filter(Complaint.status == status)

    return query.order_by(Complaint.id.desc()).all()


def update_complaint_status(
    db: Session,
    complaint_id: int,
    status: str,
):

    complaint = (
        db.query(Complaint)
        .filter(Complaint.id == complaint_id)
        .first()
    )

    if complaint is None:
        return None

    complaint.status = status

    db.commit()
    db.refresh(complaint)

    return complaint


def update_complaint(
    db: Session,
    complaint_id: int,
    data: ComplaintUpdate,
):

    complaint = (
        db.query(Complaint)
        .filter(Complaint.id == complaint_id)
        .first()
    )

    if complaint is None:
        return None

    ai = analyze_complaint(data.complaint)

    complaint.customer_name = data.customer_name
    complaint.email = data.email
    complaint.product = data.product
    complaint.complaint = data.complaint

    complaint.complaint_summary = ai.get("summary", "")
    complaint.category = ai.get("category", "")
    complaint.severity = ai.get("severity", "")
    complaint.root_cause = ai.get("root_cause", "")
    complaint.capa = ai.get("capa", "")
    complaint.suggested_response = ai.get("suggested_response", "")

    db.commit()
    db.refresh(complaint)

    return complaint


def delete_complaint(
    db: Session,
    complaint_id: int,
):

    complaint = (
        db.query(Complaint)
        .filter(Complaint.id == complaint_id)
        .first()
    )

    if complaint is None:
        return None

    db.delete(complaint)
    db.commit()

    return True


# ======================================================
# Authentication Functions
# ======================================================

def register_user(db: Session, user):

    existing = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing:
        return None

    db_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def login_user(db: Session, user):

    db_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if db_user is None:
        return None

    if not verify_password(
        user.password,
        db_user.password,
    ):
        return None

    token = create_access_token(
        {
            "sub": db_user.email,
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }