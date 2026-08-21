import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not configured in the .env file."
    )


client = genai.Client(
    api_key=API_KEY
)


MODEL_NAME = "gemini-3.6-flash"


def analyze_document(
    document_text: str,
    summary_length: str = "medium",
) -> dict:
    """
    Analyze a document using Gemini and return
    structured document intelligence.
    """

    length_instructions = {
        "short": (
            "Keep the summary concise, approximately "
            "100 words."
        ),
        "medium": (
            "Provide a balanced summary, approximately "
            "250 words."
        ),
        "long": (
            "Provide a detailed summary, approximately "
            "500 words."
        ),
    }

    selected_instruction = length_instructions.get(
        summary_length.lower(),
        length_instructions["medium"],
    )

    prompt = f"""
You are DocLens, an AI document intelligence assistant.

Analyze the document provided below.

Your task is to produce:

1. A clear summary.
2. The most important key points and main ideas.
3. Useful improvement suggestions based only on
   the document's content, clarity, completeness,
   or actionability.

Also create a Document Intelligence profile.

Determine:

- what type of document this is
- its primary topic
- its approximate complexity for a general reader
- its three most important themes
- the single most important takeaway
- practical actionable insights that can be derived
  from the document

Do not invent facts that are not supported by the
document.

Summary length requirement:

{selected_instruction}

Return ONLY valid JSON.

The JSON must contain these fields:

summary:
A string containing the document summary.

key_points:
An array containing the most important points.

improvement_suggestions:
An array containing useful suggestions for improving
the document.

document_intelligence:
An object containing:

document_type:
The type of document.

primary_topic:
The main subject of the document.

complexity:
Choose exactly one of:
Low, Medium, High.

main_themes:
An array containing the three most important themes.

key_takeaway:
The single most important takeaway from the document.

actionable_insights:
An array containing practical insights derived
from the document.

Do not add Markdown.
Do not add explanations outside the JSON.

The document intelligence profile must be grounded
only in the provided document.

DOCUMENT:

{document_text}
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
        result = json.loads(response_text)

    except json.JSONDecodeError as error:
        raise ValueError(
            "Gemini returned an invalid JSON response."
        ) from error

    # Basic validation to make sure the AI returned
    # the structure our application expects.

    required_fields = [
        "summary",
        "key_points",
        "improvement_suggestions",
        "document_intelligence",
    ]

    for field in required_fields:
        if field not in result:
            raise ValueError(
                f"AI response is missing required field: "
                f"{field}"
            )

    intelligence = result[
        "document_intelligence"
    ]

    intelligence_fields = [
        "document_type",
        "primary_topic",
        "complexity",
        "main_themes",
        "key_takeaway",
        "actionable_insights",
    ]

    for field in intelligence_fields:
        if field not in intelligence:
            raise ValueError(
                "AI document intelligence is missing "
                f"required field: {field}"
            )

    return result