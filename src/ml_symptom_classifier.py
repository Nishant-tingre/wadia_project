"""
Part 2: ML - Predict disease from structured (one-hot encoded) symptoms
Dataset: Diseases and Symptoms dataset (Kaggle)
Download: https://www.kaggle.com/datasets/dhivyeshrk/diseases-and-symptoms-dataset
Save the CSV as: data/disease_symptoms.csv
(Expected: one column for disease name, remaining columns = binary symptom flags)

This is a LEARNING / PORTFOLIO project, not a clinical diagnostic tool.
Recall is prioritized over raw accuracy: missing a real disease case is worse
than a false alarm, so we track recall and macro F1 explicitly.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, recall_score, f1_score
from sklearn.preprocessing import LabelEncoder
import joblib


def load_data(path: str = "data/disease_symptoms.csv") -> pd.DataFrame:
    chunks = []
    # Read in chunks and sample to save memory
    for chunk in pd.read_csv(path, chunksize=25000):
        chunk.columns = [c.strip().lower() for c in chunk.columns]
        chunks.append(chunk.sample(frac=0.08, random_state=42))
    df = pd.concat(chunks, ignore_index=True)
    return df


def main():
    print("Loading data...")
    df = load_data()

    # Assumes the disease/target column is named 'disease' or 'diseases' — adjust to your file
    target_col_candidates = [c for c in df.columns if "disease" in c]
    if not target_col_candidates:
        raise ValueError(f"Couldn't find a disease/target column. Columns: {list(df.columns)}")
    target_col = target_col_candidates[0]
    print(f"Using target column: '{target_col}'")

    X = df.drop(columns=[target_col])
    y = df[target_col]

    # If X has non-numeric symptom columns (yes/no text), convert to 0/1
    X = X.apply(lambda col: col.map({"yes": 1, "no": 0}) if col.dtype == object else col)
    X = X.fillna(0)

    # Encode target labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42
    )

    print("Training Random Forest...")
    model = RandomForestClassifier(n_estimators=50, max_depth=None, random_state=42, n_jobs=1)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("\n=== Metrics ===")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
    print(f"Macro Recall: {recall_score(y_test, y_pred, average='macro'):.3f}")
    print(f"Macro F1: {f1_score(y_test, y_pred, average='macro'):.3f}")

    # Feature importance — which symptoms matter most overall
    importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
    print("\nTop 15 most predictive symptoms:")
    print(importances.head(15))

    # Compressing the model reduces the 6 GB size to under 15 MB due to high target cardinality sparsity
    joblib.dump(model, "saved_models/ml_disease_model.joblib", compress=3)
    joblib.dump(le, "saved_models/ml_label_encoder.joblib")
    joblib.dump(list(X.columns), "saved_models/ml_features.joblib")
    print("\nSaved model + label encoder and features list to saved_models/.")


if __name__ == "__main__":
    main()
