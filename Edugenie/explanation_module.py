import os
from functools import lru_cache

from gemini_client import (
    generate_text,
    GeminiConfigurationError
)


# --------------------------------------------------
# OPTIONAL LOCAL MODEL
# --------------------------------------------------

@lru_cache(maxsize=1)
def get_local_pipeline():

    from transformers import pipeline

    model_name = os.getenv(
        "LOCAL_EXPLAINER_MODEL",
        "MBZUAI/LaMini-Flan-T5-783M"
    )

    return pipeline(
        "text2text-generation",
        model=model_name
    )


def local_explanation(topic: str) -> str:

    pipeline_model = get_local_pipeline()

    prompt = f"""
Explain the following concept to a beginner.

Concept:
{topic}

Use simple language and one easy example.
"""

    result = pipeline_model(
        prompt,
        max_new_tokens=220,
        do_sample=False
    )

    return result[0]["generated_text"].strip()


# --------------------------------------------------
# MAIN EXPLANATION FUNCTION
# --------------------------------------------------

def explain_concept(topic: str) -> str:

    if not topic:

        return "Please enter a topic to explain."

    use_local_model = (
        os.getenv(
            "ENABLE_LOCAL_EXPLAINER",
            "false"
        ).lower() == "true"
    )

    # Try local model if enabled
    if use_local_model:

        try:

            return local_explanation(topic)

        except Exception:

            # Fall back to Gemini
            pass

    prompt = f"""
Explain the following educational concept
to a beginner.

Topic:
{topic}

Structure your answer like this:

1. Simple definition
2. How it works
3. Easy example
4. Important points
5. Short takeaway

Avoid complicated terminology.
"""

    try:

        return generate_text(

            prompt,

            system_instruction=(
                "You are EduGenie. "
                "Your job is to simplify difficult "
                "educational concepts for students."
            )
        )

    except GeminiConfigurationError as error:

        return str(error)

    except Exception as error:

        return (
            "Unable to explain the topic right now.\n\n"
            f"Error: {error}"
        )