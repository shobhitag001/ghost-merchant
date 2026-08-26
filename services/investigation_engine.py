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
# INVESTIGATE MERCHANT
# ============================================================

def investigate_merchant(merchant_id):

    merchant_id = str(merchant_id).strip().upper()

    # ========================================================
    # FIND MERCHANT
    # ========================================================

    merchant = next(
        (
            item
            for item in merchants
            if item.get("merchant_id") == merchant_id
        ),
        None
    )

    if merchant is None:

        return {
            "success": False,
            "message": f"Merchant {merchant_id} not found."
        }

    # ========================================================
    # FIND TRANSACTIONS
    # ========================================================

    transactions = []

    for item in transaction_data:

        if item.get("merchant_id") == merchant_id:

            transactions = item.get(
                "transactions",
                []
            )

            break

    # ========================================================
    # FIND IDENTITY
    # ========================================================

    identity = next(
        (
            item
            for item in identity_data
            if item.get("merchant_id") == merchant_id
        ),
        None
    )

    if identity is None:

        return {
            "success": False,
            "message": (
                f"Identity data for "
                f"{merchant_id} not found."
            )
        }

    # ========================================================
    # INITIAL LANGGRAPH STATE
    # ========================================================

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

    # ========================================================
    # RUN FULL AGENTIC INVESTIGATION
    # ========================================================

    try:

        result = ghost_graph.invoke(
            initial_state
        )

    except Exception as error:

        return {
            "success": False,
            "message": (
                f"Investigation failed for "
                f"{merchant_id}: {error}"
            )
        }

    # ========================================================
    # COMBINE ALL EVIDENCE
    # ========================================================

    evidence = []

    reason_groups = [

        (
            "Merchant",
            result.get(
                "merchant_reasons",
                []
            )
        ),

        (
            "Transaction",
            result.get(
                "transaction_reasons",
                []
            )
        ),

        (
            "Website",
            result.get(
                "website_reasons",
                []
            )
        ),

        (
            "Identity",
            result.get(
                "identity_reasons",
                []
            )
        ),

        (
            "Graph",
            result.get(
                "graph_reasons",
                []
            )
        )

    ]

    for category, reasons in reason_groups:

        for reason in reasons:

            evidence.append(
                f"{category}: {reason}"
            )

    # ========================================================
    # RETURN COMPLETE RESULT
    # ========================================================

    return {

        "success": True,

        # ----------------------------------------------------
        # Merchant
        # ----------------------------------------------------

        "merchant": merchant,

        # ----------------------------------------------------
        # Risk Scores
        # ----------------------------------------------------

        "merchant_score": result.get(
            "merchant_score",
            0
        ),

        "transaction_score": result.get(
            "transaction_score",
            0
        ),

        "website_score": result.get(
            "website_score",
            0
        ),

        "identity_score": result.get(
            "identity_score",
            0
        ),

        "graph_score": result.get(
            "graph_score",
            0
        ),

        # ----------------------------------------------------
        # Final Decision
        # ----------------------------------------------------

        "final_score": result.get(
            "final_score",
            0
        ),

        "final_level": result.get(
            "final_level",
            "UNKNOWN"
        ),

        "recommendation": result.get(
            "recommendation",
            "No recommendation available."
        ),

        # ----------------------------------------------------
        # Evidence
        # ----------------------------------------------------

        "evidence": evidence,

        # ----------------------------------------------------
        # Connected Merchants
        # ----------------------------------------------------

        "connected_merchants": result.get(
            "connected_merchants",
            []
        ),

        # ----------------------------------------------------
        # Individual Reasons
        # ----------------------------------------------------

        "merchant_reasons": result.get(
            "merchant_reasons",
            []
        ),

        "transaction_reasons": result.get(
            "transaction_reasons",
            []
        ),

        "website_reasons": result.get(
            "website_reasons",
            []
        ),

        "identity_reasons": result.get(
            "identity_reasons",
            []
        ),

        "graph_reasons": result.get(
            "graph_reasons",
            []
        ),

        # ----------------------------------------------------
        # AI Investigation Report
        # ----------------------------------------------------

        "ai_report": result.get(
            "ai_report",
            ""
        )

    }