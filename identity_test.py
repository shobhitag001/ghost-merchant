import json

from services.identity_agent import analyze_identity


# Load identity data

with open(
    "data/identity_data.json",
    "r"
) as file:

    identities = json.load(file)


print("=" * 60)
print("       GHOST MERCHANT")
print("       IDENTITY AGENT")
print("=" * 60)


merchant_id = input(
    "\nEnter Merchant ID: "
).strip().upper()


selected_identity = None


for identity in identities:

    if identity["merchant_id"] == merchant_id:

        selected_identity = identity

        break


if selected_identity is None:

    print("\n❌ Identity data not found.")

else:

    score, reasons = analyze_identity(
        selected_identity
    )

    print("\n")
    print("IDENTITY RISK SCORE")
    print("-" * 60)

    print(
        f"{score}/100"
    )

    print("\nEvidence")
    print("-" * 60)

    if reasons:

        for reason in reasons:

            print(
                "⚠",
                reason
            )

    else:

        print(
            "✓ Identity information appears consistent."
        )

    print("\n" + "=" * 60)