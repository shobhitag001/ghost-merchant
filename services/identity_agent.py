def analyze_identity(identity):

    risk_score = 0

    reasons = []

    # -----------------------------------------
    # GST name check
    # -----------------------------------------

    if not identity["gst_name_match"]:

        risk_score += 30

        reasons.append(
            "Business identity does not match GST information."
        )

    # -----------------------------------------
    # PAN name check
    # -----------------------------------------

    if not identity["pan_name_match"]:

        risk_score += 30

        reasons.append(
            "Business identity does not match PAN information."
        )

    # -----------------------------------------
    # Category check
    # -----------------------------------------

    if not identity["business_category_match"]:

        risk_score += 25

        reasons.append(
            "Registered business category does not match "
            "the declared merchant category."
        )

    # -----------------------------------------
    # Verification check
    # -----------------------------------------

    if not identity["identity_verified"]:

        risk_score += 15

        reasons.append(
            "Merchant identity could not be fully verified."
        )

    # -----------------------------------------
    # Final score
    # -----------------------------------------

    risk_score = min(
        risk_score,
        100
    )

    return risk_score, reasons