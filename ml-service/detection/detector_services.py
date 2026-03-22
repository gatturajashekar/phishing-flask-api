from core.input_validator import normalize_url
from core.html_fetcher import fetch_html

from features.url_features import extract_url_features
from features.html_features import extract_html_features
from features.feature_vector import build_feature_vector

from detection.ml_model import MLPhishingDetector
from response.risk_scorer import compute_risk


detector = MLPhishingDetector()


def analyze_url(url):

    url = normalize_url(url)

    html = fetch_html(url)

    url_features = extract_url_features(url)

    feature_vector = url_features
    prediction, probability = detector.predict(feature_vector)

    score, level = compute_risk(probability, prediction)

    result = {
        "url": url,
        "prediction": prediction,
        "probability": round(probability, 3),
        "risk_score": score,
        "risk_level": level
    }

    return result