import os
import re
import sys
import joblib
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Model paths
NLP_MODEL_PATH = "saved_models/nlp_disease_model.joblib"
NLP_VEC_PATH = "saved_models/nlp_vectorizer.joblib"

ML_MODEL_PATH = "saved_models/ml_disease_model.joblib"
ML_LE_PATH = "saved_models/ml_label_encoder.joblib"
ML_FEAT_PATH = "saved_models/ml_features.joblib"

# NLTK cleaning setup
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


def main():
    # 1. Verify models exist
    nlp_exists = os.path.exists(NLP_MODEL_PATH) and os.path.exists(NLP_VEC_PATH)
    ml_exists = os.path.exists(ML_MODEL_PATH) and os.path.exists(ML_LE_PATH) and os.path.exists(ML_FEAT_PATH)

    if not nlp_exists and not ml_exists:
        print("[Error] No trained model files found.")
        print("Please run nlp_symptom_classifier.py and/or ml_symptom_classifier.py first.")
        sys.exit(1)

    print("Loading packed models...", end="", flush=True)
    
    # Load NLP Model
    nlp_model, nlp_vec = None, None
    if nlp_exists:
        nlp_model = joblib.load(NLP_MODEL_PATH)
        nlp_vec = joblib.load(NLP_VEC_PATH)
        
    # Load ML Model
    ml_model, ml_le, ml_features = None, None, None
    if ml_exists:
        ml_model = joblib.load(ML_MODEL_PATH)
        ml_le = joblib.load(ML_LE_PATH)
        ml_features = joblib.load(ML_FEAT_PATH)
        
    print(" Done!")

    # 2. Get input from CLI argument or prompt interactively
    if len(sys.argv) > 1:
        symptom_text = " ".join(sys.argv[1:])
        run_predictions(symptom_text, nlp_model, nlp_vec, ml_model, ml_le, ml_features)
    else:
        print("\n=== Multi-Model Disease Predictor ===")
        print("Model 1 (NLP): Logistic Regression on raw text descriptions (24 diseases)")
        print("Model 2 (ML) : Random Forest on mapped symptom flags (673+ diseases)")
        print("Type 'exit' or 'quit' to close the program.")
        while True:
            try:
                symptom_text = input("\nEnter symptoms (e.g., 'I have a headache, fever and muscle pain'): ").strip()
                if not symptom_text:
                    continue
                if symptom_text.lower() in ["exit", "quit"]:
                    break
                run_predictions(symptom_text, nlp_model, nlp_vec, ml_model, ml_le, ml_features)
            except (KeyboardInterrupt, EOFError):
                print("\nGoodbye!")
                break


def run_predictions(text: str, nlp_model, nlp_vec, ml_model, ml_le, ml_features):
    print("\n" + "=" * 50)
    print(f"Symptoms Entered: '{text}'")
    print("=" * 50)

    # --- 1. NLP PREDICTION ---
    if nlp_model and nlp_vec:
        cleaned = clean_text(text)
        vec = nlp_vec.transform([cleaned])
        nlp_pred = nlp_model.predict(vec)[0]
        nlp_proba = nlp_model.predict_proba(vec).max()
        print("\n[Model 1: NLP Classifier]")
        print(f"  - Cleaned text : '{cleaned}'")
        print(f"  - Predicted    : {nlp_pred}")
        print(f"  - Confidence   : {nlp_proba * 100:.1f}%")
    else:
        print("\n[Model 1: NLP Classifier] - Not trained. Run nlp_symptom_classifier.py.")

    # --- 2. ML PREDICTION ---
    if ml_model and ml_le and ml_features:
        # Map text to binary features list
        text_lower = text.lower()
        ml_input = [0] * len(ml_features)
        detected_symptoms = []

        for i, symptom in enumerate(ml_features):
            # Check for substring match (e.g. 'shortness of breath' in input text)
            if symptom in text_lower:
                ml_input[i] = 1
                detected_symptoms.append(symptom)

        print("\n[Model 2: Structured ML Classifier]")
        if detected_symptoms:
            print(f"  - Mapped Symptoms: {', '.join(detected_symptoms)}")
            
            # Predict using DataFrame with feature names to match training
            input_df = pd.DataFrame([ml_input], columns=ml_features)
            ml_pred_encoded = ml_model.predict(input_df)[0]
            ml_pred = ml_le.inverse_transform([ml_pred_encoded])[0]
            ml_proba = ml_model.predict_proba(input_df).max()
            
            print(f"  - Predicted      : {ml_pred}")
            print(f"  - Confidence     : {ml_proba * 100:.1f}%")
        else:
            print("  - No structured symptoms matched your text.")
            print("    Try using keywords like 'headache', 'fever', 'vomiting', 'cough', or 'shortness of breath'.")
    else:
        print("\n[Model 2: Structured ML Classifier] - Not trained. Run ml_symptom_classifier.py.")
    print("=" * 50)


if __name__ == "__main__":
    main()
