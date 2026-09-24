import os
from functools import lru_cache

from dotenv import load_dotenv
from google import genai
from google.genai import types


# Load .env
load_dotenv()


# Gemini configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)


class GeminiConfigurationError(Exception):
    pass


@lru_cache(maxsize=1)
def get_client():

    if not GEMINI_API_KEY:

        raise GeminiConfigurationError(
            "GEMINI_API_KEY is missing. "
            "Please add your Gemini API key to the .env file."
        )

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )

    return client


def generate_text(
    prompt: str,
    system_instruction: str | None = None
):

    client = get_client()

    config = types.GenerateContentConfig(
        temperature=0.4,
        system_instruction=system_instruction
    )

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=config
    )

    text = getattr(
        response,
        "text",
        None
    )

    if not text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text.strip()