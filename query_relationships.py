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
                MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
                RETURN p.name AS actor,
                       m.title AS movie,
                       m.year AS year
                ORDER BY m.year
                """
            )

            print("\nActor-Movie relationships:")
            print("-" * 50)

            for record in result:
                print(
                    f"Actor: {record['actor']} | "
                    f"Movie: {record['movie']} | "
                    f"Year: {record['year']}"
                )

    finally:
        driver.close()
        print("\nNeo4j connection closed.")


if __name__ == "__main__":
    main()