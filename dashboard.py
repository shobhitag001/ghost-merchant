import json
import pandas as pd
import streamlit as st

from services.investigation_engine import investigate_merchant
from services.network_visualizer import display_merchant_network


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Ghost Merchant | Portfolio Risk",
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
        font-weight: 800;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 19px;
        opacity: 0.7;
        margin-bottom: 20px;
    }

    .section-title {
        font-size: 26px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD MERCHANT DATA
# ============================================================

with open("data/merchants.json", "r") as file:
    merchants = json.load(file)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">👻 GHOST MERCHANT</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Agentic OSINT Portfolio Risk Investigator'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "Continuously investigate and rank merchants using "
    "transaction intelligence, website OSINT, identity "
    "analysis and merchant network intelligence."
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Portfolio Controls")

    scan_button = st.button(
        "🔎 Scan Entire Portfolio",
        type="primary",
        use_container_width=True
    )

    st.divider()

    st.markdown("### 🔍 Filters")

    search_text = st.text_input(
        "Search Merchant",
        placeholder="M001 or Urban Deals"
    )

    risk_filter = st.multiselect(
        "Risk Level",
        [
            "CRITICAL",
            "HIGH",
            "MEDIUM",
            "LOW"
        ],
        default=[
            "CRITICAL",
            "HIGH",
            "MEDIUM",
            "LOW"
        ]
    )

    st.divider()

    st.markdown("### 🤖 Investigation Agents")

    st.write("🧾 Merchant Risk Agent")
    st.write("💳 Transaction Agent")
    st.write("🌐 Website OSINT Agent")
    st.write("🪪 Identity Agent")
    st.write("🕸️ Graph Agent")
    st.write("🧠 Final Risk Analyzer")
    st.write("🤖 AI Report Agent")


# ============================================================
# PORTFOLIO SCAN
# ============================================================

if scan_button:

    results = []

    progress = st.progress(0)

    status = st.empty()

    total = len(merchants)

    for index, merchant in enumerate(merchants):

        merchant_id = merchant["merchant_id"]

        status.write(
            f"🔍 Investigating **{merchant_id}** "
            f"({index + 1}/{total})"
        )

        try:

            result = investigate_merchant(
                merchant_id
            )

            if result.get(
                "success",
                False
            ):

                results.append(
                    result
                )

            else:

                st.warning(
                    f"⚠️ {merchant_id}: "
                    f"{result.get('message', 'Failed')}"
                )

        except Exception as error:

            st.warning(
                f"⚠️ {merchant_id} failed: {error}"
            )

        progress.progress(
            (index + 1) / total
        )

    # --------------------------------------------------------
    # SORT BY RISK
    # --------------------------------------------------------

    results.sort(
        key=lambda x: x.get(
            "final_score",
            0
        ),
        reverse=True
    )

    st.session_state.portfolio_results = results

    status.success(
        f"✅ Portfolio scan completed — "
        f"{len(results)} merchants analyzed."
    )


# ============================================================
# DISPLAY PORTFOLIO RESULTS
# ============================================================

if "portfolio_results" not in st.session_state:

    st.info(
        "👈 Click **Scan Entire Portfolio** "
        "from the sidebar to begin."
    )

else:

    results = st.session_state.portfolio_results


    if not results:

        st.error(
            "❌ No merchant investigations were completed."
        )

    else:

        # ====================================================
        # FILTER RESULTS
        # ====================================================

        filtered_results = []

        for result in results:

            merchant = result.get(
                "merchant",
                {}
            )

            merchant_id = merchant.get(
                "merchant_id",
                ""
            )

            business_name = merchant.get(
                "business_name",
                ""
            )

            final_level = result.get(
                "final_level",
                "UNKNOWN"
            )

            search_match = True

            if search_text.strip():

                search_value = (
                    search_text
                    .strip()
                    .lower()
                )

                search_match = (
                    search_value in
                    merchant_id.lower()
                    or
                    search_value in
                    business_name.lower()
                )

            risk_match = (
                final_level in risk_filter
            )

            if search_match and risk_match:

                filtered_results.append(
                    result
                )


        # ====================================================
        # PORTFOLIO OVERVIEW
        # ====================================================

        st.markdown(
            '<div class="section-title">'
            '📊 Portfolio Overview'
            '</div>',
            unsafe_allow_html=True
        )


        total_merchants = len(results)

        critical_count = sum(
            1
            for r in results
            if r.get("final_level") == "CRITICAL"
        )

        high_count = sum(
            1
            for r in results
            if r.get("final_level") == "HIGH"
        )

        medium_count = sum(
            1
            for r in results
            if r.get("final_level") == "MEDIUM"
        )

        low_count = sum(
            1
            for r in results
            if r.get("final_level") == "LOW"
        )


        col1, col2, col3, col4, col5 = st.columns(5)


        with col1:

            st.metric(
                "Total Merchants",
                total_merchants
            )


        with col2:

            st.metric(
                "🔴 Critical",
                critical_count
            )


        with col3:

            st.metric(
                "🟠 High",
                high_count
            )


        with col4:

            st.metric(
                "🟡 Medium",
                medium_count
            )


        with col5:

            st.metric(
                "🟢 Low",
                low_count
            )

        # ============================================================
        # RISK ALERTS
        # ============================================================

        st.markdown(
            '<div class="section-title">'
            '🚨 Risk Alerts'
            '</div>',
            unsafe_allow_html=True
        )

        critical_merchants = [
            r for r in results
            if r.get("final_level") == "CRITICAL"
        ]

        high_risk_merchants = [
            r for r in results
            if r.get("final_level") == "HIGH"
        ]

        if critical_merchants:

            st.error(
                f"🔴 ALERT: {len(critical_merchants)} "
                f"critical-risk merchant(s) detected."
            )

            for result in critical_merchants:

                merchant = result.get(
                    "merchant",
                    {}
                )

                st.write(
                    f"🔴 **{merchant.get('merchant_id', 'Unknown')}** — "
                    f"{merchant.get('business_name', 'Unknown')} — "
                    f"Risk Score: "
                    f"**{result.get('final_score', 0)}/100**"
                )

        elif high_risk_merchants:

            st.warning(
                f"🟠 WARNING: {len(high_risk_merchants)} "
                f"high-risk merchant(s) detected."
            )

        else:

            st.success(
                "🟢 No critical or high-risk merchants detected."
            )

        # ============================================================
        # PORTFOLIO RISK STATISTICS
        # ============================================================

        st.markdown(
            '<div class="section-title">'
            '📊 Portfolio Risk Statistics'
            '</div>',
            unsafe_allow_html=True
        )

        # ------------------------------------------------------------
        # CALCULATE STATISTICS
        # ------------------------------------------------------------

        risk_scores = [
            r.get("final_score", 0)
            for r in results
        ]

        if risk_scores:
            average_risk = round(
                sum(risk_scores) / len(risk_scores),
                2
            )
            highest_risk = max(risk_scores)
            lowest_risk = min(risk_scores)

            highest_merchant = max(
                results,
                key=lambda r: r.get("final_score", 0)
            )
            lowest_merchant = min(
                results,
                key=lambda r: r.get("final_score", 0)
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Average Risk", f"{average_risk}/100")

            with col2:
                st.metric("Highest Risk", f"{highest_risk}/100")

            with col3:
                st.metric("Lowest Risk", f"{lowest_risk}/100")

            with col4:
                st.metric(
                    "High+ Risk Merchants",
                    critical_count + high_count
                )

            highest_merchant_data = highest_merchant.get("merchant", {})
            st.warning(
                f"🚨 **Highest Risk Merchant:** "
                f"{highest_merchant_data.get('merchant_id', 'Unknown')} — "
                f"{highest_merchant_data.get('business_name', 'Unknown')} "
                f"({highest_risk}/100)"
            )

            lowest_merchant_data = lowest_merchant.get("merchant", {})
            st.success(
                f"🟢 **Lowest Risk Merchant:** "
                f"{lowest_merchant_data.get('merchant_id', 'Unknown')} — "
                f"{lowest_merchant_data.get('business_name', 'Unknown')} "
                f"({lowest_risk}/100)"
            )
        else:
            st.info("No risk statistics available.")

        # ====================================================
        # PORTFOLIO RISK STATISTICS
        # ====================================================

        risk_scores = [
            r.get("final_score", 0)
            for r in results
        ]

        average_risk = round(
            sum(risk_scores) / len(risk_scores),
            1
        ) if risk_scores else 0

        highest_risk_result = max(
            results,
            key=lambda r: r.get("final_score", 0)
        ) if results else None

        if highest_risk_result:
            highest_risk_merchant = highest_risk_result.get(
                "merchant",
                {}
            )

            highest_risk_id = highest_risk_merchant.get(
                "merchant_id",
                "Unknown"
            )

            highest_risk_score = highest_risk_result.get(
                "final_score",
                0
            )
        else:
            highest_risk_id = "N/A"
            highest_risk_score = 0

        st.markdown("### 📈 Portfolio Risk Statistics")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Average Risk Score",
                f"{average_risk}/100"
            )

        with col2:
            st.metric(
                "Highest Risk Score",
                f"{highest_risk_score}/100"
            )

        with col3:
            st.metric(
                "Highest-Risk Merchant",
                highest_risk_id
            )


        st.divider()


        # ====================================================
        # FILTERED RESULTS COUNT
        # ====================================================

        st.write(
            f"Showing **{len(filtered_results)}** "
            f"of **{total_merchants}** merchants."
        )


        # ====================================================
        # RISK RANKING TABLE
        # ====================================================

        st.markdown(
            '<div class="section-title">'
            '🚨 Merchant Risk Ranking'
            '</div>',
            unsafe_allow_html=True
        )


        table_data = []


        for rank, result in enumerate(
            filtered_results,
            start=1
        ):

            merchant = result.get(
                "merchant",
                {}
            )

            table_data.append({

                "Rank":
                    rank,

                "Merchant ID":
                    merchant.get(
                        "merchant_id",
                        "Unknown"
                    ),

                "Business":
                    merchant.get(
                        "business_name",
                        "Unknown"
                    ),

                "Category":
                    merchant.get(
                        "declared_category",
                        "Unknown"
                    ),

                "Risk Score":
                    result.get(
                        "final_score",
                        0
                    ),

                "Risk Level":
                    result.get(
                        "final_level",
                        "UNKNOWN"
                    ),

                "Connected Merchants":
                    len(
                        result.get(
                            "connected_merchants",
                            []
                        )
                    )
            })


        dataframe = pd.DataFrame(
            table_data
        )


        if not dataframe.empty:

            st.dataframe(
                dataframe,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.warning(
                "No merchants match the selected filters."
            )


        # ====================================================
        # RISK SCORE CHART
        # ====================================================

        if not dataframe.empty:

            st.markdown(
                '<div class="section-title">'
                '📈 Risk Score Comparison'
                '</div>',
                unsafe_allow_html=True
            )


            chart_data = dataframe[
                [
                    "Merchant ID",
                    "Risk Score"
                ]
            ].set_index(
                "Merchant ID"
            )


            st.bar_chart(
                chart_data
            )

        # ====================================================
        # RISK LEVEL DISTRIBUTION
        # ====================================================

        st.markdown(
            '<div class="section-title">'
            '📊 Risk Level Distribution'
            '</div>',
            unsafe_allow_html=True
        )

        risk_distribution = pd.DataFrame({
            "Risk Level": [
                "CRITICAL",
                "HIGH",
                "MEDIUM",
                "LOW"
            ],
            "Merchants": [
                critical_count,
                high_count,
                medium_count,
                low_count
            ]
        })

        st.bar_chart(
            risk_distribution.set_index(
                "Risk Level"
            )
        )

        # ====================================================
        # RISK DISTRIBUTION
        # ====================================================

        st.markdown(
            '<div class="section-title">'
            '🎯 Portfolio Risk Distribution'
            '</div>',
            unsafe_allow_html=True
        )

        risk_distribution = pd.DataFrame({

            "Risk Level": [
                "CRITICAL",
                "HIGH",
                "MEDIUM",
                "LOW"
            ],

            "Merchants": [
                critical_count,
                high_count,
                medium_count,
                low_count
            ]

        })

        st.bar_chart(
            risk_distribution.set_index(
                "Risk Level"
            )
        )

        st.write(
            "The chart shows how the investigated merchant "
            "portfolio is distributed across different risk levels."
        )

        # ====================================================
        # HIGH-RISK MERCHANTS
        # ====================================================

        st.markdown(
            '<div class="section-title">'
            '🚨 High-Risk Merchants'
            '</div>',
            unsafe_allow_html=True
        )


        high_risk = [

            result

            for result in filtered_results

            if result.get(
                "final_score",
                0
            ) >= 60

        ]


        if high_risk:

            for result in high_risk:

                merchant = result[
                    "merchant"
                ]

                score = result.get(
                    "final_score",
                    0
                )

                level = result.get(
                    "final_level",
                    "UNKNOWN"
                )


                with st.expander(

                    f"🚨 "
                    f"{merchant['merchant_id']} — "
                    f"{merchant['business_name']} — "
                    f"{score}/100 "
                    f"({level})"

                ):

                    col1, col2 = st.columns(2)


                    with col1:

                        st.write(
                            "**Merchant ID:**",
                            merchant[
                                "merchant_id"
                            ]
                        )

                        st.write(
                            "**Business:**",
                            merchant[
                                "business_name"
                            ]
                        )

                        st.write(
                            "**Category:**",
                            merchant[
                                "declared_category"
                            ]
                        )


                    with col2:

                        st.write(
                            "**Risk Score:**",
                            f"{score}/100"
                        )

                        st.write(
                            "**Risk Level:**",
                            level
                        )

                        st.write(
                            "**Recommendation:**",
                            result.get(
                                "recommendation",
                                "N/A"
                            )
                        )


                    connected = result.get(
                        "connected_merchants",
                        []
                    )


                    if connected:

                        st.write(
                            "**Connected Merchants:**"
                        )

                        for connected_id in connected:

                            st.write(
                                f"🔗 {connected_id}"
                            )


        else:

            st.success(
                "🟢 No high-risk merchants "
                "detected in the current filter."
            )


        # ====================================================
        # NETWORK RISK
        # ====================================================

        st.markdown(
            '<div class="section-title">'
            '🕸️ Network Risk'
            '</div>',
            unsafe_allow_html=True
        )


        network_data = []


        for result in filtered_results:

            merchant = result[
                "merchant"
            ]

            connections = result.get(
                "connected_merchants",
                []
            )


            network_data.append({

                "Merchant ID":
                    merchant[
                        "merchant_id"
                    ],

                "Business":
                    merchant[
                        "business_name"
                    ],

                "Connections":
                    len(connections)

            })


        if network_data:

            network_df = pd.DataFrame(
                network_data
            )

            network_df = network_df.sort_values(
                "Connections",
                ascending=False
            )

            st.dataframe(
                network_df,
                use_container_width=True,
                hide_index=True
            )


        # ====================================================
        # MERCHANT DETAIL
        # ====================================================

        st.divider()

        st.markdown(
            '<div class="section-title">'
            '🔎 Merchant Deep Investigation'
            '</div>',
            unsafe_allow_html=True
        )


        merchant_options = [

            (
                result["merchant"]["merchant_id"]
                + " — "
                + result["merchant"]["business_name"]
            )

            for result in filtered_results

        ]


        if merchant_options:

            selected_label = st.selectbox(
                "Select Merchant",
                merchant_options
            )


            selected_index = merchant_options.index(
                selected_label
            )


            selected_result = filtered_results[
                selected_index
            ]


            merchant = selected_result[
                "merchant"
            ]


            # =================================================
            # MERCHANT PROFILE
            # =================================================

            st.markdown(
                "### 🏪 Merchant Profile"
            )


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Merchant ID",
                    merchant[
                        "merchant_id"
                    ]
                )


            with col2:

                st.metric(
                    "Business",
                    merchant[
                        "business_name"
                    ]
                )


            with col3:

                st.metric(
                    "Category",
                    merchant[
                        "declared_category"
                    ]
                )


            # =================================================
            # FINAL RISK
            # =================================================

            st.markdown(
                "### 🚨 Final Risk Assessment"
            )


            final_score = selected_result.get(
                "final_score",
                0
            )

            final_level = selected_result.get(
                "final_level",
                "UNKNOWN"
            )


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Final Risk Score",
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

                st.write(
                    "**Recommended Action**"
                )

                st.info(
                    selected_result.get(
                        "recommendation",
                        "No recommendation available."
                    )
                )


            st.progress(
                min(
                    max(
                        final_score,
                        0
                    ),
                    100
                ) / 100
            )

            # =================================================
            # RISK SCORE INTERPRETATION
            # =================================================

            if final_score >= 80:

                            st.error(
                                f"🔴 Critical Risk — {final_score}/100"
                            )

            elif final_score >= 60:

                            st.warning(
                                f"🟠 High Risk — {final_score}/100"
                            )

            elif final_score >= 30:

                            st.info(
                                f"🟡 Medium Risk — {final_score}/100"
                            )

            else:

                            st.success(
                                f"🟢 Low Risk — {final_score}/100"
                            )


            # =================================================
            # RISK BREAKDOWN
            # =================================================

            st.markdown(
                "### 📊 Risk Score Breakdown"
            )


            col1, col2, col3, col4, col5 = st.columns(5)


            with col1:

                st.metric(
                    "🧾 Merchant",
                    f"{selected_result.get('merchant_score', 0)}/100"
                )


            with col2:

                st.metric(
                    "💳 Transactions",
                    f"{selected_result.get('transaction_score', 0)}/100"
                )


            with col3:

                st.metric(
                    "🌐 Website",
                    f"{selected_result.get('website_score', 0)}/100"
                )


            with col4:

                st.metric(
                    "🪪 Identity",
                    f"{selected_result.get('identity_score', 0)}/100"
                )


            with col5:

                st.metric(
                    "🕸️ Graph",
                    f"{selected_result.get('graph_score', 0)}/100"
                )


            # =================================================
            # CONNECTED MERCHANTS
            # =================================================

            st.markdown(
                "### 🕸️ Connected Merchants"
            )


            connected = selected_result.get(
                "connected_merchants",
                []
            )


            if connected:

                for connected_id in connected:

                    st.info(
                        f"🔗 {connected_id}"
                    )

            else:

                st.success(
                    "No connected merchants detected."
                )


            # =================================================
            # NETWORK VISUALIZATION
            # =================================================

            st.markdown(
                "### 🕸️ Network Visualization"
            )


            display_merchant_network(
                merchant[
                    "merchant_id"
                ],
                connected
            )


            # =================================================
            # AI INVESTIGATION REPORT
            # =================================================

            st.markdown(
                "### 🤖 AI Investigation Report"
            )


            ai_report = selected_result.get(
                "ai_report",
                ""
            )


            if ai_report:

                with st.expander(
                    "📄 View Full AI Investigation Report",
                    expanded=True
                ):

                    st.markdown(
                        ai_report
                    )

            else:

                st.info(
                    "No AI investigation report available."
                )

            # =================================================
            # DOWNLOAD MERCHANT REPORT
            # =================================================

            st.markdown(
                "### 📥 Merchant Investigation Export"
            )

            report_lines = []

            report_lines.append(
                "GHOST MERCHANT - INVESTIGATION REPORT"
            )

            report_lines.append(
                "=" * 60
            )

            report_lines.append(
                f"Merchant ID: {merchant.get('merchant_id', 'N/A')}"
            )

            report_lines.append(
                f"Business: {merchant.get('business_name', 'N/A')}"
            )

            report_lines.append(
                f"Category: {merchant.get('declared_category', 'N/A')}"
            )

            report_lines.append("")

            report_lines.append(
                f"Final Risk Score: {final_score}/100"
            )

            report_lines.append(
                f"Final Risk Level: {final_level}"
            )

            report_lines.append("")

            report_lines.append(
                "RECOMMENDED ACTION"
            )

            report_lines.append(
                selected_result.get(
                    "recommendation",
                    "No recommendation available."
                )
            )

            report_lines.append("")

            report_lines.append(
                "RISK BREAKDOWN"
            )

            report_lines.append(
                f"Merchant Risk: "
                f"{selected_result.get('merchant_score', 0)}/100"
            )

            report_lines.append(
                f"Transaction Risk: "
                f"{selected_result.get('transaction_score', 0)}/100"
            )

            report_lines.append(
                f"Website Risk: "
                f"{selected_result.get('website_score', 0)}/100"
            )

            report_lines.append(
                f"Identity Risk: "
                f"{selected_result.get('identity_score', 0)}/100"
            )

            report_lines.append(
                f"Graph Risk: "
                f"{selected_result.get('graph_score', 0)}/100"
            )

            report_lines.append("")

            report_lines.append(
                "CONNECTED MERCHANTS"
            )

            connected = selected_result.get(
                "connected_merchants",
                []
            )

            if connected:

                for connected_id in connected:

                    report_lines.append(
                        f"- {connected_id}"
                    )

            else:

                report_lines.append(
                    "None detected."
                )

            report_lines.append("")

            report_lines.append(
                "INVESTIGATION EVIDENCE"
            )

            evidence = selected_result.get(
                "evidence",
                []
            )

            if evidence:

                for item in evidence:

                    report_lines.append(
                        f"- {item}"
                    )

            else:

                report_lines.append(
                    "No significant evidence detected."
                )

            report_lines.append("")

            report_lines.append(
                "AI INVESTIGATION REPORT"
            )

            if ai_report:

                report_lines.append(
                    ai_report
                )

            else:

                report_lines.append(
                    "No AI investigation report available."
                )


            merchant_report = "\n".join(
                report_lines
            )


            st.download_button(
                label="⬇️ Download Merchant Investigation Report",
                data=merchant_report,
                file_name=(
                    f"ghost_merchant_"
                    f"{merchant.get('merchant_id', 'report')}_"
                    f"investigation.txt"
                ),
                mime="text/plain",
                use_container_width=True
            )

            # =================================================
            # RISK EXPLAINABILITY
            # =================================================

            st.markdown(
                "### 🔬 Risk Explainability"
            )

            st.write(
                "The following signals contributed to the merchant's "
                "overall risk assessment."
            )

            explainability_data = {

                "Merchant Risk": selected_result.get(
                    "merchant_score",
                    0
                ),

                "Transaction Risk": selected_result.get(
                    "transaction_score",
                    0
                ),

                "Website Risk": selected_result.get(
                    "website_score",
                    0
                ),

                "Identity Risk": selected_result.get(
                    "identity_score",
                    0
                ),

                "Graph Risk": selected_result.get(
                    "graph_score",
                    0
                )

            }


            explainability_df = pd.DataFrame(
                list(
                    explainability_data.items()
                ),
                columns=[
                    "Risk Signal",
                    "Score"
                ]
            )


            st.dataframe(
                explainability_df,
                use_container_width=True,
                hide_index=True
            )


            highest_signal = max(
                explainability_data,
                key=explainability_data.get
            )

            highest_signal_score = explainability_data[
                highest_signal
            ]


            if highest_signal_score >= 80:

                st.error(
                    f"🔴 Strongest Risk Signal: "
                    f"**{highest_signal} — "
                    f"{highest_signal_score}/100**"
                )

            elif highest_signal_score >= 60:

                st.warning(
                    f"🟠 Strongest Risk Signal: "
                    f"**{highest_signal} — "
                    f"{highest_signal_score}/100**"
                )

            elif highest_signal_score >= 30:

                st.info(
                    f"🟡 Strongest Risk Signal: "
                    f"**{highest_signal} — "
                    f"{highest_signal_score}/100**"
                )

            else:

                st.success(
                    f"🟢 Strongest Risk Signal: "
                    f"**{highest_signal} — "
                    f"{highest_signal_score}/100**"
                )

            # =================================================
            # EXECUTIVE RISK SUMMARY
            # =================================================

            st.markdown(
                "### 📋 Executive Risk Summary"
            )

            connected_count = len(
                selected_result.get(
                    "connected_merchants",
                    []
                )
            )

            risk_score = selected_result.get(
                "final_score",
                0
            )

            risk_level = selected_result.get(
                "final_level",
                "UNKNOWN"
            )

            recommendation = selected_result.get(
                "recommendation",
                "No recommendation available."
            )

            # =================================================
            # INVESTIGATION WORKFLOW
            # =================================================

            st.markdown(
                "### 🔄 Investigation Workflow"
            )

            workflow_steps = [
                ("1️⃣", "Merchant Risk Analysis", "Completed"),
                ("2️⃣", "Transaction Analysis", "Completed"),
                ("3️⃣", "Website OSINT Investigation", "Completed"),
                ("4️⃣", "Identity Analysis", "Completed"),
                ("5️⃣", "Merchant Network Analysis", "Completed"),
                ("6️⃣", "Final Risk Assessment", "Completed"),
                ("7️⃣", "AI Investigation Report", "Completed")
            ]

            for icon, step, status in workflow_steps:

                col1, col2, col3 = st.columns(
                    [1, 5, 2]
                )

                with col1:

                    st.write(icon)

                with col2:

                    st.write(
                        f"**{step}**"
                    )

                with col3:

                    st.success(
                        status
                    )

            # -------------------------------------------------
            # RISK DESCRIPTION
            # -------------------------------------------------

            if risk_level == "CRITICAL":

                risk_description = (
                    "This merchant presents a critical level of risk "
                    "and should be escalated for immediate human review."
                )

            elif risk_level == "HIGH":

                risk_description = (
                    "This merchant presents significant risk signals "
                    "and should be prioritized for risk review."
                )

            elif risk_level == "MEDIUM":

                risk_description = (
                    "This merchant presents moderate risk signals "
                    "and should be monitored for additional evidence."
                )

            else:

                risk_description = (
                    "This merchant currently presents relatively low "
                    "risk based on the available investigation signals."
                )


            st.info(
                f"**Risk Assessment:** {risk_description}"
            )


            # -------------------------------------------------
            # SUMMARY METRICS
            # -------------------------------------------------

            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Overall Risk",
                    f"{risk_score}/100"
                )


            with col2:

                st.metric(
                    "Risk Level",
                    risk_level
                )


            with col3:

                st.metric(
                    "Network Connections",
                    connected_count
                )


            # -------------------------------------------------
            # RECOMMENDED ACTION
            # -------------------------------------------------

            st.markdown(
                "**🎯 Recommended Action**"
            )

            st.write(
                recommendation
            )
            
            # =================================================
            # KEY RISK EVIDENCE
            # =================================================

            st.markdown(
                "### ⚠️ Key Risk Evidence"
            )

            all_evidence = selected_result.get(
                "evidence",
                []
            )

            if all_evidence:

                st.write(
                    f"Detected **{len(all_evidence)}** "
                    "investigation signal(s)."
                )

                for evidence in all_evidence:

                    evidence_text = str(evidence)

                    if evidence_text.startswith("Merchant:"):

                        st.warning(
                            "🧾 " + evidence_text
                        )

                    elif evidence_text.startswith("Transaction:"):

                        st.warning(
                            "💳 " + evidence_text
                        )

                    elif evidence_text.startswith("Website:"):

                        st.warning(
                            "🌐 " + evidence_text
                        )

                    elif evidence_text.startswith("Identity:"):

                        st.warning(
                            "🪪 " + evidence_text
                        )

                    elif evidence_text.startswith("Graph:"):

                        st.warning(
                            "🕸️ " + evidence_text
                        )

                    else:

                        st.info(
                            "⚠️ " + evidence_text
                        )

            else:

                st.success(
                    "✓ No significant risk evidence detected."
                )


            # =================================================
            # INVESTIGATION SIGNALS
            # =================================================

            st.markdown(
                "### 🧠 Investigation Signals"
            )


            reason_sections = {

                "🧾 Merchant Risk Signals":
                    "merchant_reasons",

                "💳 Transaction Risk Signals":
                    "transaction_reasons",

                "🌐 Website Risk Signals":
                    "website_reasons",

                "🪪 Identity Risk Signals":
                    "identity_reasons",

                "🕸️ Graph Risk Signals":
                    "graph_reasons"

            }


            for title, key in reason_sections.items():

                with st.expander(title):

                    reasons = selected_result.get(
                        key,
                        []
                    )


                    if reasons:

                        for reason in reasons:

                            st.write(
                                "•",
                                reason
                            )

                    else:

                        st.success(
                            "No significant signals detected."
                        )


        else:

            st.info(
                "No merchants available for "
                "deep investigation."
            )


        # ====================================================
        # EXPORT
        # ====================================================

        st.divider()

        st.markdown(
            '<div class="section-title">'
            '📥 Export Portfolio Results'
            '</div>',
            unsafe_allow_html=True
        )


        if not dataframe.empty:

            csv_data = dataframe.to_csv(
                index=False
            )


            st.download_button(

                label="⬇️ Download Risk Ranking CSV",

                data=csv_data,

                file_name=(
                    "ghost_merchant_risk_ranking.csv"
                ),

                mime="text/csv",

                use_container_width=True

            )

        # ====================================================
        # COMPLETE INVESTIGATION EXPORT
        # ====================================================

        st.markdown(
            "### 📄 Complete Investigation Report"
        )

        detailed_data = []

        for result in results:

            merchant = result.get(
                "merchant",
                {}
            )

            detailed_data.append({

                "Merchant ID":
                    merchant.get(
                        "merchant_id",
                        "Unknown"
                    ),

                "Business":
                    merchant.get(
                        "business_name",
                        "Unknown"
                    ),

                "Category":
                    merchant.get(
                        "declared_category",
                        "Unknown"
                    ),

                "Merchant Risk":
                    result.get(
                        "merchant_score",
                        0
                    ),

                "Transaction Risk":
                    result.get(
                        "transaction_score",
                        0
                    ),

                "Website Risk":
                    result.get(
                        "website_score",
                        0
                    ),

                "Identity Risk":
                    result.get(
                        "identity_score",
                        0
                    ),

                "Graph Risk":
                    result.get(
                        "graph_score",
                        0
                    ),

                "Final Risk Score":
                    result.get(
                        "final_score",
                        0
                    ),

                "Risk Level":
                    result.get(
                        "final_level",
                        "UNKNOWN"
                    ),

                "Recommendation":
                    result.get(
                        "recommendation",
                        "N/A"
                    ),

                "Connected Merchants":
                    ", ".join(
                        result.get(
                            "connected_merchants",
                            []
                        )
                    )

            })


        detailed_df = pd.DataFrame(
            detailed_data
        )


        detailed_csv = detailed_df.to_csv(
            index=False
        )


        st.download_button(

            label="⬇️ Download Complete Investigation CSV",

            data=detailed_csv,

            file_name=(
                "ghost_merchant_complete_investigation.csv"
            ),

            mime="text/csv",

            use_container_width=True

        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Ghost Merchant — Agentic OSINT Risk Investigator"
)