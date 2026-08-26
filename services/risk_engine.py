def calculate_risk(merchant):
    score = 0
    reasons = []

    # Check website category
    if not merchant["website_category_match"]:
        score += 25
        reasons.append(
            "Website content does not match the declared business category."
        )

    # Check suspicious links
    if merchant["suspicious_links"]:
        score += 25
        reasons.append(
            "Suspicious external links detected."
        )

    # Check unusual night transactions
    if merchant["night_transaction_percentage"] > 50:
        score += 20
        reasons.append(
            "Unusually high percentage of transactions occur at night."
        )

    # Check shared payout account
    if merchant["shared_payout_account"]:
        score += 20
        reasons.append(
            "Merchant shares a payout account with another merchant."
        )

    # Check connected merchants
    if merchant["connected_merchants"] >= 2:
        score += 10
        reasons.append(
            "Merchant is connected to multiple other merchants."
        )

    # Make sure score doesn't exceed 100
    score = min(score, 100)

    # Determine risk level
    if score >= 80:
        risk_level = "CRITICAL"
    elif score >= 60:
        risk_level = "HIGH"
    elif score >= 30:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return score, risk_level, reasons