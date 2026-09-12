import os

import certifi
import streamlit as st
from dotenv import load_dotenv
from google import genai

from database import Neo4jDatabase
from retriever import MovieRetriever
from query_parser import extract_movie_title, detect_intent


load_dotenv()

# Use certifi's trusted CA bundle for SSL/TLS.
os.environ["SSL_CERT_FILE"] = certifi.where()


st.set_page_config(
    page_title="Movie RAG Assistant",
    page_icon="🎬",
    layout="wide",
)


# =========================================================
# Gemini
# =========================================================

def generate_answer(question, context, intent):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. "
            "Check your .env file."
        )

    client = genai.Client(
        api_key=api_key,
        http_options={"api_version": "v1"},
    )

    prompt = f"""
You are a helpful movie assistant.

Answer the user's question using ONLY the retrieved
information provided below.

Detected intent:
{intent}

Retrieved context:
{context}

User question:
{question}

Rules:
1. Use only the retrieved context.
2. Do not invent facts.
3. Answer the specific question directly.
4. If the requested information is not available,
   clearly say that it is not available.
5. Keep the answer concise and easy to understand.

Answer:
"""

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
    )

    return interaction.output_text


# =========================================================
# Page Header
# =========================================================

st.title("🎬 Movie RAG Assistant")

st.write(
    "A Neo4j-powered movie question-answering and "
    "recommendation system using Retrieval-Augmented Generation."
)


# =========================================================
# Sidebar
# =========================================================

with st.sidebar:

    st.header("🎥 Knowledge Graph")

    st.write("**Movies:** 3")
    st.write("**People:** 3")
    st.write("**ACTED_IN:** 3")

    st.divider()

    st.subheader("Available Movies")

    st.write("• Inception")
    st.write("• The Matrix")
    st.write("• Interstellar")

    st.divider()

    st.info(
        "Answers are grounded in information retrieved "
        "from the Neo4j knowledge graph."
    )


# =========================================================
# Application Modes
# =========================================================

mode = st.radio(
    "Choose a feature",
    [
        "🎯 Movie Q&A",
        "🎬 Recommendations",
    ],
    horizontal=True,
)


# =========================================================
# Movie Q&A
# =========================================================

if mode == "🎯 Movie Q&A":

    st.subheader("Ask a Movie Question")

    question = st.text_input(
        "Enter your question",
        placeholder="Example: Who acted in Inception?",
    )

    if st.button(
        "🔍 Ask",
        type="primary",
    ):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            try:

                movie_title = extract_movie_title(
                    question
                )

                intent = detect_intent(
                    question
                )

                st.markdown(
                    "### 🔎 Query Analysis"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Detected Movie",
                        movie_title,
                    )

                with col2:

                    st.metric(
                        "Detected Intent",
                        intent,
                    )

                db = Neo4jDatabase()

                try:

                    db.verify_connection()

                    retriever = MovieRetriever(db)

                    context = retriever.create_context(
                        movie_title
                    )

                    st.markdown(
                        "### 📚 Retrieved Context"
                    )

                    st.code(
                        context,
                        language="text",
                    )

                    if (
                        context
                        == "No relevant movie information "
                           "was found."
                    ):

                        st.warning(
                            "No matching movie information "
                            "was found in the knowledge graph."
                        )

                    else:

                        with st.spinner(
                            "Generating grounded answer..."
                        ):

                            answer = generate_answer(
                                question,
                                context,
                                intent,
                            )

                        st.markdown(
                            "### 🤖 Answer"
                        )

                        st.success(answer)

                finally:

                    db.close()

            except Exception as e:

                st.error(
                    f"An error occurred: {e}"
                )


# =========================================================
# Recommendations
# =========================================================

else:

    st.subheader(
        "🎬 Movie Recommendations"
    )

    selected_movie = st.selectbox(
        "Select a movie",
        [
            "Inception",
            "The Matrix",
            "Interstellar",
        ],
    )

    if st.button(
        "✨ Recommend Movies",
        type="primary",
    ):

        try:

            db = Neo4jDatabase()

            try:

                db.verify_connection()

                retriever = MovieRetriever(db)

                recommendations = (
                    retriever.recommend_movies(
                        selected_movie
                    )
                )

            finally:

                db.close()

            if not recommendations:

                st.info(
                    "No similar movies were found."
                )

            else:

                st.markdown(
                    f"### Movies similar to {selected_movie}"
                )

                for index, movie in enumerate(
                    recommendations,
                    start=1,
                ):

                    st.markdown(
                        f"**{index}. "
                        f"{movie['movie']}**"
                    )

                    st.write(
                        f"Year: {movie['year']}  |  "
                        f"Genre: {movie['genre']}"
                    )

                    st.divider()

        except Exception as e:

            st.error(
                f"An error occurred: {e}"
            )


# =========================================================
# Example Questions
# =========================================================

if mode == "🎯 Movie Q&A":

    st.divider()

    st.subheader(
        "💡 Example Questions"
    )

    examples = [
        "Who acted in Inception?",
        "What genre is Inception?",
        "What year was The Matrix released?",
        "Who acted in Interstellar?",
        "Who directed Inception?",
    ]

    for example in examples:

        st.write(
            f"• {example}"
        )