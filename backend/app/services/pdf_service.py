# backend/app/services/pdf_service.py

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

def generate_bill_pdf(order_details: dict) -> bytes:
    """
    Generates a PDF bill from order details and returns it as bytes.
    """
    buffer = BytesIO()

    # Create the PDF document
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # --- Header ---
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(width / 2.0, height - 1 * inch, "SHRI GURUDEVDATTA FATAKA TRADERS")

    p.setFont("Helvetica", 12)
    p.drawCentredString(width / 2.0, height - 1.25 * inch, "Your Store Address, City")

    p.setFont("Helvetica-Bold", 14)
    p.drawString(1 * inch, height - 2 * inch, f"Bill / Order ID: {order_details.get('id', 'N/A')}")
    p.drawString(1 * inch, height - 2.25 * inch, f"Date: {order_details.get('date', 'N/A')}")

    # --- Table Header ---
    p.setFont("Helvetica-Bold", 12)
    y_position = height - 3 * inch
    p.drawString(1 * inch, y_position, "Item Name")
    p.drawString(4 * inch, y_position, "Quantity")
    p.drawString(5 * inch, y_position, "Unit Price")
    p.drawString(6.5 * inch, y_position, "Total")
    p.line(1 * inch, y_position - 0.1 * inch, width - 1 * inch, y_position - 0.1 * inch)

    # --- Items Loop ---
    p.setFont("Helvetica", 11)
    y_position -= 0.4 * inch

    items = order_details.get('items', [])
    for item in items:
        p.drawString(1 * inch, y_position, str(item.get('name', '')))
        p.drawString(4.25 * inch, y_position, str(item.get('quantity', '')))
        p.drawString(5.25 * inch, y_position, f"₹{item.get('unit_price', 0.0):.2f}")
        p.drawString(6.75 * inch, y_position, f"₹{item.get('total_price', 0.0):.2f}")
        y_position -= 0.3 * inch

        if y_position < 1.5 * inch: # Add a new page if we run out of space
            p.showPage()
            y_position = height - 1 * inch

    # --- Footer / Total ---
    p.line(1 * inch, y_position + 0.2 * inch, width - 1 * inch, y_position + 0.2 * inch)
    p.setFont("Helvetica-Bold", 14)
    total_amount = order_details.get('total_amount', 0.0)
    p.drawString(5 * inch, y_position, f"Grand Total: ₹{total_amount:.2f}")

    # Finalize the PDF
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and return it
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes