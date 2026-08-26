import json

from agents.ghost_graph import ghost_graph


# ============================================================
# LOAD MERCHANT DATA
# ============================================================

with open(
    "data/merchants.json",
    "r"
) as file:

    merchants = json.load(file)


# ============================================================
# LOAD TRANSACTION DATA
# ============================================================

with open(
    "data/transactions.json",
    "r"
) as file:

    transaction_data = json.load(file)


# ============================================================
# LOAD IDENTITY DATA
# ============================================================

with open(
    "data/identity_data.json",
    "r"
) as file:

    identity_data = json.load(file)


# ============================================================
# USER INPUT
# ============================================================

print("=" * 70)

print(
    "             GHOST MERCHANT"
)

print(
    "       AGENTIC RISK INVESTIGATOR"
)

print("=" * 70)


merchant_id = input(
    "\nEnter Merchant ID: "
).strip().upper()


# ============================================================
# FIND MERCHANT
# ============================================================

merchant = None

for item in merchants:

    if item["merchant_id"] == merchant_id:

        merchant = item

        break


if merchant is None:

    print("\n❌ Merchant not found.")

    exit()


# ============================================================
# FIND TRANSACTIONS
# ============================================================

transactions = []

for item in transaction_data:

    if item["merchant_id"] == merchant_id:

        transactions = item["transactions"]

        break


# ============================================================
# FIND IDENTITY
# ============================================================

identity = None

for item in identity_data:

    if item["merchant_id"] == merchant_id:

        identity = item

        break


if identity is None:

    print("\n❌ Identity information not found.")

    exit()


# ============================================================
# INITIAL STATE
# ============================================================

initial_state = {

    "merchant": merchant,

    "transactions": transactions,

    "identity": identity,

    "merchant_score": 0,

    "transaction_score": 0,

    "website_score": 0,

    "identity_score": 0,

    "graph_score": 0,

    "merchant_reasons": [],

    "transaction_reasons": [],

    "website_reasons": [],

    "identity_reasons": [],

    "graph_reasons": [],

    "connected_merchants": [],

    "final_score": 0,

    "final_level": "",

    "recommendation": ""

}


# ============================================================
# RUN AGENTIC WORKFLOW
# ============================================================

print("\n")

print("🚀 Starting autonomous investigation...\n")


result = ghost_graph.invoke(
    initial_state
)


# ============================================================
# FINAL REPORT
# ============================================================

print("\n")
print("=" * 70)

print(
    "             INVESTIGATION REPORT"
)

print("=" * 70)


print("\nMERCHANT")

print("-" * 70)

print(
    "Merchant ID:",
    merchant["merchant_id"]
)

print(
    "Business:",
    merchant["business_name"]
)

print(
    "Declared Category:",
    merchant["declared_category"]
)


print("\nRISK SCORES")

print("-" * 70)

print(
    "Merchant Risk     :",
    result["merchant_score"],
    "/100"
)

print(
    "Transaction Risk  :",
    result["transaction_score"],
    "/100"
)

print(
    "Website Risk      :",
    result["website_score"],
    "/100"
)

print(
    "Identity Risk     :",
    result["identity_score"],
    "/100"
)

print(
    "Graph Risk        :",
    result["graph_score"],
    "/100"
)


print("\nCONNECTED MERCHANTS")

print("-" * 70)


if result["connected_merchants"]:

    for connected in result["connected_merchants"]:

        print(
            "🔗",
            connected
        )

else:

    print("None")


print("\nFINAL DECISION")

print("-" * 70)

print(
    "Risk Score:",
    result["final_score"],
    "/100"
)

print(
    "Risk Level:",
    result["final_level"]
)


print("\nRECOMMENDATION")

print("-" * 70)

print(
    result["recommendation"]
)

# ============================================================
# AI INVESTIGATION REPORT
# ============================================================

print("\n")
print("=" * 70)

print(
    "             AI INVESTIGATION REPORT"
)

print("=" * 70)

print()

print(
    result["ai_report"]
)

print()


print("\n")

print("=" * 70)

print(
    "        GHOST MERCHANT INVESTIGATION COMPLETE"
)

print("=" * 70)