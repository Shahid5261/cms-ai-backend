from io import BytesIO

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Complaint
from app.schemas import (
    ComplaintCreate,
    ComplaintResponse,
    ComplaintUpdate,
    StatusUpdate,
)
from app.crud import (
    create_complaint,
    get_all_complaints,
    update_complaint_status,
    update_complaint,
    delete_complaint,
)
from app.services.pdf_service import generate_complaint_pdf
from app.services.excel_service import generate_excel
from app.services.email_service import send_email

router = APIRouter(
    prefix="/complaints",
    tags=["Complaints"],
)


# =====================================================
# CREATE
# =====================================================

@router.post("/", response_model=ComplaintResponse)
def add_complaint(
    complaint: ComplaintCreate,
    db: Session = Depends(get_db),
):
    return create_complaint(db, complaint)


# =====================================================
# READ
# =====================================================

@router.get("/", response_model=list[ComplaintResponse])
def get_complaints(
    search: str = Query(default=""),
    category: str = Query(default=""),
    status: str = Query(default=""),
    db: Session = Depends(get_db),
):
    return get_all_complaints(
        db=db,
        search=search,
        category=category,
        status=status,
    )


# =====================================================
# UPDATE STATUS
# =====================================================

@router.put("/{complaint_id}/status")
def change_status(
    complaint_id: int,
    data: StatusUpdate,
    db: Session = Depends(get_db),
):
    complaint = update_complaint_status(
        db=db,
        complaint_id=complaint_id,
        status=data.status,
    )

    if complaint is None:
        return {"message": "Complaint not found"}

    return {
        "message": "Status updated successfully",
        "complaint": complaint,
    }


# =====================================================
# EDIT
# =====================================================

@router.put("/{complaint_id}")
def edit_complaint(
    complaint_id: int,
    data: ComplaintUpdate,
    db: Session = Depends(get_db),
):
    complaint = update_complaint(
        db=db,
        complaint_id=complaint_id,
        data=data,
    )

    if complaint is None:
        return {
            "message": "Complaint not found"
        }

    return {
        "message": "Complaint updated successfully",
        "complaint": complaint,
    }


# =====================================================
# DELETE
# =====================================================

@router.delete("/{complaint_id}")
def remove_complaint(
    complaint_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_complaint(
        db,
        complaint_id,
    )

    if not deleted:
        return {
            "message": "Complaint not found"
        }

    return {
        "message": "Complaint deleted successfully"
    }


# =====================================================
# PDF
# =====================================================

@router.get("/{complaint_id}/pdf")
def download_pdf(
    complaint_id: int,
    db: Session = Depends(get_db),
):
    complaint = (
        db.query(Complaint)
        .filter(Complaint.id == complaint_id)
        .first()
    )

    if complaint is None:
        return {"message": "Complaint not found"}

    pdf = generate_complaint_pdf(complaint)

    return StreamingResponse(
        BytesIO(pdf),
        media_type="application/pdf",
        headers={
            "Content-Disposition":
            f"attachment; filename=complaint_{complaint.id}.pdf"
        },
    )


# =====================================================
# EXCEL
# =====================================================

@router.get("/excel/download")
def download_excel(
    db: Session = Depends(get_db),
):
    complaints = (
        db.query(Complaint)
        .order_by(Complaint.id.desc())
        .all()
    )

    excel = generate_excel(complaints)

    return StreamingResponse(
        excel,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition":
            "attachment; filename=complaints.xlsx"
        },
    )


# =====================================================
# SEND EMAIL
# =====================================================

@router.post("/{complaint_id}/send-email")
def email_customer(
    complaint_id: int,
    db: Session = Depends(get_db),
):
    complaint = (
        db.query(Complaint)
        .filter(Complaint.id == complaint_id)
        .first()
    )

    if complaint is None:
        return {"message": "Complaint not found"}

    send_email(
        complaint.email,
        "Response to Your Complaint",
        complaint.suggested_response,
    )

    return {
        "message": "Email sent successfully"
    }