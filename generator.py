import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY")


client = genai.Client(
    api_key=API_KEY,
    http_options={"api_version": "v1"},
)


def generate_answer(question, context):

    prompt = f"""
You are a helpful movie assistant.

Answer the user's question using ONLY the information
provided in the context below.

If the answer cannot be found in the context,
say that the information is not available.

Context:
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


if __name__ == "__main__":

    question = "Who acted in Inception?"

    context = """
Movie: Inception
Year: 2010
Genre: Sci-Fi
Actors: Leonardo DiCaprio
"""

    answer = generate_answer(question, context)

    print("\nGemini Answer:")
    print("=" * 50)
    print(answer)
    print("=" * 50)