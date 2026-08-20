from pathlib import Path

from services.extractor import extract_pdf
from services.ocr import extract_text_from_image


SUPPORTED_IMAGE_TYPES = {
    ".png",
    ".jpg",
    ".jpeg",
}


def process_document(
    file_bytes: bytes,
    filename: str,
) -> dict:
    """
    Process a PDF or image and return a normalized
    document representation.
    """

    extension = Path(filename).suffix.lower()

    if extension == ".pdf":

        result = extract_pdf(file_bytes)

        return {
            "filename": filename,
            "file_type": "pdf",
            "page_count": result["page_count"],
            "word_count": result["word_count"],
            "character_count": result["character_count"],
            "pages": result["pages"],
        }

    if extension in SUPPORTED_IMAGE_TYPES:

        result = extract_text_from_image(
            file_bytes
        )

        text = result["text"]

        return {
            "filename": filename,
            "file_type": "image",
            "page_count": 1,
            "word_count": result["word_count"],
            "character_count": result["character_count"],
            "pages": [
                {
                    "page_number": 1,
                    "text": text,
                    "character_count": result[
                        "character_count"
                    ],
                    "word_count": result[
                        "word_count"
                    ],
                }
            ],
        }

    raise ValueError(
        "Unsupported file type. "
        "Please upload a PDF, PNG, JPG, or JPEG."
    )