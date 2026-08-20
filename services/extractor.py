import pymupdf

from services.ocr import extract_text_from_image


def extract_pdf(file_bytes: bytes) -> dict:
    """
    Extract text from a PDF.

    Uses normal PDF text extraction when text is available.
    Falls back to OCR for pages without embedded text.
    """

    document = pymupdf.open(
        stream=file_bytes,
        filetype="pdf"
    )

    pages = []
    total_characters = 0
    total_words = 0

    for page_number, page in enumerate(
        document,
        start=1
    ):

        text = page.get_text("text").strip()

        # OCR fallback for scanned/image-based pages
        if not text:

            pixmap = page.get_pixmap(
                matrix=pymupdf.Matrix(2, 2),
                alpha=False
            )

            image_bytes = pixmap.tobytes(
                "png"
            )

            ocr_result = extract_text_from_image(
                image_bytes
            )

            text = ocr_result["text"]

        character_count = len(text)
        word_count = len(text.split())

        total_characters += character_count
        total_words += word_count

        pages.append(
            {
                "page_number": page_number,
                "text": text,
                "character_count": character_count,
                "word_count": word_count,
            }
        )

    document.close()

    return {
        "page_count": len(pages),
        "character_count": total_characters,
        "word_count": total_words,
        "pages": pages,
    }