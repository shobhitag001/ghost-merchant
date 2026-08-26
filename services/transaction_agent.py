def analyze_transactions(transactions):
    """
    Analyze merchant transaction behavior.
    Returns a risk score and evidence.
    """

    if not transactions:
        return 0, ["No transaction data available."]

    risk_score = 0
    reasons = []

    # --------------------------------
    # Calculate average transaction
    # --------------------------------

    amounts = [transaction["amount"] for transaction in transactions]

    average_amount = sum(amounts) / len(amounts)

    # --------------------------------
    # Detect unusually large payments
    # --------------------------------

    large_transactions = [
        amount for amount in amounts
        if amount > average_amount * 3
    ]

    if len(large_transactions) >= 2:
        risk_score += 20

        reasons.append(
            "Multiple transactions are significantly higher "
            "than the merchant's average transaction value."
        )

    # --------------------------------
    # Analyze transaction timing
    # --------------------------------

    night_transactions = [
        transaction
        for transaction in transactions
        if transaction["hour"] < 5 or transaction["hour"] >= 23
    ]

    night_percentage = (
        len(night_transactions) / len(transactions)
    ) * 100

    if night_percentage >= 50:
        risk_score += 30

        reasons.append(
            f"{night_percentage:.0f}% of analyzed transactions "
            "occur during late-night hours."
        )

    # --------------------------------
    # Detect repeated identical amounts
    # --------------------------------

    amount_frequency = {}

    for amount in amounts:
        amount_frequency[amount] = amount_frequency.get(amount, 0) + 1

    repeated_amounts = [
        amount
        for amount, count in amount_frequency.items()
        if count >= 4
    ]

    if repeated_amounts:
        risk_score += 25

        reasons.append(
            "Repeated identical transaction amounts detected: "
            + ", ".join(f"₹{amount}" for amount in repeated_amounts)
        )

    # --------------------------------
    # Calculate final score
    # --------------------------------

    risk_score = min(risk_score, 100)

    return risk_score, reasons