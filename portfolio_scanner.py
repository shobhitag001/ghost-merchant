import json

from agents.ghost_graph import ghost_graph


# ============================================================
# LOAD DATA
# ============================================================

with open("data/merchants.json", "r") as file:
    merchants = json.load(file)

with open("data/transactions.json", "r") as file:
    transaction_data = json.load(file)

with open("data/identity_data.json", "r") as file:
    identity_data = json.load(file)


# ============================================================
# INVESTIGATE ONE MERCHANT
# ============================================================

def investigate_merchant(merchant):

    merchant_id = merchant["merchant_id"]


    # --------------------------------------------------------
    # FIND TRANSACTIONS
    # --------------------------------------------------------

    transactions = []

    for item in transaction_data:

        if item["merchant_id"] == merchant_id:

            transactions = item["transactions"]

            break


    # --------------------------------------------------------
    # FIND IDENTITY
    # --------------------------------------------------------

    identity = None

    for item in identity_data:

        if item["merchant_id"] == merchant_id:

            identity = item

            break


    if identity is None:

        return None


    # --------------------------------------------------------
    # INITIAL STATE
    # --------------------------------------------------------

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

        "recommendation": "",

        "ai_report": ""

    }


    # --------------------------------------------------------
    # RUN LANGGRAPH
    # --------------------------------------------------------

    result = ghost_graph.invoke(
        initial_state
    )


    # --------------------------------------------------------
    # RETURN SUMMARY
    # --------------------------------------------------------

    return {

        "merchant_id": merchant_id,

        "business_name": merchant[
            "business_name"
        ],

        "category": merchant[
            "declared_category"
        ],

        "final_score": result[
            "final_score"
        ],

        "final_level": result[
            "final_level"
        ],

        "recommendation": result[
            "recommendation"
        ],

        "connected_merchants": result[
            "connected_merchants"
        ]

    }


# ============================================================
# SCAN ENTIRE PORTFOLIO
# ============================================================

def scan_portfolio():

    results = []


    print("=" * 70)

    print(
        "       GHOST MERCHANT"
    )

    print(
        "       PORTFOLIO RISK SCANNER"
    )

    print("=" * 70)


    print(
        f"\n🔎 Investigating {len(merchants)} merchants...\n"
    )


    for index, merchant in enumerate(
        merchants,
        start=1
    ):

        print(
            f"[{index}/{len(merchants)}] "
            f"Investigating "
            f"{merchant['merchant_id']}..."
        )


        result = investigate_merchant(
            merchant
        )


        if result:

            results.append(
                result
            )


    # --------------------------------------------------------
    # SORT BY RISK
    # --------------------------------------------------------

    results.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )


    return results


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    results = scan_portfolio()


    print("\n")

    print("=" * 70)

    print(
        "              RISK RANKING"
    )

    print("=" * 70)


    for index, result in enumerate(
        results,
        start=1
    ):

        print(
            f"\n#{index}"
        )

        print(
            f"Merchant: "
            f"{result['merchant_id']}"
        )

        print(
            f"Business: "
            f"{result['business_name']}"
        )

        print(
            f"Risk Score: "
            f"{result['final_score']}/100"
        )

        print(
            f"Risk Level: "
            f"{result['final_level']}"
        )

        print(
            f"Recommendation: "
            f"{result['recommendation']}"
        )

        print(
            f"Connected Merchants: "
            f"{result['connected_merchants']}"
        )


    print("\n")

    print("=" * 70)

    print(
        "       PORTFOLIO SCAN COMPLETE"
    )

    print("=" * 70)