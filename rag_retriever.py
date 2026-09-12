from database import Neo4jDatabase
from retriever import MovieRetriever
from query_parser import extract_movie_title


def retrieve_from_question(question):

    movie_title = extract_movie_title(question)

    print(f"Detected movie: {movie_title}")

    db = Neo4jDatabase()

    try:
        db.verify_connection()

        retriever = MovieRetriever(db)

        context = retriever.create_context(movie_title)

        return context

    finally:
        db.close()


if __name__ == "__main__":

    question = "Who acted in Inception?"

    context = retrieve_from_question(question)

    print("\nRetrieved Context")
    print("=" * 50)
    print(context)
    print("=" * 50)