from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

def generate_pdf(jobcard, form_data):
    """
    Generates a simple PDF for the jobcard using ReportLab.
    In a real app, this would iterate over form_data to render all fields.
    """
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Header
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, f"Jobcard: {jobcard.jobcard_id}")

    p.setFont("Helvetica", 12)
    p.drawString(50, height - 80, f"Client: {jobcard.client.name}")
    p.drawString(50, height - 100, f"Technician: {jobcard.technician.username}")
    p.drawString(50, height - 120, f"Date: {jobcard.created_at.strftime('%Y-%m-%d')}")

    # Body (Generic dump of form data for MVP)
    y = height - 160
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Form Data:")
    y -= 20
    p.setFont("Helvetica", 10)

    for key, value in form_data.items():
        if key in ['submit', 'clientSignature', 'techSignature']: # Skip signatures/buttons for text dump
            continue

        # Handle lists (like datagrids)
        if isinstance(value, list):
            p.drawString(50, y, f"{key}:")
            y -= 15
            for item in value:
                p.drawString(70, y, str(item))
                y -= 15
        else:
            p.drawString(50, y, f"{key}: {str(value)}")
            y -= 15

        if y < 50: # New page if full
            p.showPage()
            y = height - 50

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    return pdf
