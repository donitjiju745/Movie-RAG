from database import Neo4jDatabase


class MovieRetriever:

    def __init__(self, db):
        self.db = db

    def search_movies(self, search_text):

        search_text = search_text.strip()

        if not search_text:
            return []

        with self.db.driver.session() as session:

            result = session.run(
                """
                MATCH (m:Movie)
                WHERE toLower(trim(m.title))
                      CONTAINS toLower(trim($search_text))

                OPTIONAL MATCH (actor:Person)-[:ACTED_IN]->(m)

                RETURN
                    m.title AS movie,
                    m.year AS year,
                    m.genre AS genre,
                    collect(DISTINCT actor.name) AS actors

                ORDER BY m.year
                LIMIT 5
                """,
                search_text=search_text,
            )

            movies = []

            for record in result:

                movies.append(
                    {
                        "movie": record["movie"],
                        "year": record["year"],
                        "genre": record["genre"],
                        "actors": record["actors"],
                    }
                )

            return movies

    def create_context(self, search_text):

        movies = self.search_movies(search_text)

        if not movies:
            return "No relevant movie information was found."

        context_parts = []

        for movie in movies:

            actors = [
                actor
                for actor in movie["actors"]
                if actor
            ]

            actor_text = (
                ", ".join(actors)
                if actors
                else "No actor information available."
            )

            year = (
                movie["year"]
                if movie["year"] is not None
                else "Year information unavailable."
            )

            genre = (
                movie["genre"]
                if movie["genre"]
                else "Genre information unavailable."
            )

            context = (
                f"Movie: {movie['movie']}\n"
                f"Year: {year}\n"
                f"Genre: {genre}\n"
                f"Actors: {actor_text}"
            )

            context_parts.append(context)

        return "\n\n".join(context_parts)

    def recommend_movies(self, movie_title):

        def get_recommendations(tx):

            result = tx.run(
                """
                MATCH (m:Movie)
                WHERE toLower(trim(m.title))
                      CONTAINS toLower(trim($movie_title))

                WITH m

                MATCH (recommendation:Movie)
                WHERE recommendation.genre = m.genre
                  AND recommendation.title <> m.title

                RETURN
                    recommendation.title AS movie,
                    recommendation.year AS year,
                    recommendation.genre AS genre

                ORDER BY recommendation.year
                LIMIT 5
                """,
                movie_title=movie_title,
            )

            return [
                {
                    "movie": record["movie"],
                    "year": record["year"],
                    "genre": record["genre"],
                }
                for record in result
            ]

        with self.db.driver.session() as session:

            return session.execute_read(
                get_recommendations
            )

if __name__ == "__main__":

    db = Neo4jDatabase()

    try:

        db.verify_connection()

        retriever = MovieRetriever(db)

        recommendations = retriever.recommend_movies(
            "Inception"
        )

        print("\nRecommended Movies:")
        print("=" * 60)

        if not recommendations:

            print("No recommendations found.")

        else:

            for movie in recommendations:

                print(
                    f"{movie['movie']} "
                    f"({movie['year']}) - "
                    f"{movie['genre']}"
                )

        print("=" * 60)

    finally:

        db.close()