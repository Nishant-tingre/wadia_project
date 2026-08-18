import os
import re
import sys
import joblib
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from flask import Flask, request, jsonify, render_template

# Initialize Flask App
# We specify template_folder and static_folder relative to the project root
app = Flask(
    __name__,
    template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), "../templates")),
    static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), "../static"))
)

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


# Global references for loaded models
models = {
    "nlp_model": None,
    "nlp_vec": None,
    "ml_model": None,
    "ml_le": None,
    "ml_features": None
}


def load_models():
    # Load NLP Model
    if os.path.exists(NLP_MODEL_PATH) and os.path.exists(NLP_VEC_PATH):
        try:
            models["nlp_model"] = joblib.load(NLP_MODEL_PATH)
            models["nlp_vec"] = joblib.load(NLP_VEC_PATH)
            print("Loaded NLP model and vectorizer.")
        except Exception as e:
            print(f"Error loading NLP model: {e}")
            
    # Load ML Model
    if os.path.exists(ML_MODEL_PATH) and os.path.exists(ML_LE_PATH) and os.path.exists(ML_FEAT_PATH):
        try:
            models["ml_model"] = joblib.load(ML_MODEL_PATH)
            models["ml_le"] = joblib.load(ML_LE_PATH)
            models["ml_features"] = joblib.load(ML_FEAT_PATH)
            print("Loaded ML model, label encoder, and features list.")
        except Exception as e:
            print(f"Error loading ML model: {e}")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data or "symptoms" not in data:
        return jsonify({"error": "No symptoms provided"}), 400
        
    symptoms_text = data["symptoms"].strip()
    if not symptoms_text:
        return jsonify({"error": "Empty symptoms string"}), 400

    response = {
        "nlp": {"success": False},
        "ml": {"success": False}
    }

    # 1. Run NLP Prediction
    if models["nlp_model"] and models["nlp_vec"]:
        try:
            cleaned = clean_text(symptoms_text)
            vec = models["nlp_vec"].transform([cleaned])
            nlp_pred = models["nlp_model"].predict(vec)[0]
            nlp_proba = models["nlp_model"].predict_proba(vec).max()
            
            response["nlp"] = {
                "success": True,
                "cleaned_text": cleaned,
                "predicted_disease": nlp_pred,
                "confidence": float(nlp_proba)
            }
        except Exception as e:
            response["nlp"] = {"success": False, "error": str(e)}

    # 2. Run ML Prediction
    if models["ml_model"] and models["ml_le"] and models["ml_features"]:
        try:
            text_lower = symptoms_text.lower()
            ml_input = [0] * len(models["ml_features"])
            detected_symptoms = []

            for i, symptom in enumerate(models["ml_features"]):
                if symptom in text_lower:
                    ml_input[i] = 1
                    detected_symptoms.append(symptom)

            if detected_symptoms:
                input_df = pd.DataFrame([ml_input], columns=models["ml_features"])
                ml_pred_encoded = models["ml_model"].predict(input_df)[0]
                ml_pred = models["ml_le"].inverse_transform([ml_pred_encoded])[0]
                ml_proba = models["ml_model"].predict_proba(input_df).max()

                response["ml"] = {
                    "success": True,
                    "mapped_symptoms": detected_symptoms,
                    "predicted_disease": ml_pred,
                    "confidence": float(ml_proba)
                }
            else:
                response["ml"] = {
                    "success": True,
                    "mapped_symptoms": [],
                    "predicted_disease": None,
                    "confidence": 0.0,
                    "message": "No structured symptoms matched your text description."
                }
        except Exception as e:
            response["ml"] = {"success": False, "error": str(e)}

    return jsonify(response)


if __name__ == "__main__":
    load_models()
    # Run server locally on port 5000
    app.run(host="127.0.0.1", port=5000, debug=True)
