from services.neo4j_service import Neo4jService


print("=" * 60)

print("       GHOST MERCHANT")

print("       NEO4J GRAPH TEST")

print("=" * 60)


neo4j = Neo4jService()


try:

    message = neo4j.test_connection()

    print("\n✅", message)


    print("\n🔎 Investigating M004...")

    connections = neo4j.find_connected_merchants(
        "M004"
    )


    print("\nCONNECTED MERCHANTS")

    print("-" * 60)


    if connections:

        for connection in connections:

            print(
                "Merchant:",
                connection["merchant_id"]
            )

            print(
                "Shared Through:",
                connection["shared_type"]
            )

            print(
                "Relationship:",
                connection["first_relationship"],
                "→",
                connection["second_relationship"]
            )

            print()


    else:

        print("No connected merchants found.")


except Exception as error:

    print("\n❌ Something went wrong.")

    print("\nError:")

    print(error)


finally:

    neo4j.close()


print("=" * 60)