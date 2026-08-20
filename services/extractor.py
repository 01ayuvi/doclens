import fitz


def extract_pdf(file_bytes: bytes) -> dict:
    """
    Extract text from a PDF while preserving page-level context.

    Returns:
        dict containing document metadata and page-level text.
    """

    document = fitz.open(stream=file_bytes, filetype="pdf")

    pages = []
    total_characters = 0
    total_words = 0

    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text").strip()

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

    return {
        "page_count": len(document),
        "character_count": total_characters,
        "word_count": total_words,
        "pages": pages,
    }