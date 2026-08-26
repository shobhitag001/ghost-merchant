from services.graph_agent import analyze_graph


print("=" * 60)
print("       GHOST MERCHANT")
print("       GRAPH AGENT")
print("=" * 60)


merchant_id = input(
    "\nEnter Merchant ID: "
).strip().upper()


score, reasons, connections = analyze_graph(
    merchant_id
)


print("\n")
print("GRAPH RISK SCORE")
print("-" * 60)

print(
    f"{score}/100"
)


print("\nEvidence")
print("-" * 60)


for reason in reasons:

    print(
        "⚠",
        reason
    )


print("\nConnected Merchants:")


if connections:

    for merchant in connections:

        print(
            "•",
            merchant
        )

else:

    print(
        "None"
    )


print("\n" + "=" * 60)