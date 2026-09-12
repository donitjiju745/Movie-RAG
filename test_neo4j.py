import os

import certifi
from dotenv import load_dotenv
from neo4j import GraphDatabase


# Load variables from .env
load_dotenv()

# Use certifi's CA certificate bundle for SSL/TLS
os.environ["SSL_CERT_FILE"] = certifi.where()

uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")


# Check that required environment variables exist
if not all([uri, username, password]):
    raise ValueError(
        "Missing Neo4j configuration. "
        "Check NEO4J_URI, NEO4J_USERNAME, and NEO4J_PASSWORD in .env."
    )


def main() -> None:
    driver = GraphDatabase.driver(
        uri,
        auth=(username, password),
    )

    try:
        driver.verify_connectivity()
        print("Successfully connected to Neo4j AuraDB!")
    finally:
        driver.close()


if __name__ == "__main__":
    main()