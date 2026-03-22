import joblib

model = joblib.load("model.pkl")

print("Feature names expected by model:")
print(model.feature_names_in_)