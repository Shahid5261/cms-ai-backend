from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Complaint

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


# ==========================================================
# Dashboard Statistics
# ==========================================================

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):

    total = db.query(Complaint).count()

    pending = db.query(Complaint).filter(
        Complaint.status == "Pending"
    ).count()

    resolved = db.query(Complaint).filter(
        Complaint.status == "Resolved"
    ).count()

    high = db.query(Complaint).filter(
        func.lower(Complaint.severity) == "high"
    ).count()

    return {
        "total": total,
        "pending": pending,
        "resolved": resolved,
        "high": high
    }


# ==========================================================
# AI Executive Summary
# ==========================================================

@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):

    complaints = db.query(Complaint).all()

    total = len(complaints)

    pending = len(
        [c for c in complaints if c.status == "Pending"]
    )

    resolved = len(
        [c for c in complaints if c.status == "Resolved"]
    )

    high = len(
        [c for c in complaints if c.severity.lower() == "high"]
    )

    categories = {}

    for complaint in complaints:

        categories[complaint.category] = (
            categories.get(complaint.category, 0) + 1
        )

    top_category = (
        max(categories, key=categories.get)
        if categories
        else "N/A"
    )

    if total == 0:

        risk = "Low"

    elif pending >= total * 0.50:

        risk = "High"

    elif pending >= total * 0.30:

        risk = "Medium"

    else:

        risk = "Low"

    if risk == "High":

        recommendation = (
            "Immediate action required. Increase support staff and resolve high priority complaints first."
        )

    elif risk == "Medium":

        recommendation = (
            "Monitor complaint trends and investigate recurring issues."
        )

    else:

        recommendation = (
            "Complaint volume is under control. Continue regular monitoring."
        )

    return {

        "total": total,

        "pending": pending,

        "resolved": resolved,

        "high": high,

        "top_category": top_category,

        "risk": risk,

        "recommendation": recommendation

    }


# ==========================================================
# Notification Center
# ==========================================================

@router.get("/notifications")
def get_notifications(db: Session = Depends(get_db)):

    complaints = (
        db.query(Complaint)
        .order_by(Complaint.id.desc())
        .limit(10)
        .all()
    )

    notifications = []

    for complaint in complaints:

        # High Severity
        if complaint.severity.lower() == "high":

            notifications.append({

                "type": "danger",

                "title": "High Priority Complaint",

                "message": f"{complaint.customer_name} reported a HIGH severity issue with {complaint.product}.",

                "time": "Just now"

            })

        # Resolved
        elif complaint.status == "Resolved":

            notifications.append({

                "type": "success",

                "title": "Complaint Resolved",

                "message": f"{complaint.customer_name}'s complaint has been successfully resolved.",

                "time": "Recently"

            })

        # Pending
        elif complaint.status == "Pending":

            notifications.append({

                "type": "warning",

                "title": "Pending Complaint",

                "message": f"Complaint from {complaint.customer_name} is awaiting action.",

                "time": "Today"

            })

        # Others
        else:

            notifications.append({

                "type": "info",

                "title": "New Complaint",

                "message": f"New complaint received from {complaint.customer_name}.",

                "time": "Today"

            })

    return notifications