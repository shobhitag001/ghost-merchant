import os

from typing import TypedDict, List

from langgraph.graph import StateGraph, START, END

from services.risk_engine import calculate_risk
from services.transaction_agent import analyze_transactions
from services.website_agent import investigate_website
from services.identity_agent import analyze_identity
from services.graph_agent import analyze_graph
from services.ai_report_agent import generate_investigation_report


# ============================================================
# 1. INVESTIGATION STATE
# ============================================================

class InvestigationState(TypedDict):

    merchant: dict
    transactions: list
    identity: dict

    merchant_score: int
    transaction_score: int
    website_score: int
    identity_score: int
    graph_score: int

    merchant_reasons: List[str]
    transaction_reasons: List[str]
    website_reasons: List[str]
    identity_reasons: List[str]
    graph_reasons: List[str]

    connected_merchants: List[str]

    final_score: int
    final_level: str
    recommendation: str

    ai_report: str


# ============================================================
# 2. MERCHANT RISK AGENT
# ============================================================

def merchant_risk_node(state: InvestigationState):

    print("🧾 Running Merchant Risk Agent...")

    merchant = state["merchant"]

    score, level, reasons = calculate_risk(
        merchant
    )

    return {
        "merchant_score": score,
        "merchant_reasons": reasons
    }


# ============================================================
# 3. TRANSACTION AGENT
# ============================================================

def transaction_node(state: InvestigationState):

    print("💳 Running Transaction Agent...")

    transactions = state["transactions"]

    score, reasons = analyze_transactions(
        transactions
    )

    return {
        "transaction_score": score,
        "transaction_reasons": reasons
    }


# ============================================================
# 4. WEBSITE OSINT AGENT
# ============================================================

def website_node(state: InvestigationState):

    print("🌐 Running Website OSINT Agent...")

    merchant = state["merchant"]

    website_path = os.path.abspath(
        "data/suspicious_merchant.html"
    )

    website_url = (
        "file:///"
        + website_path.replace("\\", "/")
    )

    website_result = investigate_website(
        website_url,
        merchant["declared_category"]
    )

    return {
        "website_score": website_result["risk_score"],
        "website_reasons": website_result["reasons"]
    }


# ============================================================
# 5. IDENTITY AGENT
# ============================================================

def identity_node(state: InvestigationState):

    print("🪪 Running Identity Agent...")

    identity = state["identity"]

    score, reasons = analyze_identity(
        identity
    )

    return {
        "identity_score": score,
        "identity_reasons": reasons
    }


# ============================================================
# 6. GRAPH AGENT
# ============================================================

def graph_node(state: InvestigationState):

    print("🕸️ Running Merchant Graph Agent...")

    merchant = state["merchant"]

    score, reasons, connections = analyze_graph(
        merchant["merchant_id"]
    )

    return {
        "graph_score": score,
        "graph_reasons": reasons,
        "connected_merchants": connections
    }


# ============================================================
# 7. FINAL RISK ANALYZER
# ============================================================

def risk_analyzer_node(state: InvestigationState):

    print("\n🧠 Running Final Risk Analyzer...")

    merchant_score = state["merchant_score"]
    transaction_score = state["transaction_score"]
    website_score = state["website_score"]
    identity_score = state["identity_score"]
    graph_score = state["graph_score"]

    # --------------------------------------------------------
    # WEIGHTED RISK SCORE
    # --------------------------------------------------------

    final_score = round(

        merchant_score * 0.30

        + transaction_score * 0.20

        + website_score * 0.20

        + identity_score * 0.15

        + graph_score * 0.15

    )

    # --------------------------------------------------------
    # RISK LEVEL
    # --------------------------------------------------------

    if final_score >= 80:

        final_level = "CRITICAL"

        recommendation = (
            "ESCALATE FOR HUMAN REVIEW - "
            "Consider temporary settlement restriction."
        )

    elif final_score >= 60:

        final_level = "HIGH"

        recommendation = (
            "FLAG FOR RISK REVIEW."
        )

    elif final_score >= 30:

        final_level = "MEDIUM"

        recommendation = (
            "MONITOR MERCHANT FOR ADDITIONAL RISK SIGNALS."
        )

    else:

        final_level = "LOW"

        recommendation = (
            "NO IMMEDIATE ACTION REQUIRED."
        )

    print(
        f"📊 Final Risk Score: {final_score}/100"
    )

    print(
        f"⚠️ Risk Level: {final_level}"
    )

    return {

        "final_score": final_score,

        "final_level": final_level,

        "recommendation": recommendation

    }


# ============================================================
# 8. AI INVESTIGATION REPORT AGENT
# ============================================================

def ai_report_node(state: InvestigationState):

    print("\n🤖 Running AI Investigation Report Agent...")

    report = generate_investigation_report(

        merchant=state["merchant"],

        merchant_score=state["merchant_score"],
        merchant_reasons=state["merchant_reasons"],

        transaction_score=state["transaction_score"],
        transaction_reasons=state["transaction_reasons"],

        website_score=state["website_score"],
        website_reasons=state["website_reasons"],

        identity_score=state["identity_score"],
        identity_reasons=state["identity_reasons"],

        graph_score=state["graph_score"],
        graph_reasons=state["graph_reasons"],

        connected_merchants=state["connected_merchants"],

        final_score=state["final_score"],
        final_level=state["final_level"],

        recommendation=state["recommendation"]
    )

    return {
        "ai_report": report
    }


# ============================================================
# 9. BUILD LANGGRAPH
# ============================================================

graph = StateGraph(
    InvestigationState
)


# ============================================================
# 10. ADD NODES
# ============================================================

graph.add_node(
    "merchant_risk",
    merchant_risk_node
)

graph.add_node(
    "transaction",
    transaction_node
)

graph.add_node(
    "website",
    website_node
)

graph.add_node(
    "identity",
    identity_node
)

graph.add_node(
    "graph",
    graph_node
)

graph.add_node(
    "risk_analyzer",
    risk_analyzer_node
)

graph.add_node(
    "ai_report",
    ai_report_node
)


# ============================================================
# 11. CONNECT WORKFLOW
# ============================================================

graph.add_edge(
    START,
    "merchant_risk"
)

graph.add_edge(
    "merchant_risk",
    "transaction"
)

graph.add_edge(
    "transaction",
    "website"
)

graph.add_edge(
    "website",
    "identity"
)

graph.add_edge(
    "identity",
    "graph"
)

graph.add_edge(
    "graph",
    "risk_analyzer"
)

graph.add_edge(
    "risk_analyzer",
    "ai_report"
)

graph.add_edge(
    "ai_report",
    END
)


# ============================================================
# 12. COMPILE
# ============================================================

ghost_graph = graph.compile()