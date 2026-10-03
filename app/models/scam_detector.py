from pathlib import Path

import joblib

from app.utils.preprocessing import clean_text
from app.utils.risk_signals import detect_risk_signals


BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "scam_model.pkl"
VECTORIZER_PATH = BASE_DIR / "tfidf_vectorizer.pkl"


model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


def detect_scam(text):

    if not isinstance(text, str):
        raise ValueError("Message must be text.")

    text = text.strip()

    if not text:
        raise ValueError("Message cannot be empty.")

    # -----------------------------
    # MACHINE LEARNING ANALYSIS
    # -----------------------------

    cleaned_text = clean_text(text)

    text_vector = vectorizer.transform([cleaned_text])

    prediction = model.predict(text_vector)[0]

    probabilities = model.predict_proba(text_vector)[0]

    scam_probability = float(probabilities[1] * 100)


    # -----------------------------
    # RULE-BASED RISK SIGNALS
    # -----------------------------

    risk_signals = detect_risk_signals(text)

    signal_count = sum(
        len(values)
        for values in risk_signals.values()
    )


    # -----------------------------
    # IMPORTANT RISK CATEGORIES
    # -----------------------------

    money_signals = (
        len(risk_signals["money_related"])
        + len(risk_signals["tax_or_fee_related"])
    )

    delivery_signals = len(
        risk_signals["delivery_related"]
    )

    credential_signals = len(
        risk_signals["credential_requests"]
    )

    urgency_signals = len(
        risk_signals["urgency"]
    )

    threat_signals = len(
        risk_signals["threats"]
    )

    link_signals = len(
        risk_signals["links"]
    )


    # -----------------------------
    # RISK SCORE
    # -----------------------------

    risk_score = scam_probability

    # Financial request
    risk_score += money_signals * 12

    # Delivery/package + payment combination
    if money_signals > 0 and delivery_signals > 0:
        risk_score += 25

    # Credential request
    risk_score += credential_signals * 15

    # Urgency
    risk_score += urgency_signals * 5

    # Threats
    risk_score += threat_signals * 8

    # Links
    risk_score += link_signals * 10

    risk_score = min(100, risk_score)


    # -----------------------------
    # RISK LEVEL
    # -----------------------------

    if risk_score >= 70:
        risk_level = "HIGH"

    elif risk_score >= 40:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"


    # -----------------------------
    # FINAL RESULT
    # -----------------------------

    if prediction == 1:
        result = "SCAM"

    elif risk_score >= 70:
        result = "SCAM"

    else:
        result = "LEGITIMATE"


    return {
        "result": result,
        "scam_probability": float(
            round(scam_probability, 2)
        ),
        "risk_score": float(
            round(risk_score, 2)
        ),
        "risk_level": risk_level,
        "risk_signals": risk_signals,
        "risk_signal_count": signal_count,
    }