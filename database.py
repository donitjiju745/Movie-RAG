import os

import certifi
from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()

# Use certifi's trusted CA bundle for SSL/TLS connections.
os.environ["SSL_CERT_FILE"] = certifi.where()


class Neo4jDatabase:

    def __init__(self):
        self.uri = os.getenv("NEO4J_URI")
        self.username = os.getenv("NEO4J_USERNAME")
        self.password = os.getenv("NEO4J_PASSWORD")

        if not all([self.uri, self.username, self.password]):
            raise ValueError(
                "Missing Neo4j configuration. "
                "Check NEO4J_URI, NEO4J_USERNAME, "
                "and NEO4J_PASSWORD in .env."
            )

        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.username, self.password),
        )

    def verify_connection(self):
        self.driver.verify_connectivity()
        print("Successfully connected to Neo4j AuraDB!")

    def close(self):
        self.driver.close()
        print("Neo4j connection closed.")


if __name__ == "__main__":

    db = Neo4jDatabase()

    try:
        db.verify_connection()
    finally:
        db.close()