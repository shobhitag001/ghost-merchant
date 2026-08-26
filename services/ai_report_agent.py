import ollama


# ============================================================
# AI INVESTIGATION REPORT AGENT
# ============================================================

def generate_investigation_report(
    merchant,
    merchant_score,
    merchant_reasons,
    transaction_score,
    transaction_reasons,
    website_score,
    website_reasons,
    identity_score,
    identity_reasons,
    graph_score,
    graph_reasons,
    connected_merchants,
    final_score,
    final_level,
    recommendation
):

    # ========================================================
    # PREPARE VERIFIED EVIDENCE
    # ========================================================

    evidence = f"""
MERCHANT INFORMATION

Merchant ID:
{merchant.get("merchant_id", "Unknown")}

Business Name:
{merchant.get("business_name", "Unknown")}

Declared Category:
{merchant.get("declared_category", "Unknown")}


RISK SCORES

Merchant Risk:
{merchant_score}/100

Transaction Risk:
{transaction_score}/100

Website Risk:
{website_score}/100

Identity Risk:
{identity_score}/100

Graph Risk:
{graph_score}/100


MERCHANT RISK REASONS

{merchant_reasons}


TRANSACTION RISK REASONS

{transaction_reasons}


WEBSITE RISK REASONS

{website_reasons}


IDENTITY RISK REASONS

{identity_reasons}


GRAPH RISK REASONS

{graph_reasons}


CONNECTED MERCHANTS

{connected_merchants}


FINAL RISK SCORE

{final_score}/100


FINAL RISK LEVEL

{final_level}


DETERMINISTIC RISK ENGINE RECOMMENDATION

{recommendation}
"""


    # ========================================================
    # AI REPORT INSTRUCTIONS
    # ========================================================

    prompt = f"""
You are the AI Investigation Report Agent in a merchant
risk intelligence system called "Ghost Merchant".

Your task is to produce a professional merchant risk
investigation report using ONLY the verified evidence
provided below.

STRICT RULES:

1. Do NOT invent facts.
2. Do NOT invent dates, timestamps, locations, people,
   companies, transactions, URLs, documents, or events.
3. Do NOT invent additional merchants.
4. Do NOT invent relationships between merchants.
5. Do NOT invent risk signals.
6. Do NOT change any numerical risk score.
7. Do NOT change the final risk level.
8. Do NOT change the deterministic recommendation.
9. Do NOT claim that the merchant committed a crime.
10. Do NOT present assumptions as facts.
11. Clearly distinguish observed evidence from interpretation.
12. If evidence is insufficient, explicitly state:
    "The available evidence is insufficient to determine this."
13. Use concise, professional fintech risk-analysis language.
14. Do not identify yourself as a human analyst.
15. Do not create a report date.
16. Do not add information outside the supplied evidence.

IMPORTANT:

The risk scores and final recommendation were produced by
the Ghost Merchant deterministic risk engine.

Your role is ONLY to explain the supplied evidence clearly
and professionally.

The final risk score is:

{final_score}/100

The final risk level is:

{final_level}

The deterministic recommendation is:

{recommendation}


Use EXACTLY these sections:

## 1. Executive Summary

Summarize the merchant, final risk score, risk level,
and the most important evidence.

Do not introduce new facts.


## 2. Key Risk Signals

List the strongest observed risk signals.

Group them by:

- Merchant
- Transaction
- Website
- Identity
- Graph / Network

Only use supplied evidence.


## 3. Website Findings

Explain the website-related evidence and why it may
represent a risk signal.

Clearly distinguish detected evidence from interpretation.


## 4. Transaction Findings

Explain the transaction-related evidence.

Do not claim fraud merely because a transaction pattern
is unusual.


## 5. Identity Findings

Explain identity-related inconsistencies or verification
signals contained in the evidence.


## 6. Graph / Network Findings

Explain the merchant's connections using ONLY the supplied
connected merchants and graph evidence.

Do not infer relationships that are not explicitly provided.


## 7. Risk Assessment

Explain how the supplied evidence supports the existing
risk classification.

The final score MUST remain:

{final_score}/100

The final risk level MUST remain:

{final_level}


## 8. Recommended Action

Repeat the existing deterministic recommendation:

{recommendation}

You may explain why the recommendation is consistent
with the supplied evidence, but you MUST NOT replace it.


VERIFIED EVIDENCE
=================

{evidence}
"""


    # ========================================================
    # CALL LOCAL GEMMA MODEL
    # ========================================================

    response = ollama.chat(

        model="gemma3",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    # ========================================================
    # RETURN REPORT
    # ========================================================

    return response["message"]["content"]