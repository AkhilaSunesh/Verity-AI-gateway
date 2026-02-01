from PIL import Image

def scan_image(image_path: str):
    """
    Detect whether an image contains sensitive information.
    This is a detection-first security gate.
    """

    # Load image
    image = Image.open(image_path)

    # Security-focused question for vision model
    prompt = (
        "Does this image contain sensitive personal information "
        "such as an Aadhaar card, passport, ID card, credit card, "
        "or any official document?"
    )

    # Placeholder for Moondream inference
    response = run_moondream(image, prompt)

    if "yes" in response.lower():
        return {
            "sensitive": True,
            "action": "BLOCK"
        }

    return {
        "sensitive": False,
        "action": "ALLOW"
    }


def run_moondream(image, prompt):
    """
    Mock Moondream response for hackathon demo.
    """
    return "yes, this looks like an identity document"
