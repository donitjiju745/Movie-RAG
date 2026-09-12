import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()


URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")


def main():
    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD),
    )

    try:
        driver.verify_connectivity()
        print("Connected to Neo4j AuraDB!")

        with driver.session() as session:

            result = session.run(
                """
                MATCH (m:Movie)
                RETURN m.title AS title, m.year AS year, m.genre AS genre
                ORDER BY m.year
                """
            )

            print("\nMovies in the database:")
            print("-" * 40)

            for record in result:
                print(
                    f"Title: {record['title']}, "
                    f"Year: {record['year']}, "
                    f"Genre: {record['genre']}"
                )

    finally:
        driver.close()
        print("\nNeo4j connection closed.")


if __name__ == "__main__":
    main()