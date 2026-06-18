import joblib

try:
    model = joblib.load("ml_pipeline/model.pkl")
    vectorizer = joblib.load("ml_pipeline/vectorizer.pkl")

except FileNotFoundError:
    raise RuntimeError(
        "Model files not found. Run trainer.py first."
    )

def predict_email(text):

    vec = vectorizer.transform([text])

    prob = model.predict_proba(vec)[0][1]

    risk = int(prob * 100)

    if risk > 70:
        result = "PHISHING"

    elif risk > 40:
        result = "SUSPICIOUS"

    else:
        result = "SAFE"

    return risk, result