import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


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


def analyze_document(
    document_text: str,
    summary_length: str = "medium",
) -> dict:
    """
    Analyze document content using Gemini.

    Returns:
        Structured document analysis.
    """

    length_instructions = {
        "short": (
            "Keep the summary concise, approximately "
            "100 words."
        ),
        "medium": (
            "Provide a moderately detailed summary, "
            "approximately 250 words."
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
2. The most important key points/main ideas.
3. Useful improvement suggestions based on the
   document's content, clarity, completeness, or
   actionability.

Summary length requirement:
{selected_instruction}

Return ONLY valid JSON using exactly this structure:

{{
  "summary": "string",
  "key_points": [
    "string",
    "string",
    "string"
  ],
  "improvement_suggestions": [
    "string",
    "string",
    "string"
  ]
}}

Do not add Markdown.
Do not add explanations outside the JSON.

DOCUMENT:

{document_text}
"""

    response = client.models.generate_content(
    model=MODEL_NAME,
    contents=prompt,
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        ),
    ),
)

    response_text = response.text.strip()

    # Remove accidental Markdown code fences.
    if response_text.startswith("```"):
        response_text = response_text.strip("`")

        if response_text.startswith("json"):
            response_text = response_text[4:].strip()

    try:

        result = json.loads(
            response_text
        )

    except json.JSONDecodeError as error:

        raise ValueError(
            "The AI returned an invalid response."
        ) from error

    return result