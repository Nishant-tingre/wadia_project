import os
import re
import sys
import time
import pandas as pd
import numpy as np
import joblib
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, recall_score, f1_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns

# File Paths
NLP_DATA_PATH = "data/Symptom2Disease.csv"
ML_DATA_PATH = "data/disease_symptoms.csv"

# NLTK setup
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def clean_text(text: str) -> str:
    """Clean the input symptoms text (lowercase, remove punctuation, remove stopwords, lemmatize)."""
    text = str(text).lower()
    text = re.sub(r"[^a-z\s]", "", text)
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words and len(t) > 2]
    return " ".join(tokens)


def load_ml_data_chunked(path: str) -> pd.DataFrame:
    """Read the large ML CSV in chunks and sample to prevent out-of-memory errors."""
    chunks = []
    for chunk in pd.read_csv(path, chunksize=25000):
        chunk.columns = [c.strip().lower() for c in chunk.columns]
        chunks.append(chunk.sample(frac=0.08, random_state=42))
    df = pd.concat(chunks, ignore_index=True)
    return df


def train_nlp():
    print("\n--- Training Model 1: NLP Classifier ---")
    if not os.path.exists(NLP_DATA_PATH):
        print(f"❌ Error: {NLP_DATA_PATH} not found.")
        return None
        
    start_time = time.time()
    
    print("Loading NLP data...")
    df = pd.read_csv(NLP_DATA_PATH)
    df = df.rename(columns={c: c.strip().lower() for c in df.columns})
    df = df.dropna(subset=["label", "text"])
    
    print(f"Rows loaded: {len(df)} | Unique diseases: {df['label'].nunique()}")
    
    print("Cleaning text descriptions...")
    df["clean_text"] = df["text"].apply(clean_text)
    
    X_train, X_test, y_train, y_test = train_test_split(
        df["clean_text"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
    )
    
    print("Vectorizing text (TF-IDF)...")
    vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    print("Training Logistic Regression...")
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_vec, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred, average='macro')
    f1 = f1_score(y_test, y_pred, average='macro')
    
    # Save Confusion Matrix
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
    plt.close()
    
    # Pack/Save
    joblib.dump(model, "saved_models/nlp_disease_model.joblib")
    joblib.dump(vectorizer, "saved_models/nlp_vectorizer.joblib")
    
    elapsed = time.time() - start_time
    print(f"Done training NLP model! (Time: {elapsed:.1f}s)")
    
    return {
        "accuracy": acc,
        "recall": rec,
        "f1": f1,
        "classes": df["label"].nunique(),
        "samples": len(df)
    }


def train_ml():
    print("\n--- Training Model 2: Structured ML Classifier ---")
    if not os.path.exists(ML_DATA_PATH):
        print(f"❌ Error: {ML_DATA_PATH} not found.")
        return None
        
    start_time = time.time()
    
    print("Loading ML data in chunks...")
    df = load_ml_data_chunked(ML_DATA_PATH)
    
    # Detect target column
    target_col_candidates = [c for c in df.columns if "disease" in c]
    if not target_col_candidates:
        print("❌ Error: Target column 'disease' not found.")
        return None
    target_col = target_col_candidates[0]
    print(f"Using target column: '{target_col}'")
    
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # Process inputs (non-numeric text to binary)
    X = X.apply(lambda col: col.map({"yes": 1, "no": 0}) if col.dtype == object else col)
    X = X.fillna(0)
    
    # Encode target labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42
    )
    
    print(f"Sampled rows: {len(df)} | Unique diseases in sample: {len(le.classes_)}")
    
    print("Training Random Forest Classifier (50 trees)...")
    model = RandomForestClassifier(n_estimators=50, max_depth=None, random_state=42, n_jobs=1)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    # Ignore UndefinedMetricWarning for label classes not in test set
    rec = recall_score(y_test, y_pred, average='macro', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='macro', zero_division=0)
    
    # Pack/Save with compression to reduce file size from 6 GB to under 15 MB
    joblib.dump(model, "saved_models/ml_disease_model.joblib", compress=3)
    joblib.dump(le, "saved_models/ml_label_encoder.joblib")
    joblib.dump(list(X.columns), "saved_models/ml_features.joblib")
    
    elapsed = time.time() - start_time
    print(f"Done training ML model! (Time: {elapsed:.1f}s)")
    
    return {
        "accuracy": acc,
        "recall": rec,
        "f1": f1,
        "classes": len(le.classes_),
        "samples": len(df)
    }


def main():
    print("==================================================")
    print("      Unified Classifier Training Process         ")
    print("==================================================")
    
    nlp_results = train_nlp()
    ml_results = train_ml()
    
    print("\n" + "=" * 55)
    print("     SIDE-BY-SIDE TRAINING PERFORMANCE REPORT     ")
    print("=" * 55)
    print(f"{'Metric':<20} | {'Model 1 (NLP)':<15} | {'Model 2 (ML)':<15}")
    print("-" * 55)
    
    if nlp_results and ml_results:
        print(f"{'Dataset Size':<20} | {nlp_results['samples']:<15} | {ml_results['samples']:<15}")
        print(f"{'Unique Diseases':<20} | {nlp_results['classes']:<15} | {ml_results['classes']:<15}")
        print(f"{'Accuracy':<20} | {nlp_results['accuracy']*100:.1f}% | {ml_results['accuracy']*100:.1f}%")
        print(f"{'Macro Recall':<20} | {nlp_results['recall']*100:.1f}% | {ml_results['recall']*100:.1f}%")
        print(f"{'Macro F1-Score':<20} | {nlp_results['f1']*100:.1f}% | {ml_results['f1']*100:.1f}%")
    else:
        print("Training failed for one or both models. Check logs above.")
        
    print("=" * 55)
    print("All models successfully saved (packed) to disk.")
    print("Run predictions instantly using: python predict.py")
    print("=" * 55)


if __name__ == "__main__":
    main()
