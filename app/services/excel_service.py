from io import BytesIO
from openpyxl import Workbook


def generate_excel(complaints):
    wb = Workbook()
    ws = wb.active
    ws.title = "Complaints"

    ws.append([
        "ID",
        "Customer",
        "Email",
        "Product",
        "Category",
        "Severity",
        "Status",
        "Summary",
        "Root Cause",
        "CAPA",
    ])

    for c in complaints:
        ws.append([
            c.id,
            c.customer_name,
            c.email,
            c.product,
            c.category,
            c.severity,
            c.status,
            c.complaint_summary,
            c.root_cause,
            c.capa,
        ])

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return output