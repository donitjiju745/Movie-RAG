import re


def extract_movie_title(question):
    """
    Extract a movie title from a simple natural-language question.
    """

    question = question.strip()

    patterns = [
        r"who directed (.+?)[?]?$",
        r"who acted in (.+?)[?]?$",
        r"who starred in (.+?)[?]?$",
        r"what genre is (.+?)[?]?$",
        r"what is the genre of (.+?)[?]?$",
        r"what year was (.+?) released[?]?$",
        r"when was (.+?) released[?]?$",
        r"tell me about (.+?)[?]?$",
        r"what is (.+?)[?]?$",
        r"what's (.+?)[?]?$",
        r"information about (.+?)[?]?$",
        r"details about (.+?)[?]?$",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            question,
            re.IGNORECASE,
        )

        if match:
            return match.group(1).strip()

    return question


def detect_intent(question):
    """
    Detect what information the user is requesting.
    """

    question = question.lower().strip()

    if (
        "who acted" in question
        or "who starred" in question
        or "actors" in question
        or "cast" in question
    ):
        return "actors"

    if (
        "what genre" in question
        or "genre of" in question
        or "what is the genre" in question
    ):
        return "genre"

    if (
        "what year" in question
        or "when was" in question
        or "release year" in question
        or "released" in question
    ):
        return "year"

    if "who directed" in question or "director" in question:
        return "director"

    return "general"


if __name__ == "__main__":

    questions = [
        "Who acted in Inception?",
        "Who starred in The Matrix?",
        "What genre is Inception?",
        "What is the genre of The Matrix?",
        "What year was Interstellar released?",
        "When was Inception released?",
        "Who directed Inception?",
        "Tell me about Interstellar",
    ]

    for question in questions:

        movie_title = extract_movie_title(question)
        intent = detect_intent(question)

        print(f"Question: {question}")
        print(f"Movie title: {movie_title}")
        print(f"Intent: {intent}")
        print("-" * 50)