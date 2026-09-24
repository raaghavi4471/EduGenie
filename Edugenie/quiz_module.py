import re
from typing import List

from pydantic import BaseModel, Field

from google.genai import types

from gemini_client import (
    get_client,
    GEMINI_MODEL,
    GeminiConfigurationError
)


# --------------------------------------------------
# QUIZ DATA STRUCTURES
# --------------------------------------------------

class QuizQuestion(BaseModel):

    question: str

    options: List[str] = Field(
        min_length=4,
        max_length=4
    )

    correct_answer: str

    explanation: str


class QuizResponse(BaseModel):

    questions: List[QuizQuestion] = Field(
        min_length=3,
        max_length=3
    )


# --------------------------------------------------
# CLEAN MARKDOWN JSON
# --------------------------------------------------

def clean_json_block(text: str) -> str:

    text = text.strip()

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    return text.strip()


# --------------------------------------------------
# GENERATE QUIZ
# --------------------------------------------------

def generate_quiz(text: str):

    if not text:

        return {
            "error": "Please enter a topic or passage."
        }

    prompt = f"""
Create exactly 3 multiple-choice questions
from the following educational material.

Material:
{text}

Rules:

1. Generate exactly 3 questions.
2. Every question must contain exactly 4 options.
3. Only one option must be correct.
4. correct_answer must exactly match one option.
5. Add a short explanation for every answer.
6. Questions should test understanding.
"""

    try:

        client = get_client()

        response = client.models.generate_content(

            model=GEMINI_MODEL,

            contents=prompt,

            config=types.GenerateContentConfig(

                temperature=0.3,

                response_mime_type="application/json",

                response_schema=QuizResponse
            )
        )

        # Try structured response first
        parsed = getattr(
            response,
            "parsed",
            None
        )

        if parsed is not None:

            if isinstance(
                parsed,
                QuizResponse
            ):

                return parsed.model_dump()

            if hasattr(
                parsed,
                "model_dump"
            ):

                return QuizResponse.model_validate(
                    parsed
                ).model_dump()

        # Fallback: parse text JSON
        raw = getattr(
            response,
            "text",
            ""
        ) or ""

        raw = clean_json_block(raw)

        if not raw:

            return {
                "error": "Gemini returned an empty quiz."
            }

        quiz = QuizResponse.model_validate_json(
            raw
        )

        return quiz.model_dump()

    except GeminiConfigurationError as error:

        return {
            "error": str(error)
        }

    except Exception as error:

        return {
            "error": (
                "Quiz generation failed: "
                f"{error}"
            )
        }