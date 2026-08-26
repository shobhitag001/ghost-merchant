import json

from services.transaction_agent import analyze_transactions


# Load transaction data
with open("data/transactions.json", "r") as file:
    transaction_data = json.load(file)


print("=" * 60)
print("       GHOST MERCHANT")
print("      TRANSACTION AGENT")
print("=" * 60)


merchant_id = input("\nEnter Merchant ID: ").strip().upper()


selected_transactions = None

for merchant in transaction_data:

    if merchant["merchant_id"] == merchant_id:
        selected_transactions = merchant["transactions"]
        break


if selected_transactions is None:

    print("\n❌ Merchant transaction data not found.")

else:

    print("\n🔎 Analyzing transactions...")
    print("-" * 60)

    score, reasons = analyze_transactions(
        selected_transactions
    )

    print(f"Transaction Risk Score: {score}/100")

    print("\nEvidence")
    print("-" * 60)

    if reasons:

        for reason in reasons:
            print(f"⚠ {reason}")

    else:

        print("✓ No major transaction anomalies detected.")

    print("\n" + "=" * 60)
    print("Transaction analysis completed.")
    print("=" * 60)