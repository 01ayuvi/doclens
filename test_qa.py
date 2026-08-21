from pathlib import Path

from services.document_processor import process_document
from services.qa_service import answer_document_question


pdf_path = Path(
    "sample_documents/test.pdf"
)

file_bytes = pdf_path.read_bytes()

document = process_document(
    file_bytes,
    pdf_path.name,
)


question = (
    "What is the author's favorite programming language?"
)

result = answer_document_question(
    document["pages"],
    question,
)


print("\n===== QUESTION =====\n")

print(
    result["question"]
)


print("\n===== ANSWER =====\n")

print(
    result["answer"]
)


print("\n===== SOURCE PAGES =====\n")

print(
    result["source_pages"]
)


print("\n===== CONFIDENCE =====\n")

print(
    result["confidence"]
)