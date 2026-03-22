from features.url_features import extract_url_features
from features.html_features import extract_html_features


def build_feature_vector(url, html):
    # extract features properly
    url_features = extract_url_features(url)
    html_features = extract_html_features(html, url)

    # merge both
    return {**url_features, **html_features}