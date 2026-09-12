import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()


URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")


def create_movie_data(driver):

    movies = [
        {
            "title": "Inception",
            "year": 2010,
            "genre": "Sci-Fi",
            "director": "Christopher Nolan",
        },
        {
            "title": "The Matrix",
            "year": 1999,
            "genre": "Sci-Fi",
            "director": "The Wachowskis",
        },
        {
            "title": "Interstellar",
            "year": 2014,
            "genre": "Sci-Fi",
            "director": "Christopher Nolan",
        },
    ]

    actors = [
        {
            "name": "Leonardo DiCaprio",
            "movie": "Inception",
        },
        {
            "name": "Keanu Reeves",
            "movie": "The Matrix",
        },
        {
            "name": "Matthew McConaughey",
            "movie": "Interstellar",
        },
    ]

    with driver.session() as session:

        # Create movies
        for movie in movies:

            session.run(
                """
                MERGE (m:Movie {title: $title})
                SET m.year = $year
                """,
                title=movie["title"],
                year=movie["year"],
            )

            # Create director
            session.run(
                """
                MERGE (p:Person {name: $director})
                MERGE (m:Movie {title: $title})
                MERGE (p)-[:DIRECTED]->(m)
                """,
                director=movie["director"],
                title=movie["title"],
            )

            # Create genre
            session.run(
                """
                MERGE (g:Genre {name: $genre})
                MERGE (m:Movie {title: $title})
                MERGE (m)-[:HAS_GENRE]->(g)
                """,
                genre=movie["genre"],
                title=movie["title"],
            )

        # Create actors
        for actor in actors:

            session.run(
                """
                MERGE (p:Person {name: $name})
                MERGE (m:Movie {title: $movie})
                MERGE (p)-[:ACTED_IN]->(m)
                """,
                name=actor["name"],
                movie=actor["movie"],
            )


def main():

    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD),
    )

    try:

        driver.verify_connectivity()

        print("Connected to Neo4j AuraDB!")

        create_movie_data(driver)

        print("Movie graph updated successfully!")

    finally:

        driver.close()

        print("Neo4j connection closed.")


if __name__ == "__main__":
    main()