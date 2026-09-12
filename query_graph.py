from database import Neo4jDatabase


def main():

    db = Neo4jDatabase()

    try:

        db.verify_connection()

        with db.driver.session() as session:

            result = session.run(
                """
                MATCH (m:Movie)
                OPTIONAL MATCH (actor:Person)-[:ACTED_IN]->(m)
                OPTIONAL MATCH (director:Person)-[:DIRECTED]->(m)
                OPTIONAL MATCH (m)-[:HAS_GENRE]->(genre:Genre)

                RETURN
                    m.title AS movie,
                    m.year AS year,
                    collect(DISTINCT actor.name) AS actors,
                    collect(DISTINCT director.name) AS directors,
                    collect(DISTINCT genre.name) AS genres

                ORDER BY m.year
                """
            )

            print("\nMovie Graph:")
            print("=" * 60)

            for record in result:

                print(f"Movie: {record['movie']}")
                print(f"Year: {record['year']}")
                print(f"Actors: {', '.join(record['actors'])}")
                print(f"Directors: {', '.join(record['directors'])}")
                print(f"Genres: {', '.join(record['genres'])}")

                print("-" * 60)

    finally:

        db.close()


if __name__ == "__main__":
    main()