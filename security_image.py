import easyocr
import numpy as np
import re
from PIL import Image

_reader = None

def load_ocr():
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(['en'], gpu=False)
    return _reader

def analyze_image(image_file):
    reader = load_ocr()
    try:
        image = Image.open(image_file)
        image_np = np.array(image)
        result = reader.readtext(image_np, detail=0)
        extracted_text = " ".join(result).lower()
        
        threats = ["aadhaar", "pan card", "passport", "driving licence"]
        for keyword in threats:
            if keyword in extracted_text:
                return False, f"Found keyword '{keyword.upper()}'"
        
        # 12-digit pattern for Aadhaar detection
        if re.search(r"\b\d{4}\s?\d{4}\s?\d{4}\b", extracted_text):
            return False, "Found 12-digit ID pattern"
            
        return True, "Safe"
    except Exception as e:
        return False, f"Scan Error: {str(e)}"
