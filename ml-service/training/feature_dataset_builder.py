import pandas as pd
from features.url_features import extract_url_features


def build_feature_dataset(url_list, label):

    dataset = []

    for url in url_list:

        try:
            features = extract_url_features(url)
            features["label"] = label
            dataset.append(features)

        except Exception:
            continue

    return pd.DataFrame(dataset)