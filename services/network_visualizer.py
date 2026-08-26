import streamlit as st

from streamlit_agraph import agraph, Node, Edge, Config


def display_merchant_network(
    merchant_id,
    connected_merchants
):

    st.markdown("### 🕸️ Merchant Network")

    if not connected_merchants:

        st.success(
            "✓ No connected merchants detected."
        )

        return

    nodes = []
    edges = []

    # --------------------------------------------------------
    # MAIN MERCHANT
    # --------------------------------------------------------

    nodes.append(
        Node(
            id=merchant_id,
            label=merchant_id,
            size=30,
            shape="dot"
        )
    )

    # --------------------------------------------------------
    # CONNECTED MERCHANTS
    # --------------------------------------------------------

    for connected_id in connected_merchants:

        nodes.append(
            Node(
                id=connected_id,
                label=connected_id,
                size=22,
                shape="dot"
            )
        )

        edges.append(
            Edge(
                source=merchant_id,
                target=connected_id
            )
        )

    # --------------------------------------------------------
    # GRAPH CONFIGURATION
    # --------------------------------------------------------

    config = Config(
        width=900,
        height=500,
        directed=True,
        physics=True,
        hierarchical=False,
        nodeHighlightBehavior=True,
        highlightColor="#F7A7A6",
        collapsible=False
    )

    # --------------------------------------------------------
    # DISPLAY GRAPH
    # --------------------------------------------------------

    agraph(
        nodes=nodes,
        edges=edges,
        config=config
    )