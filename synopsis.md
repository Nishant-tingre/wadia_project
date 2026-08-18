# NOWROSJEE WADIA COLLEGE, PUNE – 411 001
### (Affiliated to Savitribai Phule Pune University)
### DEPARTMENT OF COMPUTER SCIENCE & DATA SCIENCE
**ACADEMIC YEAR: 2024–2025 / 2025–2026**  
**PROJECT SYNOPSIS**

---

<!-- ========================================== -->
<!--                  PAGE 1                    -->
<!-- ========================================== -->

## 1. Basic & Team Details

| Field | Details |
| :--- | :--- |
| **Project Title** | **AuraDX: Dual-Engine Symptom Classifier using NLP & Structured Machine Learning** |
| **Domain / Track** | Data Science / Natural Language Processing & Machine Learning |
| **Student Names** | **Nishant, Yash, Suraj** |
| **Roll Number(s)** | **DS2521** |
| **Department** | **Data Science** |
| **College** | **Nowrosjee Wadia College, Pune** |
| **Class** | __________________________________________________ |
| **Faculty / Mentor** | __________________________________________________ *(Vacant - To be assigned by Faculty)* |

---

## 2. Project Description & Problem Statement

### 2.1 Project Description & Background
In healthcare institutions and outpatient clinics, clinical triage is a time-critical first step where patient intake information must be quickly reviewed to prioritize care. Traditional triage relies on manual inquiry by triage nurses or clerical staff, which is susceptible to cognitive fatigue, high inter-observer variability, and severe bottlenecks during peak admission hours. 

**AuraDX** is an AI-assisted Clinical Decision Support System (CDSS) designed to automate initial symptom assessment. The system introduces a dual-paradigm architecture:
1. An **Unstructured NLP Engine** (TF-IDF Vectorization + Logistic Regression) trained on natural language symptom descriptions (`Symptom2Disease`) for conversational patient self-reporting.
2. A **Structured ML Engine** (Random Forest Classifier) trained on high-dimensional binary symptom indicators (`disease_symptoms`) covering 673 unique diseases across 377 symptom flags for clinical checklist intake.

Both models are unified within a responsive Flask-based web dashboard, providing healthcare workers with real-time, side-by-side diagnostic predictions and comparative confidence scores.

### 2.2 Problem Statement
Existing patient assessment processes face significant operational challenges:
* **Noisy & Ambiguous Free-Text**: Patient self-reported descriptions are unstructured, containing non-standard terminology, spelling variations, and narrative noise that classical rule-based algorithms fail to interpret.
* **Extreme Class Cardinality & Imbalance**: Medical checklists encompass hundreds of rare and common conditions. Distinguishing among 600+ diseases with overlapping symptom presentations leads to high class confusion.
* **Lack of Dual-Format Verification**: Prevailing tools evaluate either text or checklists in isolation; there is a lack of integrated solutions capable of cross-verifying free-form narratives against structured symptom vectors simultaneously.

---

## 3. Existing System & Its Limitations

### 3.1 Overview of Existing System
Current triage workflows rely on manual clinical documentation, basic questionnaire forms, or generic single-format internet symptom checkers (such as WebMD or rudimentary keyword search utilities).

### 3.2 Limitations of the Existing System
* **No Dual-Engine Cross-Validation**: Systems operate strictly in one format (either purely structured forms or generic text search), lacking comparative validation across multiple modeling techniques.
* **Vocabulary & Negation Fragility**: Traditional keyword matchers produce frequent false alarms when patient descriptions use colloquial language or indirect symptom expressions.
* **Scalability Bottlenecks**: Manual assessment by triage staff creates severe patient queues during peak outpatient hours.
* **High Memory Footprint in Multi-Class Setups**: Generic multi-class classifiers with hundreds of targets suffer from massive uncompressed model file sizes (6+ GB), making local deployment impractical.

---

## 4. Proposed System & Key Advantages

### 4.1 Proposed System Overview
AuraDX solves these shortcomings by deploying two specialized, complementary machine learning engines into a unified decision-support platform:
* **Engine 1 (Conversational NLP)**: Uses text cleaning, stopword removal, WordNet lemmatization, and TF-IDF feature extraction with Logistic Regression to achieve 95.8% accuracy over 24 distinct illness categories.
* **Engine 2 (Clinical Structured ML)**: Uses an ensemble Random Forest with memory-safe chunked loading and gzip compression (`compress=3`), mapping 377 binary symptom features across 673 target diseases with 81.8% accuracy.
* **Unified Web Dashboard**: A lightweight Flask web application serving a modern, glassmorphic UI for live, sub-second dual inference.

---
<!-- PAGE BREAK (Print Page 1 End) -->
\pagebreak
<!-- ========================================== -->
<!--                  PAGE 2                    -->
<!-- ========================================== -->

## 5. Project Scope & Objectives

### 5.1 Project Scope
* **In-Scope**:
  * Automated natural language preprocessing (NLTK lemmatization, TF-IDF n-grams).
  * High-cardinality multi-class classification on 19,700+ structured records.
  * Model serialization with gzip compression to keep binary files compact (<45 MB).
  * Interactive local web dashboard (`AuraDX`) and command-line interfaces for real-time predictions.
