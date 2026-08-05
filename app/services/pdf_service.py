from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER


def generate_complaint_pdf(complaint):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER

    heading = styles["Heading2"]
    normal = styles["BodyText"]

    elements = []

    elements.append(
        Paragraph("AI Complaint Management System", title_style)
    )

    elements.append(Spacer(1, 20))

    elements.append(Paragraph(f"<b>Complaint ID:</b> {complaint.id}", normal))
    elements.append(Paragraph(f"<b>Customer:</b> {complaint.customer_name}", normal))
    elements.append(Paragraph(f"<b>Email:</b> {complaint.email}", normal))
    elements.append(Paragraph(f"<b>Product:</b> {complaint.product}", normal))
    elements.append(Paragraph(f"<b>Status:</b> {complaint.status}", normal))
    elements.append(Paragraph(f"<b>Category:</b> {complaint.category}", normal))
    elements.append(Paragraph(f"<b>Severity:</b> {complaint.severity}", normal))

    elements.append(Spacer(1, 15))

    elements.append(Paragraph("Original Complaint", heading))
    elements.append(Paragraph(complaint.complaint, normal))

    elements.append(Spacer(1, 12))

    elements.append(Paragraph("AI Summary", heading))
    elements.append(Paragraph(complaint.complaint_summary or "", normal))

    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Root Cause", heading))
    elements.append(Paragraph(complaint.root_cause or "", normal))

    elements.append(Spacer(1, 12))

    elements.append(Paragraph("CAPA", heading))
    elements.append(Paragraph(complaint.capa or "", normal))

    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Suggested Response", heading))
    elements.append(
        Paragraph(complaint.suggested_response or "", normal)
    )

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf