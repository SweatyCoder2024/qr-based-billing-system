# desktop_app/services/label_printer_service.py

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import qrcode
from io import BytesIO
from PIL import Image

def generate_qr_pdf(items: list, output_path: str):
    """
    Generates a PDF with a grid of QR codes for printing.
    """
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # --- Settings for the grid ---
    margin = 0.5 * inch
    label_width = 2.5 * inch
    label_height = 1.0 * inch
    cols = 3
    rows = 10

    x_start, y_start = margin, height - margin - label_height
    x, y = x_start, y_start

    for i, item in enumerate(items):
        # --- Check if we need a new page ---
        if i > 0 and i % (cols * rows) == 0:
            c.showPage()
            x, y = x_start, y_start

        # --- Generate QR Code Image ---
        qr_text = item.get("qr_code", "")
        if not qr_text:
            continue

        qr_img = qrcode.make(qr_text)
        pil_img = qr_img.convert("RGB")

        # Use BytesIO to handle the image in memory
        img_buffer = BytesIO()
        pil_img.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        # --- Draw the label on the PDF ---
        qr_image_size = label_height - (0.2 * inch)

        # Draw QR Code
        c.drawImage(Image.open(img_buffer), x, y + 0.1 * inch, width=qr_image_size, height=qr_image_size, preserveAspectRatio=True, anchor='n')

        # Draw Item Name and Code
        text_x = x + qr_image_size + 0.1 * inch
        c.setFont("Helvetica", 8)
        c.drawString(text_x, y + 0.6 * inch, item.get("name", "N/A"))
        c.setFont("Helvetica-Bold", 7)
        c.drawString(text_x, y + 0.4 * inch, item.get("qr_code", ""))

        # Move to the next label position
        x += label_width
        if (i + 1) % cols == 0:
            x = x_start
            y -= label_height

    c.save()