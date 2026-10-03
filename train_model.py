import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# Load SMS Spam Collection dataset
data_path = "data/sms_dataset/SMSSpamCollection"

df = pd.read_csv(
    data_path,
    sep="\t",
    header=None,
    names=["label", "message"]
)

print("Dataset loaded successfully!")
print("Total messages:", len(df))

# Convert labels
df["label"] = df["label"].map({
    "ham": 0,
    "spam": 1
})

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    df["message"],
    df["label"],
    test_size=0.2,
    random_state=42,
    stratify=df["label"]
)

# Convert text into numerical features
vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    max_features=5000
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train model
model = LogisticRegression(max_iter=1000)

model.fit(X_train_tfidf, y_train)

# Evaluate
predictions = model.predict(X_test_tfidf)

accuracy = accuracy_score(y_test, predictions)

print("\nModel Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(
    y_test,
    predictions,
    target_names=["Legitimate", "Spam"]
))

# Save model and vectorizer
joblib.dump(model, "app/models/scam_model.pkl")
joblib.dump(vectorizer, "app/models/tfidf_vectorizer.pkl")

print("\nModel saved successfully!")
print("app/models/scam_model.pkl")
print("app/models/tfidf_vectorizer.pkl")