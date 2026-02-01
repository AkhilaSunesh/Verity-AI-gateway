import easyocr
import numpy as np
import re  # <--- NEW IMPORT for pattern matching
from PIL import Image

# Global variable
_reader = None

def load_ocr():
    global _reader
    if _reader is not None:
        return _reader
    
    print("👁️ Loading OCR Engine...")
    try:
        # Load English model
        _reader = easyocr.Reader(['en'], gpu=False) 
        print("✅ OCR Engine Loaded!")
        return _reader
    except Exception as e:
        print(f"❌ Error loading OCR: {e}")
        return None

load_ocr()

def analyze_image(image_file):
    global _reader
    if _reader is None:
        return True, "⚠️ Dev Mode: OCR Failed"

    try:
        image = Image.open(image_file)
        image_np = np.array(image)

        # Extract text
        result = _reader.readtext(image_np, detail=0)
        extracted_text = " ".join(result).lower()
        
        print(f"DEBUG OCR READ: {extracted_text}")

        # --- STRATEGY 1: KEYWORD BLOCKLIST ---
        threats = [
            "aadhaar", "government of india", "income tax", "pan card", 
            "passport", "republic of india", "driving licence", "license",
            "permanent account number", "father's name", "dob", 
            "male", "female", "yob"
        ]

        for keyword in threats:
            if keyword in extracted_text:
                return False, f"Visual Threat Detected: Found keyword '{keyword.upper()}'"

        # --- STRATEGY 2: NUMBER PATTERNS (The Fix!) ---
        # Aadhaar numbers look like: 1234 5678 9012 (3 groups of 4 digits)
        # Regex explanation: \d{4} means "4 digits", \s? means "optional space"
        aadhaar_pattern = r"\b\d{4}\s?\d{4}\s?\d{4}\b"
        
        if re.search(aadhaar_pattern, extracted_text):
            return False, "Visual Threat Detected: Found 12-digit ID Number"

        return True, "Safe"

    except Exception as e:
        print(f"Error: {e}")
        return False, f"Error processing image: {e}"


security_image.txt
