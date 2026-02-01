from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

# Initialize Presidio engines once
_analyzer = AnalyzerEngine()
_anonymizer = AnonymizerEngine()

# -------------------------------
# Custom Aadhaar (Indian ID) recognizer
# -------------------------------
aadhaar_pattern = Pattern(
    name="AADHAAR Pattern",
    regex=r"\b[2-9]\d{3}\s?\d{4}\s?\d{4}\b",
    score=1.0
)

aadhaar_recognizer = PatternRecognizer(
    supported_entity="AADHAAR",
    patterns=[aadhaar_pattern]
)

_analyzer.registry.add_recognizer(aadhaar_recognizer)


# -------------------------------
# Text scanning function
# -------------------------------
def scan_text(text: str):
    """
    Detect sensitive entities in text using Presidio.
    Returns a list of detected entities.
    """
    return _analyzer.analyze(
        text=text,
        language="en"
    )


# -------------------------------
# Text sanitization function
# -------------------------------
def sanitize_text(text: str):
    """
    Redacts sensitive entities from text.
    Returns sanitized text.
    """
    results = scan_text(text)

    if not results:
        return text  # No sensitive data found

    operators = {
        "DEFAULT": OperatorConfig(
            operator_name="replace",
            params={"new_value": "[REDACTED]"}
        )
    }

    anonymized = _anonymizer.anonymize(
        text=text,
        analyzer_results=results,
        operators=operators
    )

    return anonymized.text
