from gemini_client import (
    generate_text,
    GeminiConfigurationError
)


def answer_question(question: str) -> str:

    if not question:

        return "Please enter a question."

    prompt = f"""
Answer the student's question clearly and accurately.

Question:
{question}

Instructions:

1. Give the direct answer first.
2. Explain the answer in simple language.
3. Add useful context when necessary.
4. Use an example if it helps.
5. Do not make up facts.
6. Keep the explanation suitable for a student.
"""

    try:

        result = generate_text(

            prompt,

            system_instruction=(
                "You are EduGenie, "
                "a helpful educational question-answering assistant."
            )
        )

        return result

    except GeminiConfigurationError as error:

        return str(error)

    except Exception as error:

        return (
            "Unable to answer the question right now.\n\n"
            f"Error: {error}"
        )