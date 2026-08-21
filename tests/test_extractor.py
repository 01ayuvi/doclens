import pymupdf

from services.extractor import extract_pdf


def create_test_pdf():
    document = pymupdf.open()

    page = document.new_page()

    page.insert_text(
        (72, 72),
        "DocLens extraction test document."
    )

    page.insert_text(
        (72, 100),
        "This document contains sample text."
    )

    pdf_bytes = document.tobytes()

    document.close()

    return pdf_bytes


def test_extract_pdf_returns_page_information():

    pdf_bytes = create_test_pdf()

    result = extract_pdf(pdf_bytes)

    assert "pages" in result
    assert "page_count" in result
    assert "word_count" in result
    assert "character_count" in result

    assert result["page_count"] == 1
    assert result["word_count"] > 0
    assert result["character_count"] > 0


def test_extract_pdf_preserves_page_numbers():

    pdf_bytes = create_test_pdf()

    result = extract_pdf(pdf_bytes)

    page_numbers = [
        page["page_number"]
        for page in result["pages"]
    ]

    assert page_numbers == [1]