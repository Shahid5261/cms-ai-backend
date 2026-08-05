from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Complaint

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard AI"],
)


@router.get("/summary")
def ai_summary(
    db: Session = Depends(get_db),
):

    complaints = db.query(Complaint).all()

    total = len(complaints)

    high = len(
        [c for c in complaints if c.severity == "High"]
    )

    resolved = len(
        [c for c in complaints if c.status == "Resolved"]
    )

    pending = len(
        [c for c in complaints if c.status == "Pending"]
    )

    resolution_rate = (
        round((resolved / total) * 100)
        if total
        else 0
    )

    satisfaction = max(
        50,
        100 - high * 2,
    )

    top_category = "N/A"

    if complaints:

        counts = {}

        for c in complaints:

            counts[c.category] = (
                counts.get(c.category, 0) + 1
            )

        top_category = max(
            counts,
            key=counts.get,
        )

    return {
        "total": total,
        "high": high,
        "pending": pending,
        "resolution_rate": resolution_rate,
        "customer_satisfaction": satisfaction,
        "top_category": top_category,
        "insights": [
            f"{top_category} complaints are currently the highest.",
            "High severity complaints require immediate attention.",
            "Customer satisfaction is stable.",
            "Continue monitoring complaint trends.",
        ],
        "recommendations": [
            "Increase QA inspections.",
            "Prioritize high severity complaints.",
            "Improve customer follow-up.",
            "Review recurring issues weekly.",
        ],
    }