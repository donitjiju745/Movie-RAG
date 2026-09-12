import os

import certifi
from dotenv import load_dotenv
from google import genai

from database import Neo4jDatabase
from retriever import MovieRetriever
from query_parser import extract_movie_title, detect_intent


load_dotenv()

# Use certifi's trusted CA bundle for SSL/TLS.
os.environ["SSL_CERT_FILE"] = certifi.where()


API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. "
        "Check your .env file."
    )


client = genai.Client(
    api_key=API_KEY,
    http_options={"api_version": "v1"},
)


def generate_answer(question, context, intent):

    prompt = f"""
You are a helpful movie assistant.

Answer the user's question using ONLY the information
provided in the retrieved context.

Detected intent:
{intent}

The context may contain:
- Movie title
- Release year
- Genre
- Actors

Rules:
1. Do not invent information.
2. Do not use outside knowledge.
3. Answer the specific question directly.
4. Use only information present in the context.
5. If the requested information is not present,
   say that the information is not available.
6. Keep the answer concise and clear.

Retrieved context:
{context}

User question:
{question}

Answer:
"""

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
    )

    return interaction.output_text


def answer_question(question):

    movie_title = extract_movie_title(question)
    intent = detect_intent(question)

    print(f"\nDetected movie: {movie_title}")
    print(f"Detected intent: {intent}")

    db = Neo4jDatabase()

    try:

        db.verify_connection()

        retriever = MovieRetriever(db)

        context = retriever.create_context(movie_title)

        print("\nRetrieved Context:")
        print("-" * 60)
        print(context)
        print("-" * 60)

        answer = generate_answer(
            question,
            context,
            intent,
        )

        return answer

    finally:
        db.close()


def main():

    print("=" * 60)
    print("        Movie RAG Assistant")
    print("=" * 60)

    print("\nAvailable movies:")
    print("1. Inception")
    print("2. The Matrix")
    print("3. Interstellar")

    print("\nType 'exit' to quit.")

    while True:

        question = input("\nAsk a movie question: ").strip()

        if question.lower() == "exit":
            print("\nGoodbye!")
            break

        if not question:
            print("Please enter a question.")
            continue

        try:

            answer = answer_question(question)

            print("\nAnswer:")
            print("-" * 60)
            print(answer)
            print("-" * 60)

        except Exception as e:

            print("\nAn error occurred:")
            print(e)


if __name__ == "__main__":
    main()