from io import BytesIO

from PIL import Image
import pytesseract


def extract_text_from_image(image_bytes: bytes) -> dict:
    """
    Extract text from an image using Tesseract OCR.

    Args:
        image_bytes: Image file content as bytes.

    Returns:
        Dictionary containing extracted text and basic metadata.
    """

    image = Image.open(
        BytesIO(image_bytes)
    )

    text = pytesseract.image_to_string(
        image
    ).strip()

    return {
        "text": text,
        "character_count": len(text),
        "word_count": len(text.split()),
    }