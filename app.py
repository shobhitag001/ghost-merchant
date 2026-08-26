import json
import streamlit as st

from agents.ghost_graph import ghost_graph
from services.network_visualizer import display_merchant_network


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Ghost Merchant | AI Risk Investigator",
    page_icon="👻",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 18px;
        opacity: 0.7;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


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
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">👻 GHOST MERCHANT</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Agentic OSINT Risk Investigator'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "Continuously investigate merchants using "
    "transaction intelligence, website OSINT, "
    "identity analysis and graph intelligence."
)

st.divider()


# ============================================================
# MERCHANT SEARCH
# ============================================================

st.markdown(
    '<div class="section-title">🔎 Merchant Investigation</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns([3, 1])

with col1:

    merchant_id = st.text_input(
        "Merchant ID",
        placeholder="Example: M004"
    )

with col2:

    st.write("")

    investigate = st.button(
        "🔍 INVESTIGATE",
        type="primary",
        use_container_width=True
    )


# ============================================================
# RUN INVESTIGATION
# ============================================================

if investigate:

    if not merchant_id:

        st.warning(
            "Please enter a Merchant ID."
        )

        st.stop()


    merchant_id = merchant_id.strip().upper()


    # ========================================================
    # FIND MERCHANT
    # ========================================================

    merchant = None

    for item in merchants:

        if item["merchant_id"] == merchant_id:

            merchant = item

            break


    if merchant is None:

        st.error(
            f"❌ Merchant {merchant_id} was not found."
        )

        st.stop()


    # ========================================================
    # FIND TRANSACTIONS
    # ========================================================

    transactions = []

    for item in transaction_data:

        if item["merchant_id"] == merchant_id:

            transactions = item["transactions"]

            break


    # ========================================================
    # FIND IDENTITY
    # ========================================================

    identity = None

    for item in identity_data:

        if item["merchant_id"] == merchant_id:

            identity = item

            break


    if identity is None:

        st.error(
            "❌ Identity information not found."
        )

        st.stop()


    # ========================================================
    # INITIAL STATE
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
    # RUN LANGGRAPH INVESTIGATION
    # ========================================================

    with st.spinner(
        "🤖 AI agents are investigating the merchant..."
    ):

        try:

            result = ghost_graph.invoke(
                initial_state
            )

        except Exception as error:

            st.error(
                "❌ Investigation failed."
            )

            st.exception(error)

            st.stop()


    st.success(
        "✅ Investigation completed successfully."
    )


    # ========================================================
    # MERCHANT INFORMATION
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '🏪 Merchant Information'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Merchant ID",
            merchant["merchant_id"]
        )

    with col2:

        st.metric(
            "Business",
            merchant["business_name"]
        )

    with col3:

        st.metric(
            "Declared Category",
            merchant["declared_category"]
        )


    # ========================================================
    # FINAL RISK DECISION
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '🚨 Final Risk Decision'
        '</div>',
        unsafe_allow_html=True
    )

    final_score = result["final_score"]

    final_level = result["final_level"]


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "FINAL RISK SCORE",
            f"{final_score}/100"
        )


    with col2:

        if final_level == "CRITICAL":

            st.error(
                "🔴 CRITICAL"
            )

        elif final_level == "HIGH":

            st.error(
                "🟠 HIGH"
            )

        elif final_level == "MEDIUM":

            st.warning(
                "🟡 MEDIUM"
            )

        else:

            st.success(
                "🟢 LOW"
            )


    with col3:

        st.info(
            result["recommendation"]
        )


    # ========================================================
    # RISK SCORE BREAKDOWN
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '📊 Risk Score Breakdown'
        '</div>',
        unsafe_allow_html=True
    )


    col1, col2, col3, col4, col5 = st.columns(5)


    with col1:

        st.metric(
            "Merchant",
            f'{result["merchant_score"]}/100'
        )


    with col2:

        st.metric(
            "Transactions",
            f'{result["transaction_score"]}/100'
        )


    with col3:

        st.metric(
            "Website",
            f'{result["website_score"]}/100'
        )


    with col4:

        st.metric(
            "Identity",
            f'{result["identity_score"]}/100'
        )


    with col5:

        st.metric(
            "Graph",
            f'{result["graph_score"]}/100'
        )


    # ========================================================
    # RISK BARS
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '📈 Risk Indicators'
        '</div>',
        unsafe_allow_html=True
    )


    st.write("Merchant Risk")

    st.progress(
        result["merchant_score"] / 100
    )


    st.write("Transaction Risk")

    st.progress(
        result["transaction_score"] / 100
    )


    st.write("Website Risk")

    st.progress(
        result["website_score"] / 100
    )


    st.write("Identity Risk")

    st.progress(
        result["identity_score"] / 100
    )


    st.write("Graph Risk")

    st.progress(
        result["graph_score"] / 100
    )


    # ========================================================
    # MERCHANT NETWORK
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '🕸️ Merchant Network'
        '</div>',
        unsafe_allow_html=True
    )


    connections = result.get(
        "connected_merchants",
        []
    )


    if connections:

        st.warning(
            f"🔗 {len(connections)} connected merchant(s) detected."
        )


        # ----------------------------------------------------
        # NETWORK VISUALIZATION
        # ----------------------------------------------------

        try:

            selected_node = display_merchant_network(
                merchant_id,
                connections
            )

            if selected_node:

                st.info(
                    f"Selected node: {selected_node}"
                )

        except Exception as error:

            st.warning(
                "Network visualization could not be displayed."
            )

            st.exception(error)


        # ----------------------------------------------------
        # CONNECTED MERCHANTS
        # ----------------------------------------------------

        st.subheader(
            "Connected Merchants"
        )


        cols = st.columns(
            len(connections)
        )


        for index, connected in enumerate(
            connections
        ):

            with cols[index]:

                st.info(
                    f"🔗 {connected}"
                )


    else:

        st.success(
            "✓ No connected merchants detected."
        )


    # ========================================================
    # AI INVESTIGATION REPORT
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '🤖 AI Investigation Report'
        '</div>',
        unsafe_allow_html=True
    )


    report = result.get(
        "ai_report",
        ""
    )


    if report:

        with st.expander(
            "📄 Open Full AI Investigation Report",
            expanded=True
        ):

            st.markdown(
                report
            )

    else:

        st.warning(
            "AI investigation report was not generated."
        )


    # ========================================================
    # INVESTIGATION EVIDENCE
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '🧠 Investigation Evidence'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # MERCHANT EVIDENCE
    # --------------------------------------------------------

    with st.expander(
        "🧾 Merchant Risk Evidence"
    ):

        reasons = result.get(
            "merchant_reasons",
            []
        )


        if reasons:

            for reason in reasons:

                st.write(
                    "⚠️",
                    reason
                )

        else:

            st.write(
                "✓ No significant merchant risk indicators."
            )


    # --------------------------------------------------------
    # TRANSACTION EVIDENCE
    # --------------------------------------------------------

    with st.expander(
        "💳 Transaction Risk Evidence"
    ):

        reasons = result.get(
            "transaction_reasons",
            []
        )


        if reasons:

            for reason in reasons:

                st.write(
                    "⚠️",
                    reason
                )

        else:

            st.write(
                "✓ No significant transaction risk indicators."
            )


    # --------------------------------------------------------
    # WEBSITE EVIDENCE
    # --------------------------------------------------------

    with st.expander(
        "🌐 Website Risk Evidence"
    ):

        reasons = result.get(
            "website_reasons",
            []
        )


        if reasons:

            for reason in reasons:

                st.write(
                    "⚠️",
                    reason
                )

        else:

            st.write(
                "✓ No significant website risk indicators."
            )


    # --------------------------------------------------------
    # IDENTITY EVIDENCE
    # --------------------------------------------------------

    with st.expander(
        "🪪 Identity Risk Evidence"
    ):

        reasons = result.get(
            "identity_reasons",
            []
        )


        if reasons:

            for reason in reasons:

                st.write(
                    "⚠️",
                    reason
                )

        else:

            st.write(
                "✓ No significant identity risk indicators."
            )


    # --------------------------------------------------------
    # GRAPH EVIDENCE
    # --------------------------------------------------------

    with st.expander(
        "🕸️ Graph Risk Evidence"
    ):

        reasons = result.get(
            "graph_reasons",
            []
        )


        if reasons:

            for reason in reasons:

                st.write(
                    "⚠️",
                    reason
                )

        else:

            st.write(
                "✓ No significant graph risk indicators."
            )


    # ========================================================
    # FOOTER
    # ========================================================

    st.divider()

    st.caption(
        "👻 Ghost Merchant | "
        "Agentic OSINT Risk Investigator"
    )