* **Out-of-Scope (Boundaries)**:
  * AuraDX is strictly an academic decision-support prototype; it does not replace certified clinical physicians nor prescribe medications directly.
  * Real-time integration with hospital Electronic Health Record (EHR) databases is reserved for future phases.

### 5.2 Specific Measurable Objectives
1. Design and train a text classification pipeline achieving >90% accuracy on natural language symptom descriptions.
2. Implement memory-efficient chunked training for a 50-tree Random Forest classifier predicting across 670+ diseases.
3. Optimize model persistence via Joblib compression to reduce disk footprint from 6.6 GB to under 45 MB (160x+ reduction).
4. Build and deploy a responsive Flask web interface displaying side-by-side predictions and animated confidence meters.

---

## 6. Key Features & Functional Modules

* **Module 1 — Text Preprocessing & NLP Pipeline**: Cleans conversational input (regex punctuation stripping, lowercasing, stopword elimination, WordNet lemmatization) and builds TF-IDF matrices.
* **Module 2 — High-Cardinality Structured Classifier**: Processes 377 symptom flags, handling sparsity and class imbalance across 673 diseases via ensemble decision trees.
* **Module 3 — Model Serialization & Compression Engine**: Compresses large tree node matrices into compact `.joblib` binaries for sub-second cold starts.
* **Module 4 — Keyword Symptom Mapper**: Scans free-form user text, automatically extracts matching symptom keywords from the 377-feature dictionary, and builds binary feature vectors on the fly.
* **Module 5 — AuraDX Interactive Web Dashboard**: Dark-mode glassmorphic UI featuring symptom suggestion tags, dynamic pill badges, and dual confidence progress bars.

---

## 7. System Requirements

### 7.1 Hardware Requirements
| Component | Minimum Specification | Recommended Specification |
| :--- | :--- | :--- |
| **Processor** | Intel Core i3 / AMD Ryzen 3 (Quad Core) | Intel Core i5 / AMD Ryzen 5 or higher |
| **RAM** | 4 GB | 8 GB – 16 GB DDR4 |
| **Storage** | 1 GB Free Disk Space | SSD with 5 GB Free Space |
| **Input / Output** | Standard Keyboard, Mouse, Monitor | Full HD Display (1920x1080) |

### 7.2 Software & Tool Requirements
| Category | Tools / Technology Used |
| :--- | :--- |
| **Operating System** | Windows 10 / 11 or Linux (Ubuntu 20.04+) |
| **Programming Language** | Python 3.10 / 3.11+ |
| **Web Framework** | Flask 3.0+ (WSGI Local Server) |
| **ML & NLP Libraries** | Scikit-Learn (LogisticRegression, RandomForest), NLTK, Pandas, NumPy |
| **Model Serialization** | Joblib (with gzip level 3 compression) |
| **Data Visualization** | Matplotlib, Seaborn (Confusion Matrix plotting) |
| **Frontend Technologies** | HTML5, Modern Vanilla CSS3 (Glassmorphism), JavaScript (ES6 Fetch API) |
| **IDE & Version Control** | Visual Studio Code, Git / GitHub |

---

## 8. Project Methodology & Phase-Wise Timeline

| Phase | Duration | Activities & Deliverables |
| :---: | :--- | :--- |
| **1. Topic Selection** | Week 1–2 | Formulated clinical decision-support scope; finalized dual-model architecture. |
| **2. Data Collection** | Week 3–4 | Sourced `Symptom2Disease` (text) and `disease_symptoms` (structured) Kaggle datasets. |
| **3. Literature Survey**| Week 5–6 | Surveyed medical NLP benchmarks, multi-class decision trees, and triage workflows. |
| **4. Data Processing** | Week 7–8 | Built text cleaning pipeline, WordNet lemmatization, and chunked CSV sampling logic. |
| **5. Model Development**| Week 9–11 | Trained TF-IDF Logistic Regression model and compressed Random Forest classifier. |
| **6. Testing & Evaluation**| Week 12–13 | Benchmarked Accuracy, Macro Recall, Macro F1, and plotted confusion matrices. |
| **7. Web Development** | Week 14 | Built Flask backend (`app.py`), glassmorphic UI, and live dual-inference endpoints. |
| **8. Documentation** | Week 15 | Prepared academic synopsis, case study report, and technical README documentation. |
| **9. Final Presentation**| Week 16 | Project demonstration, model validation viva, and final submission. |

---

## 9. Academic Endorsement & Signatures

```text
________________________        ________________________        ________________________
   (Student Signature)             (Student Signature)             (Student Signature)
     Nishant DS2521                    Yash DS2521                    Suraj DS2521


________________________                                        ________________________
 (Internal Project Guide)                                        (Head of the Department)
  Department of Data Science                                      Department of Data Science
  Nowrosjee Wadia College, Pune                                   Nowrosjee Wadia College, Pune
```
