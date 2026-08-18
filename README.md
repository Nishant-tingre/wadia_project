# Disease Symptom Classifier — NLP + ML Portfolio Project

A two-part project combining classic ML and NLP on health/symptom data.
**This is a learning/portfolio project, not a validated clinical or diagnostic
tool.** Real medical predictions require far larger, curated, clinically
validated datasets. Frame it that way in interviews and any write-up.

## Project Structure

```text
project_wadia/
├── data/                             # Dataset CSV files
│   ├── Symptom2Disease.csv
│   └── disease_symptoms.csv
├── src/                              # Script files
│   ├── nlp_symptom_classifier.py     # Individual NLP classifier training script
│   ├── ml_symptom_classifier.py      # Individual ML classifier training script
│   ├── train_all.py                  # Unified side-by-side training script
│   ├── predict.py                    # Side-by-side prediction script (packed models)
│   └── app.py                        # Flask Web Application backend server
├── templates/                        # HTML templates for the Web App
│   └── index.html                    # Dashboard webpage layout
├── static/                           # Static assets for the Web App
│   ├── style.css                     # UI styling (dark theme, glassmorphism)
│   └── app.js                        # Client-side interface interactive logic
├── saved_models/                     # Folder for storing trained/packed files
│   ├── nlp_disease_model.joblib
│   ├── nlp_vectorizer.joblib
│   ├── ml_disease_model.joblib
│   ├── ml_label_encoder.joblib
│   ├── ml_features.joblib
│   └── confusion_matrix_nlp.png
├── requirements.txt                  # Python dependencies list
├── README.md
└── case_study_writeup.md             # Summary comparison case study
```

## Setup

First, install the Python dependencies:
```bash
pip install -r requirements.txt
```

Ensure your datasets are downloaded and placed in the `data/` directory:
1. `data/Symptom2Disease.csv`
2. `data/disease_symptoms.csv`

## Run Training

You can train both the NLP and ML models in a single command, which evaluates both side-by-side and saves their packed `.joblib` files to the `saved_models/` folder:

```bash
python src/train_all.py
```

*Alternatively, you can run `python src/nlp_symptom_classifier.py` or `python src/ml_symptom_classifier.py` to train them individually.*

## Run Predictions (Instant Inference)

Once the models are trained, you can use the packed models to make predictions instantly without retraining:

* **Direct prediction via arguments:**
  ```bash
  python src/predict.py "I have a runny nose, cough, and a mild fever"
  ```

* **Interactive prompt mode:**
  ```bash
  python src/predict.py
  ```

## Web Application Dashboard (Flask UI)

You can launch an interactive web-based dashboard (AURA-DX) that allows you to type symptoms and see side-by-side predictions in a modern web UI:

1. **Launch the web server:**
   ```bash
   python src/app.py
   ```
2. **Open in browser:**
   Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.

## Suggested next steps (to make this stand out further)

1. **Upgrade the NLP model**: Swap TF-IDF + Logistic Regression for a pretrained biomedical transformer like `emilyalsentzer/Bio_ClinicalBERT` (via HuggingFace `transformers`) for stronger accuracy on medical language.
2. **Add Named Entity Recognition**: Use `scispaCy` (`en_core_sci_sm`) to pull out symptom/condition/medication entities from raw text — a nice second NLP skill to show.
3. **Build a small Streamlit app**: A text box for symptom input $\rightarrow$ predicted disease + confidence + extracted entities. This turns the project into something you can actually demo live in an interview.
4. **Write the case study**: Refer to `case_study_writeup.md` for a comprehensive, portfolio-ready comparison of both approaches.

## Responsible framing (use this in your portfolio write-up)

- State clearly this is a decision-support/triage learning exercise, not a diagnostic system.
- Mention data limitations (dataset size, lack of demographic diversity, self-reported symptom text vs. clinical notes).
- Note that any real deployment would need clinical validation and regulatory review.
