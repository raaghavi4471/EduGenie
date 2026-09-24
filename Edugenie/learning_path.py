from gemini_client import generate_text, GeminiConfigurationError


def get_learning_recommendations(topic: str) -> str:
    if not topic:
        return "Please enter a topic."

    prompt = f"""
Create a complete learning path for the following topic:

{topic}

The learner should progress from beginner to advanced.

Include:

1. Prerequisites
2. Beginner level
3. Intermediate level
4. Advanced level
5. Suggested timeline
6. Practice exercises
7. Project ideas
8. Recommended types of resources
9. Final checklist

Make the plan practical and realistic.

Do not invent specific website URLs.
"""

    try:
        result = generate_text(
            prompt,
            system_instruction=(
                "You are EduGenie, "
                "a personal educational mentor. "
                "Create structured learning paths "
                "for students."
            )
        )

        return result

    except GeminiConfigurationError as error:
        return str(error)

    except Exception as error:
        return (
            "Unable to create the learning path right now.\n\n"
            f"Error: {error}"
        )