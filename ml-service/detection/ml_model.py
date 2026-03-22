import joblib
import pandas as pd

MODEL_PATH = "models/phishing_model.pkl"


class MLPhishingDetector:

    def __init__(self):
        # Load trained model
        self.model = joblib.load(MODEL_PATH)

        # Get expected feature names from model
        self.feature_names = list(self.model.feature_names_in_)

        print("\n✅ MODEL EXPECTS FEATURES:")
        print(self.feature_names)

    def prepare_input(self, features: dict):
        """
        Align input features with model expectations
        """
        row = {}
        missing = []
        extra = []

        # Check missing features
        for name in self.feature_names:
            if name not in features:
                missing.append(name)
            row[name] = features.get(name, 0)

        # Check extra features (not used by model)
        for key in features.keys():
            if key not in self.feature_names:
                extra.append(key)

        if missing:
            print("\n⚠️ MISSING FEATURES (auto-filled with 0):", missing)

        if extra:
            print("\nℹ️ EXTRA FEATURES (ignored by model):", extra)

        # Create DataFrame in correct order
        df = pd.DataFrame([row], columns=self.feature_names)

        return df

    def predict(self, features: dict):
        """
        Run prediction using trained model
        """

        print("\n==============================")
        print("🔍 RAW FEATURES INPUT:")
        print(features)

        # Prepare input
        df = self.prepare_input(features)

        print("\n📊 FINAL INPUT TO MODEL:")
        print(df)

        # Model prediction
        prediction = self.model.predict(df)[0]
        probability = self.model.predict_proba(df)[0][1]

        # Convert to readable label
        label = "phishing" if prediction == 1 else "legitimate"

        print("\n🎯 PREDICTION:", label)
        print("📈 CONFIDENCE:", probability)

        return label, float(probability)


# 🔥 Singleton instance (used by app.py)
detector = MLPhishingDetector()


def predict_with_model(features):
    return detector.predict(features)