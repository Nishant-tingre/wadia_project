# ⚡ AuraDX Quickstart & Architecture Guide

This guide explains the relationships between the files in the project and provides step-by-step commands to run each component.

---

## 🔗 File Relationships (Data Flow & Architecture)

The project separates data processing, training, model storage, and inference to create a modular, scalable ML system. Here is how the files interact:

```text
                                  +-----------------------+
                                  |     Raw Datasets      |
                                  | (data/ CSV files)     |
                                  +-----------+-----------+
                                              |
                                              v
                                  +-----------------------+
                                  |   Training Scripts    |
                                  | (src/train_all.py)    |
                                  +-----------+-----------+
                                              |
                          +-------------------+-------------------+
                          | (Generates)                           | (Generates)
                          v                                       v
              +-----------------------+               +-----------------------+
              |     Packed Models     |               |    Visual Reports     |
              | (saved_models/*.joblib)|               |    (saved_models/*.png) |
              +-----------+-----------+               +-----------------------+
                          |
                          +-------------------+
                          | (Loads Instantly) | (Loads Instantly)
                          v                   v
              +-----------------------+  +-----------------------+
              |      CLI Predict      |  |    Flask Web App      |
              |   (src/predict.py)    |  |     (src/app.py)      |
              +-----------+-----------+  +-----------+-----------+
                          |                          |
                          v                          v
              +-----------------------+  +-----------------------+
              |   Terminal Output     |  |   Browser Interface   |
              | (Instant Predictions) |  |   (http://127.0.0.1)  |
              +-----------------------+  +-----------------------+
```

### Dependency Mapping:
* **`data/` $\rightarrow$ `src/`**: Raw CSVs serve as inputs to the training scripts.
* **`src/train_all.py` $\rightarrow$ `saved_models/`**: Trains the algorithms and outputs serialized `.joblib` model binaries, encoders, and the confusion matrix plot.
* **`saved_models/` $\rightarrow$ `src/predict.py` & `src/app.py`**: The inference scripts do not train any models. Instead, they read these pre-trained binaries instantly from disk to evaluate your input symptoms.
* **`templates/` & `static/` $\rightarrow$ `src/app.py`**: Web assets provide the layout (HTML), styles (CSS), and user interaction (JavaScript) for the Flask server.

---

## 🚀 Execution Guide (How to Run Each File)

Always run these commands from the **root** folder of your project: `C:\Users\LENOVO\Downloads\project_wadia`.

### 1. Model Training (Unified Run)
* **Command**: 
  ```bash
  python src/train_all.py
  ```
* **Description**: Trains both models side-by-side.
* **Output**: Prints a side-by-side performance comparison matrix in the console. Generates and updates files inside the `saved_models/` folder.

---

### 2. Command-Line Predictions (Instant Output)
* **Command (Single Sentence)**: 
  ```bash
  python src/predict.py "I have a sore throat, runny nose and mild fever"
  ```
* **Command (Interactive Loop)**:
  ```bash
  python src/predict.py
  ```
* **Description**: Instantly evaluates your symptoms using the saved models.
* **Output**: Displays side-by-side predictions and confidence percentages for both the NLP and ML models in the terminal.

---

### 3. Graphical Web Application (Browser Dashboard)
* **Command**: 
  ```bash
  python src/app.py
  ```
* **Description**: Launches a local web server displaying the AuraDX glassmorphic dashboard.
* **Output**: Hosts the website at **[http://127.0.0.1:5000](http://127.0.0.1:5000)**. Open this link in your browser to test predictions interactively on a modern web UI.

---

### 4. Individual Training Scripts (Optional)
If you wish to train or test either model in isolation:
* **Train NLP Classifier only**:
  ```bash
  python src/nlp_symptom_classifier.py
  ```
* **Train ML Classifier only**:
  ```bash
  python src/ml_symptom_classifier.py
  ```
