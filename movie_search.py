from database import Neo4jDatabase


def search_movies(db, search_text):
    with db.driver.session() as session:

        result = session.run(
            """
            MATCH (m:Movie)
            WHERE toLower(m.title) CONTAINS toLower($search_text)

            OPTIONAL MATCH (p:Person)-[:ACTED_IN]->(m)

            RETURN
                m.title AS movie,
                m.year AS year,
                m.genre AS genre,
                collect(p.name) AS actors

            ORDER BY m.year
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


if __name__ == "__main__":

    db = Neo4jDatabase()

    try:
        db.verify_connection()

        search_text = "matrix"

        results = search_movies(db, search_text)

        print(f"\nSearch results for: {search_text}")
        print("-" * 50)

        if results:

            for movie in results:
                print(f"Title: {movie['movie']}")
                print(f"Year: {movie['year']}")
                print(f"Genre: {movie['genre']}")
                print(f"Actors: {', '.join(movie['actors'])}")
                print("-" * 50)

        else:
            print("No movies found.")

    finally:
        db.close()