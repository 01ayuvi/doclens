import pymupdf

from services.document_processor import process_document
from io import BytesIO

from PIL import Image, ImageDraw


def create_test_pdf():
    document = pymupdf.open()

    page = document.new_page()

    page.insert_text(
        (72, 72),
        "DocLens integration test."
    )

    page.insert_text(
        (72, 100),
        "Testing document processing."
    )

    pdf_bytes = document.tobytes()

    document.close()

    return pdf_bytes


def test_process_pdf():

    pdf_bytes = create_test_pdf()

    result = process_document(
        pdf_bytes,
        "integration_test.pdf",
    )

    assert result["filename"] == "integration_test.pdf"

    assert result["file_type"] == "pdf"

    assert result["page_count"] == 1

    assert result["word_count"] > 0

    assert result["character_count"] > 0

    assert len(result["pages"]) == 1

    assert result["pages"][0]["page_number"] == 1

    assert (
        "DocLens"
        in result["pages"][0]["text"]
    )
    


def create_test_image_bytes():

    image = Image.new(
        "RGB",
        (800, 300),
        "white",
    )

    draw = ImageDraw.Draw(image)

    draw.text(
        (50, 50),
        "DOCLENS PROCESSOR TEST",
        fill="black",
    )

    draw.text(
        (50, 120),
        "OCR integration test",
        fill="black",
    )

    image_bytes = BytesIO()

    image.save(
        image_bytes,
        format="PNG",
    )

    return image_bytes.getvalue()


def test_process_image_with_ocr():

    image_bytes = create_test_image_bytes()

    result = process_document(
        image_bytes,
        "integration_test.png",
    )

    assert result["filename"] == "integration_test.png"

    assert result["file_type"] == "image"

    assert result["page_count"] == 1

    assert result["word_count"] > 0

    assert result["character_count"] > 0

    assert len(result["pages"]) == 1

    assert result["pages"][0]["page_number"] == 1

    extracted_text = result["pages"][0]["text"]

    assert "DOCLENS" in extracted_text.upper()
    assert "OCR" in extracted_text.upper()
    
def test_process_invalid_file():

    invalid_bytes = b"This is not a valid PDF or image."

    try:

        process_document(
            invalid_bytes,
            "invalid_document.pdf",
        )

    except Exception as error:

        assert isinstance(
            error,
            Exception,
        )

    else:

        raise AssertionError(
            "Invalid document should raise an exception."
        )