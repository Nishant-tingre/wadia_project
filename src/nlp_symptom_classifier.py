"""
Part 1: NLP - Predict disease from free-text symptom description
Dataset: Symptom2Disease (Kaggle)
Download: https://www.kaggle.com/datasets/niyarrbarman/symptom2disease
Save the CSV as: data/Symptom2Disease.csv  (columns expected: 'label', 'text')

This is a LEARNING / PORTFOLIO project, not a clinical diagnostic tool.
"""

import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# ---- 1. Setup ----
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def clean_text(text: str) -> str:
    """Lowercase, remove punctuation/numbers, remove stopwords, lemmatize."""
    text = str(text).lower()
    text = re.sub(r"[^a-z\s]", "", text)
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words and len(t) > 2]
    return " ".join(tokens)


def load_data(path: str = "data/Symptom2Disease.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    # Standardize expected column names — adjust if your download differs
    df = df.rename(columns={c: c.strip().lower() for c in df.columns})
    if "label" not in df.columns or "text" not in df.columns:
        raise ValueError(f"Expected columns 'label' and 'text', got: {list(df.columns)}")
    df = df.dropna(subset=["label", "text"])
    return df


def main():
    print("Loading data...")
    df = load_data()
    print(f"Rows: {len(df)} | Unique diseases: {df['label'].nunique()}")

    print("Cleaning text...")
    df["clean_text"] = df["text"].apply(clean_text)

    # ---- 2. Split ----
    X_train, X_test, y_train, y_test = train_test_split(
        df["clean_text"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
    )

    # ---- 3. Vectorize ----
    vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # ---- 4. Train ----
    print("Training model...")
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_vec, y_train)

    # ---- 5. Evaluate ----
    y_pred = model.predict(X_test_vec)
    print("\n=== Classification Report ===")
    print(classification_report(y_test, y_pred))

    # Confusion matrix plot
    labels = sorted(df["label"].unique())
    cm = confusion_matrix(y_test, y_pred, labels=labels)
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=False, cmap="Blues", xticklabels=labels, yticklabels=labels)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix - Symptom Text to Disease")
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig("saved_models/confusion_matrix_nlp.png", dpi=150)
    print("Saved saved_models/confusion_matrix_nlp.png")

    # ---- 6. Save model for reuse ----
    joblib.dump(model, "saved_models/nlp_disease_model.joblib")
    joblib.dump(vectorizer, "saved_models/nlp_vectorizer.joblib")
    print("Saved model + vectorizer to saved_models/.")

    # ---- 7. Try it on a new example ----
    sample = ["I have a runny nose, sore throat and mild fever since yesterday"]
    sample_clean = [clean_text(s) for s in sample]
    sample_vec = vectorizer.transform(sample_clean)
    prediction = model.predict(sample_vec)[0]
    proba = model.predict_proba(sample_vec).max()
    print(f"\nExample prediction: '{sample[0]}'")
    print(f"-> Predicted disease: {prediction} (confidence: {proba:.2f})")


if __name__ == "__main__":
    main()
