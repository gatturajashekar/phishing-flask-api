from flask import Flask, request, jsonify
from flask_cors import CORS

from core.html_fetcher import fetch_html
from features.feature_vector import build_feature_vector
from detection.ml_model import predict_with_model
from detection.rule_engine import apply_rules
from response.risk_scorer import calculate_risk
from response.formatter import format_response

app = Flask(__name__)
CORS(app)  # 🔥 THIS LINE FIXES YOUR PROBLEM


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        url = data["url"]

        # 1. Fetch HTML
        html = fetch_html(url)

        # 2. Extract features
        features = build_feature_vector(url, html)

        print("\n==============================")
        print("FEATURES:", features)

        # 3. ML prediction
        prediction, prob = predict_with_model(features)

        # 4. Rule engine
        rule_score = apply_rules(url, html, features)

        # 5. Risk scoring
        risk_score, risk_level = calculate_risk(prob, rule_score, features)

        # 6. Response
        result = format_response(url, prediction, prob, risk_score, risk_level, features)

        return jsonify(result)

    except Exception as e:
        print("ML ERROR:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return "Advanced Phishing Detection Service Running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)