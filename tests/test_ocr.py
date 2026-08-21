from io import BytesIO

from PIL import Image, ImageDraw

from services.ocr import extract_text_from_image


def create_test_image_bytes():
    image = Image.new(
        "RGB",
        (800, 300),
        "white",
    )

    draw = ImageDraw.Draw(image)

    draw.text(
        (50, 50),
        "DOCLENS OCR TEST",
        fill="black",
    )

    draw.text(
        (50, 120),
        "Document Intelligence Assistant",
        fill="black",
    )

    draw.text(
        (50, 190),
        "OCR extraction test",
        fill="black",
    )

    image_bytes = BytesIO()

    image.save(
        image_bytes,
        format="PNG",
    )

    return image_bytes.getvalue()


def test_ocr_extracts_text():

    image_bytes = create_test_image_bytes()

    result = extract_text_from_image(
        image_bytes
    )

    assert isinstance(result, dict)

    assert "text" in result

    extracted_text = result["text"]

    assert len(extracted_text.strip()) > 0

    assert "DOCLENS" in extracted_text.upper()
    assert "OCR" in extracted_text.upper()