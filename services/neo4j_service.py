from neo4j import GraphDatabase

from config import (
    NEO4J_URI,
    NEO4J_USERNAME,
    NEO4J_PASSWORD
)


class Neo4jService:

    def __init__(self):

        self.driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(
                NEO4J_USERNAME,
                NEO4J_PASSWORD
            )
        )


    def close(self):

        self.driver.close()


    def test_connection(self):

        with self.driver.session(
            database="ghost-merchant-db"
        ) as session:

            result = session.run(
                "RETURN 'Ghost Merchant connected to Neo4j!' AS message"
            )

            record = result.single()

            return record["message"]


    def find_connected_merchants(self, merchant_id):

        query = """
        MATCH (
            m:Merchant {
                merchant_id: $merchant_id
            }
        )-[r1]-(shared)-[r2]-(other:Merchant)

        WHERE other <> m

        RETURN DISTINCT
            other.merchant_id AS merchant_id,
            labels(shared) AS shared_type,
            type(r1) AS first_relationship,
            type(r2) AS second_relationship
        """

        with self.driver.session(
            database="ghost-merchant-db"
        ) as session:

            result = session.run(
                query,
                merchant_id=merchant_id
            )

            connections = []

            for record in result:

                connections.append({
                    "merchant_id": record["merchant_id"],
                    "shared_type": record["shared_type"],
                    "first_relationship": record["first_relationship"],
                    "second_relationship": record["second_relationship"]
                })

            return connections