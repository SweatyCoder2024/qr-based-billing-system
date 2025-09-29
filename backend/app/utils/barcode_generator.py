# backend/app/utils/barcode_generator.py

import uuid

def generate_unique_barcode():
    """Generates a unique, human-readable barcode string."""
    # Takes the first 8 characters of a UUID for a short but highly unique ID
    unique_id = uuid.uuid4().hex[:8].upper()
    return f"ITEM-{unique_id}"