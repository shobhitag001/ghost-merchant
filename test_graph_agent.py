from services.graph_agent import analyze_graph


print("=" * 60)

print("       GHOST MERCHANT")

print("       GRAPH AGENT TEST")

print("=" * 60)


merchant_id = "M004"


print(
    f"\n🔎 Investigating merchant: {merchant_id}"
)


score, reasons, connections = analyze_graph(
    merchant_id
)


print("\n📊 GRAPH RISK SCORE:")

print(score)


print("\n📝 RISK REASONS:")

for reason in reasons:

    print(
        " -",
        reason
    )


print("\n🔗 CONNECTED MERCHANTS:")

for merchant in connections:

    print(
        " -",
        merchant
    )


print("\n" + "=" * 60)

print("GRAPH AGENT TEST COMPLETE")

print("=" * 60)