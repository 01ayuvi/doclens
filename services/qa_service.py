import json
import os
import re

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai import errors


load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not configured."
    )


client = genai.Client(
    api_key=API_KEY
)


MODEL_NAME = "gemini-3.6-flash"


def _normalize_text(text: str) -> str:
    """
    Normalize whitespace and casing so that source
    excerpts can be compared reliably.
    """

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def _verify_source_quotes(
    pages: list[dict],
    sources: list[dict],
) -> list[dict]:
    """
    Verify AI-provided source excerpts against
    extracted page text while tolerating differences
    in whitespace and line breaks.
    """

    verified_sources = []

    pages_by_number = {
        page["page_number"]: page
        for page in pages
    }

    for source in sources:

        page_number = source.get("page")
        quote = source.get("quote", "")

        if not isinstance(page_number, int):
            continue

        if not isinstance(quote, str):
            continue

        if not quote.strip():
            continue

        page = pages_by_number.get(page_number)

        if not page:
            continue

        page_text = _normalize_text(
            page["text"]
        )

        normalized_quote = _normalize_text(
            quote
        )

        # Exact normalized match
        if normalized_quote in page_text:

            verified_sources.append(
                {
                    "page": page_number,
                    "quote": quote.strip(),
                }
            )

            continue

        # -----------------------------------------
        # TOLERANT MATCH
        # -----------------------------------------
        #
        # PDF extraction may introduce line breaks,
        # spacing differences, or hyphenation.
        #

        quote_words = normalized_quote.split()

        if len(quote_words) >= 8:

            matched_words = sum(
                1
                for word in quote_words
                if word in page_text
            )

            match_ratio = (
                matched_words / len(quote_words)
            )

            if match_ratio >= 0.75:

                verified_sources.append(
                    {
                        "page": page_number,
                        "quote": quote.strip(),
                    }
                )

    return verified_sources


def answer_document_question(
    pages: list[dict],
    question: str,
) -> dict:
    """
    Answer a question using only the uploaded
    document's extracted page content.

    Returns:
        Answer, confidence, and verified source evidence.
    """

    page_context = "\n\n".join(
        (
            f"--- PAGE {page['page_number']} ---\n"
            f"{page['text']}"
        )
        for page in pages
        if page["text"]
    )

    prompt = f"""
You are DocLens, an AI assistant that answers
questions about an uploaded document.

Answer the user's question using ONLY the
document context provided below.

Do not use outside knowledge.

If the answer cannot be determined from the
document, clearly say that the document does
not provide enough information.

For every source used to support the answer,
provide:

1. The exact page number.
2. A short exact excerpt copied from that page.

The excerpt must be copied word-for-word from
the provided document context.

Do not paraphrase source excerpts.

If the document does not support the answer,
return an empty sources array.

Return ONLY valid JSON.

The JSON must contain:

answer:
A clear and concise answer to the user's question.

confidence:
Choose exactly one:
High, Medium, Low.

sources:
An array of objects with this structure:

[
  {{
    "page": 1,
    "quote": "exact text copied from the document"
  }}
]

question:
The original user question.

DOCUMENT CONTEXT:

{page_context}

USER QUESTION:

{question}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            automatic_function_calling=(
                types.AutomaticFunctionCallingConfig(
                    disable=True
                )
            ),
        ),
    )

    response_text = response.text.strip()

    try:

        result = json.loads(
            response_text
        )

    except json.JSONDecodeError as error:

        raise ValueError(
            "Gemini returned an invalid JSON response."
        ) from error

    required_fields = [
        "answer",
        "confidence",
        "sources",
        "question",
    ]

    for field in required_fields:

        if field not in result:

            raise ValueError(
                f"AI response is missing required "
                f"field: {field}"
            )

    # -----------------------------------------
    # VERIFY AI-PROVIDED SOURCES
    # -----------------------------------------

    verified_sources = _verify_source_quotes(
        pages,
        result["sources"],
    )

    result["sources"] = verified_sources

    # -----------------------------------------
    # CONFIDENCE SAFETY CHECK
    # -----------------------------------------

    if not verified_sources:

        result["confidence"] = "Low"

    return result