import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_report():
    doc = Document()

    # Set 1-inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Styles setup
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Calibri'
    font.size = Pt(11)
    font.color.rgb = RGBColor(30, 41, 59)

    # =========================================================================
    # TITLE PAGE
    # =========================================================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("NOWROSJEE WADIA COLLEGE, PUNE – 411 001\n")
    r_inst.font.size = Pt(15)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(14, 116, 144) # Teal / Cyan

    r_inst2 = p_inst.add_run("(Affiliated to Savitribai Phule Pune University - SPPU)\nDEPARTMENT OF COMPUTER SCIENCE & DATA SCIENCE\nACADEMIC YEAR: 2024–2025 / 2025–2026")
    r_inst2.font.size = Pt(11)
    r_inst2.font.bold = True
    r_inst2.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_paragraph("\n" * 2)

    p_proj = doc.add_paragraph()
    p_proj.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_proj = p_proj.add_run("PROJECT DOCUMENTATION REPORT\n\n")
    r_proj.font.size = Pt(13)
    r_proj.font.bold = True
    r_proj.font.color.rgb = RGBColor(100, 116, 139)

    r_title = p_proj.add_run("AuraDX: Dual-Engine Symptom Classifier using NLP & Structured Machine Learning\n")
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(15, 23, 42)

    r_sub = p_proj.add_run("An AI-Assisted Clinical Decision Support System (CDSS) for Outpatient Triage")
    r_sub.font.size = Pt(13)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(71, 85, 105)

    doc.add_paragraph("\n" * 3)

    # Team details table
    tbl_team = doc.add_table(rows=4, cols=2)
    tbl_team.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_team.autofit = False
    
    col_widths = [Inches(2.5), Inches(4.0)]
    for row in tbl_team.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

    team_data = [
        ("Project Roll Number:", "DS2521"),
        ("Project Team Members:", "Nishant, Yash, Suraj"),
        ("Department:", "Department of Data Science"),
        ("Institution:", "Nowrosjee Wadia College, Pune")
    ]

    for ri, (k, v) in enumerate(team_data):
        cell_k = tbl_team.cell(ri, 0)
        cell_v = tbl_team.cell(ri, 1)
        set_cell_background(cell_k, "F1F5F9")
        set_cell_background(cell_v, "FFFFFF")
        
        p_k = cell_k.paragraphs[0]
        r = p_k.add_run(k)
        r.font.bold = True
        r.font.size = Pt(10.5)
        
        p_v = cell_v.paragraphs[0]
        r2 = p_v.add_run(v)
        r2.font.bold = (ri < 2)
        r2.font.size = Pt(10.5)

    doc.add_page_break()

    # =========================================================================
    # EXECUTIVE SUMMARY / ABSTRACT
    # =========================================================================
    h_abs = doc.add_heading("Executive Summary", level=1)
    h_abs.paragraph_format.space_before = Pt(12)
    h_abs.paragraph_format.space_after = Pt(8)

    p_abs = doc.add_paragraph(
        "In healthcare outpatient clinics, clinical triage is the first critical line of assessment to prioritize patient acuity. "
        "Traditional verbal inquiry by triage staff suffers from cognitive fatigue, high inter-observer variability, and severe bottlenecks during peak admission hours. "
        "AuraDX is an AI-assisted Clinical Decision Support System (CDSS) developed to address diagnostic bottlenecks in outpatient intake and patient triage.\n\n"
        "The system introduces a dual-paradigm architecture:\n"
        "1. Unstructured NLP Engine: Employs text sanitation, stopword removal, WordNet lemmatization, and TF-IDF feature extraction (unigram+bigram, 3,000 features) "
        "coupled with multi-class Logistic Regression trained on the Symptom2Disease dataset, achieving 96.0% accuracy across 24 distinct illness categories.\n"
        "2. Structured ML Engine: Employs an ensemble Random Forest classifier (50 decision trees) trained on high-dimensional binary symptom indicators (disease_symptoms dataset) "
        "covering 673 unique diseases across 377 symptom flags, achieving 81.6% accuracy despite extreme class sparsity.\n\n"
        "Through Joblib gzip compression (level 3), the multi-class ensemble model was compressed from 6.6 GB down to 41.4 MB (a 160x reduction). "
        "Both models are served side-by-side through a responsive, dark-mode glassmorphic Flask web dashboard for real-time outpatient triage assistance."
    )
    p_abs.paragraph_format.line_spacing = 1.15

    # =========================================================================
    # SECTION 1: INTRODUCTION & PROBLEM STATEMENT
    # =========================================================================
    doc.add_heading("1. Project Introduction & Problem Statement", level=1)
    
    doc.add_heading("1.1 Background & Motivation", level=2)
    doc.add_paragraph(
        "Clinical triage in emergency departments and outpatient clinics is a time-sensitive intake process that categorizes incoming patients "
        "based on the severity of their symptoms. However, triage workflows in most public healthcare institutions rely heavily on manual inquiry "
        "by triage nurses or clerical staff. During epidemic surges or peak outpatient hours, this manual process introduces significant delays, "
        "inconsistent documentation, and human fatigue.\n\n"
        "Patient intake information arrives in two distinct modalities:\n"
        "• Unstructured free-text narratives: Conversational patient self-reports describing discomfort in subjective language.\n"
        "• Structured medical checklists: Standardized symptom inventories filled out by healthcare workers."
    )

    doc.add_heading("1.2 Problem Statement", level=2)
    doc.add_paragraph(
        "Existing automated symptom checkers (such as WebMD or basic keyword-search portals) face severe limitations:\n"
        "• Vocabulary & Syntactic Fragility: Simple rule-based matchers fail when patients describe symptoms in colloquial language (e.g., 'feeling woozy and dizzy' vs 'vertigo').\n"
        "• Lack of Dual-Engine Cross-Validation: Tools operate strictly in one paradigm—either pure text search or closed checklists—with no secondary model to cross-verify hypotheses.\n"
        "• High Class Cardinality Bottlenecks: Multi-class models scaling across 600+ target diseases produce uncompressed binaries exceeding 6+ GB, making local deployment impractical on hospital workstations."
    )

    doc.add_heading("1.3 Measurable Project Objectives", level=2)
    doc.add_paragraph(
        "1. NLP Accuracy: Train a text classification pipeline achieving >90% accuracy (achieved 96.0%) on natural language symptom descriptions.\n"
        "2. High-Cardinality Triage: Deploy a memory-optimized 50-tree Random Forest mapping 377 symptom features across 673 unique diseases.\n"
        "3. 160x Model Compression: Compress the tree ensemble binary from 6.6 GB to under 45 MB (achieved 41.4 MB) via Joblib gzip level 3 compression.\n"
        "4. Live Web Dashboard: Build and deploy a responsive Flask web application providing sub-second side-by-side diagnostic inference."
    )

    # =========================================================================
    # SECTION 2: EXISTING SYSTEM & LIMITATIONS
    # =========================================================================
    doc.add_heading("2. Existing System vs. Proposed AuraDX System", level=1)

    tbl_comp = doc.add_table(rows=6, cols=3)
    tbl_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_comp.autofit = False

    comp_widths = [Inches(2.0), Inches(2.2), Inches(2.3)]
    for r in tbl_comp.rows:
        for ci, w in enumerate(comp_widths):
            r.cells[ci].width = w

    comp_headers = ["Parameter / Feature", "Existing System", "Proposed AuraDX System"]
    for ci, h in enumerate(comp_headers):
        c = tbl_comp.cell(0, ci)
        set_cell_background(c, "0F172A")
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(10)

    comp_rows = [
        ("Input Modality", "Single format (either text OR checklist)", "Dual format: simultaneously evaluates free-text and 377 binary symptom flags."),
        ("Verification", "No cross-validation; single-model inference", "Side-by-side dual cross-verification with independent confidence meters."),
        ("Disease Coverage", "Limited to 10–25 common conditions", "Covers 673 unique diseases in Engine 2 and 24 common diseases in Engine 1."),
        ("Model Storage Size", "Uncompressed ensembles exceed 6+ GB", "Joblib gzip level 3 compression reduces binary to 41.4 MB (160x reduction)."),
        ("Inference Latency", "Batch delays or slow cloud lookups", "Local sub-second inference (<150 ms) on standard workstation hardware.")
    ]

    for ri, row in enumerate(comp_rows):
        for ci, val in enumerate(row):
            c = tbl_comp.cell(ri + 1, ci)
            set_cell_background(c, "F8FAFC" if ri % 2 == 0 else "FFFFFF")
            p = c.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            if ci == 0:
                r.font.bold = True

    # =========================================================================
    # SECTION 3: ALGORITHMS USED & MATHEMATICAL APPLICATION
    # =========================================================================
    doc.add_heading("3. Algorithms Used & Implementation Details", level=1)

    doc.add_heading("3.1 Natural Language Processing Pipeline (Engine 1)", level=2)
    doc.add_paragraph(
        "• Text Sanitization & Lemmatization: Uses regular expressions to strip non-alphabet characters, converts to lowercase, eliminates NLTK English stopwords, "
        "and applies WordNet lemmatization to extract base morphological lemmas (e.g., 'vomiting' -> 'vomit', 'headaches' -> 'headache').\n\n"
        "• TF-IDF Feature Extraction: Converts cleaned text into a weighted sparse numerical vector. Configured with unigrams and bigrams (ngram_range=(1,2)) "
        "and a vocabulary ceiling of 3,000 features:\n"
        "       TF-IDF(t, d) = TF(t, d) * log( (1 + |D|) / (1 + DF(t)) ) + 1\n\n"
        "• Multi-Class Logistic Regression: Employs multinomial cross-entropy (softmax) with L2 regularization and L-BFGS solver:\n"
        "       P(y = k | x) = exp(w_k * x) / SUM( exp(w_j * x) )\n"
        "Achieved 96.0% accuracy, 96.0% macro recall, and 96.0% macro F1-score across 24 balanced disease categories."
    )

    doc.add_heading("3.2 High-Cardinality Random Forest Classifier (Engine 2)", level=2)
    doc.add_paragraph(
        "• Dynamic Keyword Substring Mapper: Scans user text against a lexicon of 377 clinical symptom names, constructing a 1x377 binary indicator vector (1 = present, 0 = absent).\n\n"
        "• Random Forest Ensemble (50 Decision Trees): Aggregates bootstrap decision trees using the Gini Impurity metric:\n"
        "       Gini = 1 - SUM( p_i^2 )\n"
        "Where p_i is the proportion of samples belonging to disease class i at a given tree split.\n\n"
        "• High Cardinality Scaling: Mapped 377 symptom features across 673 unique diseases, achieving 81.6% accuracy and 76.6% macro recall despite extreme sparsity.\n\n"
        "• Top 5 Predictive Symptoms by Gini Importance:\n"
        "   1. headache (1.88%)   2. vomiting (1.67%)   3. sharp abdominal pain (1.59%)\n"
        "   4. cough (1.41%)      5. sharp chest pain (1.40%)"
    )

    # =========================================================================
    # SECTION 4: DATASET DESCRIPTIONS
    # =========================================================================
    doc.add_heading("4. Dataset Specifications & Data Dictionary", level=1)

    doc.add_heading("4.1 Dataset 1: Symptom2Disease (NLP Source)", level=2)
    doc.add_paragraph(
        "• Source: Kaggle Medical NLP Repository\n"
        "• Total Records: 1,200 rows (perfectly balanced with 50 samples per class)\n"
        "• Classes: 24 unique conditions (Psoriasis, Dengue, Typhoid, Pneumonia, Malaria, Diabetes, Arthritis, Migraine, etc.)\n"
        "• Attributes: 'label' (categorical target string), 'text' (natural language symptom description feature)"
    )

    # Sample Table NLP
    tbl_d1 = doc.add_table(rows=6, cols=3)
    tbl_d1.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_d1.autofit = False
    for r in tbl_d1.rows:
        r.cells[0].width = Inches(0.8)
        r.cells[1].width = Inches(1.8)
        r.cells[2].width = Inches(3.9)

    d1_headers = ["Index", "Target Disease", "Symptom Narrative (Text Feature)"]
    for ci, h in enumerate(d1_headers):
        c = tbl_d1.cell(0, ci)
        set_cell_background(c, "1E293B")
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(9.5)

    d1_sample = [
        ("0", "Psoriasis", "I have been experiencing a skin rash on my arms, legs, and torso for the past few weeks. It is red, itchy, and scaly."),
        ("1", "Psoriasis", "My skin has been peeling, especially on my knees, elbows, and scalp accompanied by a burning sensation."),
        ("24", "Varicose veins", "I have noticed bulging and twisted veins on my legs. They appear blue and purple, and my legs feel heavy."),
        ("62", "Typhoid", "I have had a high fever and chills for three days with severe stomach pain, weakness, and loss of appetite."),
        ("118", "Pneumonia", "I have a persistent cough with green phlegm, high fever, and sharp pain in my chest whenever I breathe.")
    ]
    for ri, row in enumerate(d1_sample):
        for ci, val in enumerate(row):
            c = tbl_d1.cell(ri + 1, ci)
            set_cell_background(c, "F8FAFC" if ri % 2 == 0 else "FFFFFF")
            p = c.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9)
            if ci < 2:
                r.font.bold = True

    doc.add_heading("4.2 Dataset 2: disease_symptoms.csv (Structured ML Source)", level=2)
    doc.add_paragraph(
        "• Source: Kaggle Clinical Dataset\n"
        "• Raw Dimensions: 246,947 rows x 378 columns (~190 MB on disk)\n"
        "• Sampled Dimensions: 19,756 records sampled via chunksize=25000\n"
        "• Attributes: 'diseases' (673 classes), and 377 binary columns (0 = absent, 1 = present)"
    )

    # Sample Table ML
    tbl_d2 = doc.add_table(rows=6, cols=6)
    tbl_d2.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_d2.autofit = False
    for r in tbl_d2.rows:
        r.cells[0].width = Inches(2.0)
        for ci in range(1, 6):
            r.cells[ci].width = Inches(0.9)

    d2_headers = ["Target Disease", "headache", "fever", "cough", "vomiting", "chest pain"]
    for ci, h in enumerate(d2_headers):
        c = tbl_d2.cell(0, ci)
        set_cell_background(c, "1E293B")
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(9.5)

    d2_sample = [
        ("panic disorder", "1", "0", "0", "0", "1"),
        ("influenza", "1", "1", "1", "0", "0"),
        ("gastroenteritis", "0", "1", "0", "1", "0"),
        ("migraine", "1", "0", "0", "1", "0"),
        ("pneumonia", "0", "1", "1", "0", "1")
    ]
    for ri, row in enumerate(d2_sample):
        for ci, val in enumerate(row):
            c = tbl_d2.cell(ri + 1, ci)
            set_cell_background(c, "F8FAFC" if ri % 2 == 0 else "FFFFFF")
            p = c.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9)
            if ci == 0:
                r.font.bold = True

    # =========================================
    # SECTION 5: SYSTEM DIAGRAMS & ARCHITECTURE
    # =========================================
    doc.add_heading("5. System Architecture & Design Diagrams", level=1)

    doc.add_heading("5.1 System Architecture Overview", level=2)
    doc.add_paragraph(
        "AuraDX is built as a 4-tier decoupled web application:\n"
        "1. Presentation Layer: HTML5, CSS3 Glassmorphism, and Vanilla JavaScript with ES6 Fetch API. Handles user text input, keyword tags, and animated meters.\n"
        "2. Application Layer: Flask 3.0+ REST controller exposing '/' (Web Dashboard) and 'POST /api/predict'. Coordinates parallel dual-engine inference.\n"
        "3. Dual-Engine Intelligence Layer:\n"
        "   - Branch A: NLTK Lemmatizer -> TF-IDF Vectorizer -> Logistic Regression (24 classes)\n"
        "   - Branch B: 377-Lexicon Matcher -> 1x377 Binary Vector -> 50-Tree Random Forest (673 classes)\n"
        "4. Storage & Persistence Layer: File-based architecture holding flat CSV datasets in data/ and gzip-compressed joblib binaries in saved_models/ (41.4 MB)."
    )

    doc.add_heading("5.2 Use Case Model & Dependencies", level=2)
    doc.add_paragraph(
        "• Actors:\n"
        "  - Patient / End User: Enters symptom text, clicks suggestion tags, and views predictions.\n"
        "  - Triage Clinician: Auxiliary decision-support user comparing dual predictions for patient queue prioritization.\n"
        "  - Data Scientist / Administrator: Executes offline retraining (train_all.py) and monitors evaluation heatmaps.\n\n"
        "• Key Use Cases:\n"
        "  - UC-1: Enter Symptom Description\n"
        "  - UC-2: Select Suggestion Pills (<<extend>> UC-1)\n"
        "  - UC-3: Request Dual Disease Diagnosis (<<include>> UC-4 and UC-5)\n"
        "  - UC-4: Clean & Lemmatize Text\n"
        "  - UC-5: Map Keywords to 377 Binary Symptom Flags\n"
        "  - UC-6: View Side-by-Side Results\n"
        "  - UC-7: Retrain & Compress Models (<<include>> UC-8)\n"
        "  - UC-8: Plot Evaluation Confusion Matrix"
    )

    doc.add_heading("5.3 Database Applicability Statement", level=2)
    doc.add_paragraph(
        "Official Academic Justification:\n"
        "A traditional Relational Database Management System (RDBMS like MySQL/PostgreSQL) is NOT required for this project.\n"
        "AuraDX operates as a stateless machine learning inference web service. It does not perform transactional OLTP, user session logging, "
        "or patient credential management. Serialized model weights are stored in compressed .joblib binaries and datasets in flat CSV files. "
        "Adding an RDBMS would add unnecessary connection latency without any functional utility for real-time model serving."
    )

    # =========================================
    # SECTION 6: SYSTEM REQUIREMENTS
    # =========================================
    doc.add_heading("6. System Requirements", level=1)

    tbl_req = doc.add_table(rows=6, cols=3)
    tbl_req.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_req.autofit = False
    for r in tbl_req.rows:
        r.cells[0].width = Inches(2.0)
        r.cells[1].width = Inches(2.2)
        r.cells[2].width = Inches(2.3)

    req_headers = ["Component", "Minimum Requirement", "Recommended Specification"]
    for ci, h in enumerate(req_headers):
        c = tbl_req.cell(0, ci)
        set_cell_background(c, "0F172A")
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(10)

    req_rows = [
        ("Processor", "Intel Core i3 / AMD Ryzen 3 (Quad Core)", "Intel Core i5 / AMD Ryzen 5 or higher"),
        ("RAM", "4 GB DDR3/DDR4", "8 GB – 16 GB DDR4"),
        ("Storage", "1 GB Free Disk Space", "SSD with 5 GB Free Space"),
        ("Operating System", "Windows 10 (64-bit) or Ubuntu 20.04+", "Windows 11 or Ubuntu 22.04 LTS"),
        ("Software Stack", "Python 3.10+, Flask 3.0+, Scikit-Learn", "Python 3.11+, VS Code, Git, Chrome/Edge")
    ]

    for ri, row in enumerate(req_rows):
        for ci, val in enumerate(row):
            c = tbl_req.cell(ri + 1, ci)
            set_cell_background(c, "F8FAFC" if ri % 2 == 0 else "FFFFFF")
            p = c.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            if ci == 0:
                r.font.bold = True

    # =========================================
    # SECTION 7: EXPERIMENTAL RESULTS
    # =========================================
    doc.add_heading("7. Experimental Results & Performance Analysis", level=1)

    tbl_perf = doc.add_table(rows=3, cols=6)
    tbl_perf.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_perf.autofit = False
    for r in tbl_perf.rows:
        r.cells[0].width = Inches(2.0)
        r.cells[1].width = Inches(0.9)
        r.cells[2].width = Inches(0.9)
        r.cells[3].width = Inches(0.9)
        r.cells[4].width = Inches(0.9)
        r.cells[5].width = Inches(0.9)

    perf_headers = ["Model / Approach", "Classes", "Sample Size", "Accuracy", "Recall", "F1-Score"]
    for ci, h in enumerate(perf_headers):
        c = tbl_perf.cell(0, ci)
        set_cell_background(c, "0F172A")
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(9.5)

    perf_rows = [
        ("NLP (TF-IDF + Logistic Regression)", "24", "1,200", "96.0%", "96.0%", "96.0%"),
        ("ML (Random Forest Ensemble)", "673", "19,756", "81.6%", "76.6%", "75.5%")
    ]

    for ri, row in enumerate(perf_rows):
        for ci, val in enumerate(row):
            c = tbl_perf.cell(ri + 1, ci)
            set_cell_background(c, "F8FAFC" if ri % 2 == 0 else "FFFFFF")
            p = c.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            if ci == 0:
                r.font.bold = True

    doc.add_paragraph("\n")
    doc.add_paragraph(
        "Why the Comparison is Not Apples-to-Apples (Viva Discussion Insight):\n"
        "Although the NLP model achieved higher accuracy (96.0% vs 81.6%), the task complexity differs by orders of magnitude:\n"
        "• Class Cardinality: Random guessing on the NLP task has a probability of 1/24 = 4.17%, while random guessing on the ML task has a probability of 1/673 = 0.15%.\n"
        "• Macro Recall: Achieving 76.6% macro recall across 673 classes is an exceptionally strong result, proving that binary symptom flags provide powerful diagnostic signals despite extreme sparsity."
    )

    # =========================================
    # SECTION 8: SYSTEM LAYOUTS & USER INTERFACE
    # =========================================
    doc.add_heading("8. System Layouts & User Interfaces", level=1)
    doc.add_paragraph(
        "1. Symptom Entry & Suggestion Panel: Textarea accepting free-form patient narratives with 7 quick-select suggestion pills (headache, fever, cough, vomiting, nausea, back pain, shortness of breath) and an 'Analyze Symptoms' button with an animated loading spinner.\n\n"
        "2. Dual-Engine Diagnostic Results Panel: Side-by-side display featuring:\n"
        "   • Model 1 (NLP Card): Cleaned lemmatized text preview, predicted disease name, and animated confidence progress bar.\n"
        "   • Model 2 (Structured ML Card): Dynamically extracted symptom badge pills, predicted disease across 673 classes, and animated confidence progress bar.\n\n"
        "3. Interactive Terminal CLI Interface (src/predict.py): Lightweight command-line triage tool for headless environments.\n\n"
        "4. Confusion Matrix Heatmap (saved_models/confusion_matrix_nlp.png): Visual seaborn heatmap evaluating true vs predicted labels across 24 conditions."
    )

    # =========================================
    # SECTION 9: CONCLUSION & FUTURE SCOPE
    # =========================================
    doc.add_heading("9. Conclusion & Future Roadmap", level=1)
    doc.add_paragraph(
        "AuraDX successfully demonstrates that combining unstructured conversational NLP with high-cardinality machine learning creates an effective, low-latency clinical decision-support tool. "
        "By achieving 160x compression via Joblib gzip serialization, the system delivers sub-second cold starts and real-time inference on modest workstation hardware.\n\n"
        "Future Enhancements:\n"
        "• Clinical Transformers: Integrate pretrained Bio_ClinicalBERT or PubMedBERT to capture complex syntactic negation (e.g., 'patient denies fever').\n"
        "• Hospital EHR Integration: Implement HL7 / FHIR APIs to ingest patient history directly from hospital Electronic Health Records.\n"
        "• Multi-Lingual Support: Expand NLTK preprocessing to handle regional Indian languages (Hindi, Marathi) for rural healthcare outreach.\n"
        "• Emergency Severity Index (ESI): Incorporate clinical triage urgency level tagging (Levels 1 to 5) with color codes (Red, Yellow, Green)."
    )

    # =========================================
    # SECTION 10: ENDORSEMENT & SIGNATURES
    # =========================================
    doc.add_paragraph("\n" * 2)
    p_sig = doc.add_paragraph()
    p_sig.add_run(
        "________________________        ________________________        ________________________\n"
        "   (Student Signature)             (Student Signature)             (Student Signature)\n"
        "     Nishant DS2521                    Yash DS2521                    Suraj DS2521\n\n\n"
        "________________________                                        ________________________\n"
        " (Internal Project Guide)                                        (Head of the Department)\n"
        "  Department of Data Science                                      Department of Data Science\n"
        "  Nowrosjee Wadia College, Pune                                   Nowrosjee Wadia College, Pune"
    )

    out_file = "AuraDX_Project_Documentation.docx"
    doc.save(out_file)
    print(f"[SUCCESS] Word documentation created successfully at: {out_file}")

if __name__ == "__main__":
    create_report()
