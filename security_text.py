from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

# Initialize Presidio engines
try:
    _analyzer = AnalyzerEngine()
    _anonymizer = AnonymizerEngine()
except Exception as e:
    print(f"Error loading Presidio: {e}")
    _analyzer = None
    _anonymizer = None

# -------------------------------
# 1. Custom Patterns (Aadhaar & Crypto)
# -------------------------------

# Aadhaar (Indian ID)
aadhaar_pattern = Pattern(
    name="AADHAAR Pattern",
    regex=r"\b[2-9]\d{3}\s?\d{4}\s?\d{4}\b",
    score=1.0
)
aadhaar_recognizer = PatternRecognizer(
    supported_entity="AADHAAR",
    patterns=[aadhaar_pattern]
)

# API Keys / Crypto (Basic Regex for demo)
crypto_pattern = Pattern(
    name="API_KEY Pattern",
    regex=r"(sk-[a-zA-Z0-9]{20,}|0x[a-fA-F0-9]{40})",
    score=1.0
)
crypto_recognizer = PatternRecognizer(
    supported_entity="API_KEY",
    patterns=[crypto_pattern]
)

if _analyzer:
    _analyzer.registry.add_recognizer(aadhaar_recognizer)
    _analyzer.registry.add_recognizer(crypto_recognizer)


# -------------------------------
# 2. Targeted Scanning (The Fix)
# -------------------------------
def scan_text(text: str):
    """
    Detect ONLY high-risk entities.
    Ignores PERSON, LOCATION, DATE_TIME to avoid false positives.
    """
    if not _analyzer: return []
    
    # We explicitly list ONLY what we want to block.
    # We exclude 'PERSON', 'LOCATION', 'ORGANIZATION' so "Bresenham" is safe.
    target_entities = [
        "PHONE_NUMBER", 
        "EMAIL_ADDRESS", 
        "CREDIT_CARD", 
        "US_SSN", 
        "AADHAAR", 
        "API_KEY",
        "IP_ADDRESS"
    ]
    
    return _analyzer.analyze(
        text=text,
        language="en",
        entities=target_entities
    )


# -------------------------------
# 3. Sanitization
# -------------------------------
def sanitize_text(text: str):
    """
    Redacts sensitive entities from text.
    """
    if not _analyzer or not _anonymizer:
        return text

    results = scan_text(text)

    if not results:
        return text

    operators = {
        "DEFAULT": OperatorConfig(
            operator_name="replace",
            params={"new_value": "<REDACTED>"}
        )
    }

    anonymized = _anonymizer.anonymize(
        text=text,
        analyzer_results=results,
        operators=operators
    )

    return anonymized.text

security_text.py
