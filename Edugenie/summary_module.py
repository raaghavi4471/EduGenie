from gemini_client import (
    generate_text,
    GeminiConfigurationError
)


def summarize_text(text: str) -> str:

    if not text:

        return (
            "Please paste some text "
            "to summarize."
        )

    prompt = f"""
Summarize the following educational text.

TEXT:
{text}

Return the result using this structure:

Summary:
A concise summary.

Key Points:
- Point 1
- Point 2
- Point 3

Important Terms:
List important terms if applicable.

Instructions:

- Preserve the original meaning.
- Remove unnecessary repetition.
- Keep important information.
- Use simple language.
"""

    try:

        return generate_text(

            prompt,

            system_instruction=(
                "You are EduGenie, "
                "an educational summarization assistant."
            )
        )

    except GeminiConfigurationError as error:

        return str(error)

    except Exception as error:

        return (
            "Unable to summarize the text right now.\n\n"
            f"Error: {error}"
        )