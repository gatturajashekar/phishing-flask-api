def format_response(url, prediction, prob, risk_score, risk_level, features):
    return {
        "url": url,
        "prediction": prediction,
        "confidence": prob,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "features": features
    }