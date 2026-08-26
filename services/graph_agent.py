from services.neo4j_service import Neo4jService


def analyze_graph(merchant_id):

    print("🔎 Querying Neo4j graph...")


    # --------------------------------------------------------
    # Connect to Neo4j
    # --------------------------------------------------------

    neo4j = Neo4jService()


    try:

        # ----------------------------------------------------
        # Find connected merchants
        # ----------------------------------------------------

        connections = neo4j.find_connected_merchants(
            merchant_id
        )


        connected_merchants = set()

        relationship_details = []


        # ----------------------------------------------------
        # Process Neo4j results
        # ----------------------------------------------------

        for connection in connections:

            other_merchant = connection["merchant_id"]

            connected_merchants.add(
                other_merchant
            )


            shared_type = connection["shared_type"]


            first_relationship = connection[
                "first_relationship"
            ]


            second_relationship = connection[
                "second_relationship"
            ]


            relationship_details.append(
                f"{other_merchant} shares "
                f"{shared_type} "
                f"({first_relationship})"
            )


        # ----------------------------------------------------
        # Calculate risk
        # ----------------------------------------------------

        number_of_connections = len(
            connected_merchants
        )


        if number_of_connections >= 3:

            risk_score = 80


        elif number_of_connections == 2:

            risk_score = 60


        elif number_of_connections == 1:

            risk_score = 30


        else:

            risk_score = 0


        # ----------------------------------------------------
        # Generate reasons
        # ----------------------------------------------------

        reasons = []


        if connected_merchants:

            reasons.append(
                "Merchant is connected to "
                + str(number_of_connections)
                + " other merchant(s) "
                + "through shared infrastructure."
            )


            reasons.append(
                "Connected merchants: "
                + ", ".join(
                    sorted(connected_merchants)
                )
            )


            # Add detailed relationships

            for detail in relationship_details:

                reasons.append(
                    detail
                )


        else:

            reasons.append(
                "No suspicious merchant connections detected."
            )


        # ----------------------------------------------------
        # Return result
        # ----------------------------------------------------

        return (
            risk_score,
            reasons,
            list(connected_merchants)
        )


    finally:

        # Always close Neo4j connection

        neo4j.close()