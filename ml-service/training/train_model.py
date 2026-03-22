import pandas as pd
import joblib
import json
import datetime

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from training.dataset_loader import (
    load_phishtank_dataset,
    load_legitimate_dataset
)

from training.feature_dataset_builder import build_feature_dataset


def train():

    print("Loading datasets...")

    phishing_urls = load_phishtank_dataset()
    legit_urls = load_legitimate_dataset()

    phishing_urls = phishing_urls[:8000]
    legit_urls = legit_urls[:8000]

    print("Building phishing feature dataset...")
    phishing_dataset = build_feature_dataset(phishing_urls, 1)

    print("Building legitimate feature dataset...")
    legit_dataset = build_feature_dataset(legit_urls, 0)

    dataset = pd.concat([phishing_dataset, legit_dataset], ignore_index=True)

    X = dataset.drop("label", axis=1)
    y = dataset["label"]

    print("Splitting dataset...")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=42
    )

    print("Training RandomForest model...")

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=16,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print("\nModel Accuracy:", accuracy)

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, predictions))

    print("\nClassification Report:")
    print(classification_report(y_test, predictions))

    # Feature importance
    print("\nFeature Importance:")

    importance = pd.Series(
        model.feature_importances_,
        index=X.columns
    ).sort_values(ascending=False)

    print(importance)

    joblib.dump(model, "models/phishing_model.pkl")
    print("\nModel saved → models/phishing_model.pkl")

    metadata = {
        "model_version": "1.1",
        "algorithm": "RandomForest",
        "n_estimators": 300,
        "max_depth": 16,
        "features_used": len(X.columns),
        "feature_names": list(X.columns),
        "training_samples": len(dataset),
        "training_data": ["PhishTank", "Majestic Million"],
        "training_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "accuracy": float(accuracy)
    }

    with open("models/model_info.json", "w") as f:
        json.dump(metadata, f, indent=4)

    print("Metadata saved → models/model_info.json")


if __name__ == "__main__":
    train()