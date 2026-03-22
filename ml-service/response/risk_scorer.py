def calculate_risk(probability, rule_score, features):
    """
    Combine ML + rules + trust signal
    """

    # 🔥 TRUST OVERRIDE (VERY IMPORTANT)
    if features.get("is_trusted_domain") == 1:
        return 10, "LOW"

    # normalize rule score
    rule_norm = min(rule_score, 100) / 100

    # weighted combination
    final_score = (probability * 0.7 + rule_norm * 0.3) * 100

    if final_score >= 70:
        risk_level = "HIGH"
    elif final_score >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return int(final_score), risk_level