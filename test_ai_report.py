from services.ai_report_agent import generate_investigation_report


merchant = {
    "merchant_id": "M004",
    "business_name": "Urban Deals",
    "declared_category": "Apparel"
}


report = generate_investigation_report(

    merchant=merchant,

    merchant_score=40,

    merchant_reasons=[
        "Merchant information requires additional verification."
    ],

    transaction_score=70,

    transaction_reasons=[
        "High-value transactions detected during unusual hours."
    ],

    website_score=80,

    website_reasons=[
        "Website content appears inconsistent "
        "with the declared business category."
    ],

    identity_score=30,

    identity_reasons=[
        "Identity information requires additional review."
    ],

    graph_score=60,

    graph_reasons=[
        "Merchant is connected to other merchants "
        "through shared infrastructure.",
        "M008 shares a payout account.",
        "M009 shares a device and payout account."
    ],

    connected_merchants=[
        "M008",
        "M009"
    ],

    final_score=58,

    final_level="MEDIUM",

    recommendation=(
        "MONITOR MERCHANT FOR ADDITIONAL RISK SIGNALS."
    )
)


print("=" * 70)

print("       GHOST MERCHANT")
print("       AI INVESTIGATION REPORT")

print("=" * 70)

print()

print(report)

print()

print("=" * 70)

print("AI REPORT TEST COMPLETE")

print("=" * 70)