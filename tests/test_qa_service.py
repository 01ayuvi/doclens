import json

import pytest

from services import qa_service


class MockResponse:
    def __init__(self, data):
        self.text = json.dumps(data)


def mock_generate_content(
    model,
    contents,
    config,
):
    return MockResponse(
        {
            "answer": (
                "Attackers abuse code-signing "
                "certificates to sign malicious software."
            ),
            "confidence": "High",
            "sources": [
                {
                    "page": 2,
                    "quote": (
                        "Attackers obtain legitimate "
                        "code-signing certificates."
                    ),
                }
            ],
            "question": (
                "How are code-signing certificates abused?"
            ),
        }
    )


def test_verified_source_is_returned(
    monkeypatch,
):

    monkeypatch.setattr(
        qa_service.client.models,
        "generate_content",
        mock_generate_content,
    )

    pages = [
        {
            "page_number": 2,
            "text": (
                "Attackers obtain legitimate "
                "code-signing certificates."
            ),
        }
    ]

    result = qa_service.answer_document_question(
        pages,
        "How are code-signing certificates abused?",
    )

    assert result["answer"]

    assert result["confidence"] == "High"

    assert len(result["sources"]) == 1

    assert result["sources"][0]["page"] == 2

    assert (
        result["sources"][0]["quote"]
        == "Attackers obtain legitimate "
        "code-signing certificates."
    )


def mock_generate_invalid_source(
    model,
    contents,
    config,
):
    return MockResponse(
        {
            "answer": (
                "The document discusses certificate abuse."
            ),
            "confidence": "High",
            "sources": [
                {
                    "page": 2,
                    "quote": (
                        "This sentence does not exist "
                        "in the document."
                    ),
                }
            ],
            "question": (
                "How are certificates abused?"
            ),
        }
    )


def test_unverified_source_is_removed(
    monkeypatch,
):

    monkeypatch.setattr(
        qa_service.client.models,
        "generate_content",
        mock_generate_invalid_source,
    )

    pages = [
        {
            "page_number": 2,
            "text": (
                "The document discusses "
                "certificate security."
            ),
        }
    ]

    result = qa_service.answer_document_question(
        pages,
        "How are certificates abused?",
    )

    assert result["sources"] == []

    assert result["confidence"] == "Low"


def mock_generate_invalid_json(
    model,
    contents,
    config,
):

    class InvalidResponse:
        text = "This is not valid JSON."

    return InvalidResponse()


def test_invalid_json_raises_error(
    monkeypatch,
):

    monkeypatch.setattr(
        qa_service.client.models,
        "generate_content",
        mock_generate_invalid_json,
    )

    pages = [
        {
            "page_number": 1,
            "text": "Sample document text.",
        }
    ]

    with pytest.raises(
        ValueError,
        match="invalid JSON",
    ):

        qa_service.answer_document_question(
            pages,
            "What is this document about?",
        )


def mock_generate_missing_field(
    model,
    contents,
    config,
):

    return MockResponse(
        {
            "answer": "Sample answer.",
            "confidence": "High",
            "sources": [],
        }
    )


def test_missing_required_field_raises_error(
    monkeypatch,
):

    monkeypatch.setattr(
        qa_service.client.models,
        "generate_content",
        mock_generate_missing_field,
    )

    pages = [
        {
            "page_number": 1,
            "text": "Sample document text.",
        }
    ]

    with pytest.raises(
        ValueError,
        match="missing required field",
    ):

        qa_service.answer_document_question(
            pages,
            "What is this document about?",
        )