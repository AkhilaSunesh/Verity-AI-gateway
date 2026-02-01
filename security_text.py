from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

try:
    _analyzer = AnalyzerEngine()
    _anonymizer = AnonymizerEngine()
except Exception as e:
    _analyzer = None
    _anonymizer = None

# Custom Aadhaar Pattern
aadhaar_pattern = Pattern(
    name="AADHAAR Pattern",
    regex=r"\b[2-9]\d{3}\s?\d{4}\s?\d{4}\b",
    score=1.0
)
aadhaar_recognizer = PatternRecognizer(supported_entity="AADHAAR", patterns=[aadhaar_pattern])

if _analyzer:
    _analyzer.registry.add_recognizer(aadhaar_recognizer)

def sanitize_text(text: str):
    if not _analyzer or not _anonymizer:
        return text
    
    target_entities = ["PHONE_NUMBER", "EMAIL_ADDRESS", "CREDIT_CARD", "AADHAAR", "API_KEY"]
    results = _analyzer.analyze(text=text, language="en", entities=target_entities)
    
    operators = {"DEFAULT": OperatorConfig("replace", {"new_value": "<REDACTED>"})}
    anonymized = _anonymizer.anonymize(text=text, analyzer_results=results, operators=operators)
    return anonymized.text
