import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # Set 16:9 widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    blank_slide_layout = prs.slide_layouts[6]
    
    # Color Palette: Modern Medical Dark / Slate & Cyan
    BG_COLOR = RGBColor(15, 23, 42)       # Slate 900
    CARD_BG = RGBColor(30, 41, 59)        # Slate 800
    TEXT_MAIN = RGBColor(248, 250, 252)   # Slate 50
    TEXT_MUTED = RGBColor(148, 163, 184)  # Slate 400
    ACCENT_CYAN = RGBColor(6, 182, 212)   # Cyan 500
    ACCENT_TEAL = RGBColor(20, 184, 166)  # Teal 500
    ACCENT_BLUE = RGBColor(59, 130, 246)  # Blue 500
    ACCENT_EMERALD = RGBColor(16, 185, 129) # Emerald 500
    ACCENT_AMBER = RGBColor(245, 158, 11) # Amber 500
    BORDER_COLOR = RGBColor(51, 65, 85)   # Slate 700

    def apply_bg(slide):
        bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = BG_COLOR
        bg_shape.line.fill.background()
        return bg_shape

    def add_header(slide, title_text, category_text="AuraDX Presentation"):
        # Header category pill
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(10), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_CYAN

        # Slide Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(26)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_MAIN

        # Decorative line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.73), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = BORDER_COLOR
        line.line.fill.background()

    def add_card(slide, left, top, width, height, bg=CARD_BG, border=BORDER_COLOR):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg
        card.line.color.rgb = border
        card.line.width = Pt(1.5)
        return card

    # ==========================================
    # SLIDE 1: Title Slide
    # ==========================================
    s1 = prs.slides.add_slide(blank_slide_layout)
    apply_bg(s1)

    # Title Card
    add_card(s1, 0.8, 0.8, 11.733, 5.9, bg=RGBColor(24, 34, 53), border=ACCENT_CYAN)

    tbox = s1.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(10.9), Inches(5.1))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "NOWROSJEE WADIA COLLEGE, PUNE – 411 001"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_CYAN
    p0.alignment = PP_ALIGN.CENTER

    p0b = tf1.add_paragraph()
    p0b.text = "Department of Computer Science & Data Science (Affiliated to SPPU)"
    p0b.font.size = Pt(12)
    p0b.font.color.rgb = TEXT_MUTED
    p0b.alignment = PP_ALIGN.CENTER

    p_gap = tf1.add_paragraph()
    p_gap.text = ""

    p1 = tf1.add_paragraph()
    p1.text = "AuraDX"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(56, 189, 248) # Sky blue
    p1.alignment = PP_ALIGN.CENTER

    p2 = tf1.add_paragraph()
    p2.text = "Dual-Engine Symptom Classifier using NLP & Structured Machine Learning"
    p2.font.size = Pt(22)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_MAIN
    p2.alignment = PP_ALIGN.CENTER

    p3 = tf1.add_paragraph()
    p3.text = "An AI-Assisted Clinical Decision Support System (CDSS) for Outpatient Triage"
    p3.font.size = Pt(14)
    p3.font.color.rgb = TEXT_MUTED
    p3.alignment = PP_ALIGN.CENTER

    p_gap2 = tf1.add_paragraph()
    p_gap2.text = ""

    p4 = tf1.add_paragraph()
    p4.text = "Team Members: Nishant | Yash | Suraj   (Roll No: DS2521)"
    p4.font.size = Pt(14)
    p4.font.bold = True
    p4.font.color.rgb = ACCENT_EMERALD
    p4.alignment = PP_ALIGN.CENTER

    p5 = tf1.add_paragraph()
    p5.text = "Academic Year: 2024–2025 / 2025–2026 | Domain: Data Science & Clinical NLP"
    p5.font.size = Pt(12)
    p5.font.color.rgb = TEXT_MUTED
    p5.alignment = PP_ALIGN.CENTER

    # ==========================================
    # SLIDE 2: Introduction & Purpose
    # ==========================================
    s2 = prs.slides.add_slide(blank_slide_layout)
    apply_bg(s2)
    add_header(s2, "Introduction, Purpose & Project Objectives", "Section 2 • Project Foundations")

    # Left Column: Brief Introduction & Purpose
    add_card(s2, 0.8, 1.8, 5.6, 5.0)
    tb_s2_left = s2.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6))
    tf2_l = tb_s2_left.text_frame
    tf2_l.word_wrap = True

    p = tf2_l.paragraphs[0]
    p.text = "Clinical Triage Challenge & Purpose"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    items_l = [
        "In healthcare outpatient clinics, clinical triage is the first critical line of assessment to prioritize patient care.",
        "Traditional inquiry suffers from cognitive fatigue, high inter-observer variability, and severe bottlenecks during peak hours.",
        "Patient data arrives in two distinct modalities: noisy free-text conversational descriptions and formal structured symptom checklists.",
        "Purpose: AuraDX builds a unified Clinical Decision Support System (CDSS) combining Unstructured NLP and Structured ML to cross-verify diagnoses side-by-side in real time."
    ]
    for item in items_l:
        p = tf2_l.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

    # Right Column: Measurable Objectives
    add_card(s2, 6.8, 1.8, 5.733, 5.0)
    tb_s2_right = s2.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf2_r = tb_s2_right.text_frame
    tf2_r.word_wrap = True

    p = tf2_r.paragraphs[0]
    p.text = "Measurable Project Objectives"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_EMERALD

    items_r = [
        "1. Train High-Accuracy NLP Engine: Achieve >90% accuracy on natural language symptom narratives using NLTK lemmatization and TF-IDF Logistic Regression.",
        "2. High-Cardinality Multi-Class Classifier: Deploy a memory-optimized 50-tree Random Forest mapping 377 symptom flags across 673 distinct diseases.",
        "3. 160x Model Compression: Utilize Joblib gzip compression (level 3) to compress binary model files from 6.6 GB down to 41.4 MB for rapid cold boot.",
        "4. Deploy Real-Time Web Interface: Deliver a responsive, dark-mode glassmorphic Flask web app providing live side-by-side diagnostic inference and animated confidence meters."
    ]
    for item in items_r:
        p = tf2_r.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

    # ==========================================
    # SLIDE 3: Team Details
    # ==========================================
    s3 = prs.slides.add_slide(blank_slide_layout)
    apply_bg(s3)
    add_header(s3, "Team Details & Individual Contributions", "Section 3 • Project Team")

    team_members = [
        {
            "name": "Nishant",
            "roll": "DS2521",
            "role": "Project Lead & ML Architecture",
            "color": ACCENT_CYAN,
            "tasks": [
                "Architected the dual-engine ML paradigm and pipeline.",
                "Designed the 50-tree Random Forest classifier across 673 disease categories.",
                "Engineered chunked dataset loading logic for large CSV data.",
                "Implemented Joblib gzip level 3 compression (6.6 GB -> 41.4 MB)."
            ]
        },
        {
            "name": "Yash",
            "roll": "DS2521",
            "role": "NLP & Preprocessing Specialist",
            "color": ACCENT_EMERALD,
            "tasks": [
                "Built text sanitation, tokenization & WordNet lemmatization pipeline.",
                "Engineered unigram+bigram TF-IDF vectorization (3,000 features).",
                "Trained and evaluated multi-class Logistic Regression on Symptom2Disease.",
                "Generated confusion matrix heatmap and classification metrics report."
            ]
        },
        {
            "name": "Suraj",
            "roll": "DS2521",
            "role": "Full-Stack & Integration Engineer",
            "color": ACCENT_AMBER,
            "tasks": [
                "Engineered the Flask REST controller (src/app.py) & /api/predict endpoint.",
                "Designed responsive dark-mode Glassmorphic web UI (HTML5/CSS3).",
                "Built asynchronous JS frontend with animated confidence meters.",
                "Conducted end-to-end integration testing and interactive CLI development."
            ]
        }
    ]

    card_w = 3.65
    gap = 0.39
    for i, m in enumerate(team_members):
        left_pos = 0.8 + i * (card_w + gap)
        add_card(s3, left_pos, 1.8, card_w, 5.0, border=m["color"])
        tb = s3.shapes.add_textbox(Inches(left_pos + 0.2), Inches(2.0), Inches(card_w - 0.4), Inches(4.6))
        tf = tb.text_frame
        tf.word_wrap = True

        p_name = tf.paragraphs[0]
        p_name.text = m["name"]
        p_name.font.size = Pt(20)
        p_name.font.bold = True
        p_name.font.color.rgb = m["color"]

        p_roll = tf.add_paragraph()
        p_roll.text = f"Roll No: {m['roll']}"
        p_roll.font.size = Pt(13)
        p_roll.font.bold = True
        p_roll.font.color.rgb = TEXT_MAIN

        p_dept = tf.add_paragraph()
        p_dept.text = "Dept. of Data Science\nNowrosjee Wadia College"
        p_dept.font.size = Pt(11)
        p_dept.font.color.rgb = TEXT_MUTED

        p_role = tf.add_paragraph()
        p_role.text = m["role"]
        p_role.font.size = Pt(12)
        p_role.font.bold = True
        p_role.font.color.rgb = m["color"]
        p_role.space_before = Pt(8)

        p_div = tf.add_paragraph()
        p_div.text = "Key Contributions:"
        p_div.font.size = Pt(12)
        p_div.font.bold = True
        p_div.font.color.rgb = TEXT_MAIN
        p_div.space_before = Pt(6)

        for t in m["tasks"]:
            p_t = tf.add_paragraph()
            p_t.text = "• " + t
            p_t.font.size = Pt(10.5)
            p_t.font.color.rgb = TEXT_MUTED
            p_t.space_before = Pt(3)

    # ==========================================
    # SLIDE 4: Existing System & Limitations
    # ==========================================
    s4 = prs.slides.add_slide(blank_slide_layout)
    apply_bg(s4)
    add_header(s4, "Existing System & Critical Limitations", "Section 4 • Problem Analysis")

    # Left: Existing System Description
    add_card(s4, 0.8, 1.8, 5.6, 5.0)
    tb_s4_left = s4.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6))
    tf4_l = tb_s4_left.text_frame
    tf4_l.word_wrap = True

    p = tf4_l.paragraphs[0]
    p.text = "Overview of Existing Systems"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_AMBER

    items_s4_l = [
        "Manual Clinical Intake: Triage nurses or hospital clerical staff interview patients verbally to fill physical registration forms.",
        "Generic Symptom Checkers: Tools like WebMD or basic keyword-matching websites rely on simple dictionary lookups or static decision trees.",
        "Single-Modality Dependency: Current systems strictly accept either free-form text OR a closed checklist—never cross-referencing both.",
        "Rule-Based Vulnerability: Hardcoded rule engines cannot handle misspellings, colloquial expressions, or complex overlapping symptoms."
    ]
    for item in items_s4_l:
        p = tf4_l.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(10)

    # Right: Limitations of Existing Systems
    add_card(s4, 6.8, 1.8, 5.733, 5.0)
    tb_s4_right = s4.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf4_r = tb_s4_right.text_frame
    tf4_r.word_wrap = True

    p = tf4_r.paragraphs[0]
    p.text = "Severe Operational Limitations"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = RGBColor(239, 68, 68) # Red

    limitations = [
        ("No Dual Cross-Validation: ", "Inferences are made in isolation without secondary model verification, increasing misdiagnosis risks."),
        ("Narrative Noise Fragility: ", "Keyword search fails when patients use varied phrases (e.g., 'feeling dizzy and woozy' vs 'vertigo')."),
        ("Triage Queues & Fatigue: ", "Manual documentation creates dangerous patient wait times during peak epidemic or outpatient surges."),
        ("Prohibitive Memory Overhead: ", "Standard multi-class ensembles spanning 600+ conditions require 6+ GB of uncompressed memory, preventing local deployment.")
    ]
    for title, desc in limitations:
        p = tf4_r.add_paragraph()
        p.text = "• " + title + desc
        p.font.size = Pt(12.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

    # ==========================================
    # SLIDE 5: Proposed System & Key Features
    # ==========================================
    s5 = prs.slides.add_slide(blank_slide_layout)
    apply_bg(s5)
    add_header(s5, "Proposed System & Key Architectural Features", "Section 5 • Proposed Solution (1/2)")

    feat_cards = [
        {
            "title": "Dual-Engine Architecture",
            "desc": "Simultaneously activates an Unstructured NLP Classifier (free text) and a Structured ML Classifier (377 symptom flags) side-by-side for comparative validation.",
            "color": ACCENT_CYAN,
            "badge": "Core Innovation"
        },
        {
            "title": "High-Cardinality Prediction",
            "desc": "Engine 2 maps 377 binary symptom features across 673 distinct medical conditions—scaling far beyond standard 10-20 class academic toy models.",
            "color": ACCENT_EMERALD,
            "badge": "673 Disease Classes"
        },
        {
            "title": "160x Model Compression",
            "desc": "Memory-safe chunked loading and Joblib gzip level 3 compression shrink the Random Forest binary from 6.6 GB down to 41.4 MB for sub-second cold boot.",
            "color": ACCENT_BLUE,
            "badge": "Optimized Footprint"
        },
        {
            "title": "Real-Time Glassmorphic UI",
            "desc": "A responsive dark-mode dashboard provides dynamic symptom tag suggestions, instant keyword mapping, and animated confidence meters.",
            "color": ACCENT_AMBER,
            "badge": "Interactive Web App"
        }
    ]

    for idx, fc in enumerate(feat_cards):
        row = idx // 2
        col = idx % 2
        l = 0.8 + col * (5.6 + 0.533)
        t = 1.8 + row * (2.35 + 0.3)
        add_card(s5, l, t, 5.6, 2.35, border=fc["color"])

        tb = s5.shapes.add_textbox(Inches(l + 0.2), Inches(t + 0.2), Inches(5.2), Inches(1.95))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = fc["title"] + "  [" + fc["badge"] + "]"
        p_t.font.size = Pt(16)
        p_t.font.bold = True
        p_t.font.color.rgb = fc["color"]

        p_d = tf.add_paragraph()
        p_d.text = fc["desc"]
        p_d.font.size = Pt(12)
        p_d.font.color.rgb = TEXT_MAIN
        p_d.space_before = Pt(6)

    # ==========================================
    # SLIDE 6: Algorithms Used & Application
    # ==========================================
    s6 = prs.slides.add_slide(blank_slide_layout)
    apply_bg(s6)
    add_header(s6, "Algorithms Used & Implementation Details", "Section 5 • Proposed Solution (2/2)")

    # 2 Big Cards
    add_card(s6, 0.8, 1.8, 5.6, 5.0, border=ACCENT_CYAN)
    tb_s6_l = s6.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6))
    tf6_l = tb_s6_l.text_frame
    tf6_l.word_wrap = True

    p = tf6_l.paragraphs[0]
    p.text = "Engine 1: NLP Symptom Classifier"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    alg_nlp = [
        ("NLTK Preprocessing Pipeline: ", "Converts text to lowercase, strips non-alphabet regex symbols, removes English stopwords, and applies WordNet lemmatization."),
        ("TF-IDF Vectorization: ", "Extracts unigram and bigram n-grams (1,2) with a vocabulary limit of 3,000 features, weighting rare clinical keywords."),
        ("Multi-Class Logistic Regression: ", "Trained with L2 regularization and max_iter=1000 over 24 distinct illness categories."),
        ("Purpose & Metric: ", "Interprets conversational patient self-reports. Achieved 96.0% Test Accuracy, 96.0% Macro Recall, and 96.0% Macro F1-Score.")
    ]
    for h, d in alg_nlp:
        p = tf6_l.add_paragraph()
        p.text = "• " + h + d
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

    add_card(s6, 6.8, 1.8, 5.733, 5.0, border=ACCENT_EMERALD)
    tb_s6_r = s6.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf6_r = tb_s6_r.text_frame
    tf6_r.word_wrap = True

    p = tf6_r.paragraphs[0]
    p.text = "Engine 2: Structured ML Classifier"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_EMERALD

    alg_ml = [
        ("Dynamic Keyword Mapping: ", "Scans user input against a 377 symptom lexicon to generate a 1x377 binary feature vector on the fly."),
        ("Random Forest Ensemble: ", "Built with 50 decision trees, Gini impurity splitting criterion, and full depth exploration."),
        ("Label Encoding & Chunking: ", "Transforms 673 unique disease strings into numerical targets and samples huge CSV via chunksize=25000."),
        ("Purpose & Metric: ", "Performs clinical checklist triage across 673 diseases. Achieved 81.6% Test Accuracy and 76.6% Macro Recall despite extreme sparsity.")
    ]
    for h, d in alg_ml:
        p = tf6_r.add_paragraph()
        p.text = "• " + h + d
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

    # ==========================================
    # SLIDE 7: Dataset Description (NLP)
    # ==========================================
    s7 = prs.slides.add_slide(blank_slide_layout)
    apply_bg(s7)
    add_header(s7, "Dataset Description: Unstructured NLP Engine", "Section 6 • Dataset Analysis (1/2)")

    # Left Stats Card
    add_card(s7, 0.8, 1.8, 4.2, 5.0)
    tb_s7_l = s7.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(3.8), Inches(4.6))
    tf7_l = tb_s7_l.text_frame
    tf7_l.word_wrap = True

    p = tf7_l.paragraphs[0]
    p.text = "Dataset Specifications"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    nlp_specs = [
        ("Dataset Name: ", "Symptom2Disease"),
        ("Source: ", "Kaggle Medical NLP"),
        ("Total Records: ", "1,200 rows"),
        ("Distribution: ", "Balanced (50 samples / class)"),
        ("Disease Classes: ", "24 unique conditions"),
        ("Feature Column: ", "text (Free-text descriptions)"),
        ("Target Column: ", "label (Disease category)"),
        ("Role in AuraDX: ", "Powers conversational NLP inference for patient narrative intake.")
    ]
    for h, d in nlp_specs:
        p = tf7_l.add_paragraph()
        p.text = h + d
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(4)

    # Right: Sample Data Table
    add_card(s7, 5.3, 1.8, 7.233, 5.0)
    tb_s7_r = s7.shapes.add_textbox(Inches(5.5), Inches(2.0), Inches(6.8), Inches(4.6))
    tf7_r = tb_s7_r.text_frame
    tf7_r.word_wrap = True

    p = tf7_r.paragraphs[0]
    p.text = "Representative Sample (Symptom2Disease.csv)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_EMERALD

    # Create Table on slide
    table_shape = s7.shapes.add_table(6, 3, Inches(5.5), Inches(2.6), Inches(6.8), Inches(3.8))
    table = table_shape.table
    table.columns[0].width = Inches(0.8)
    table.columns[1].width = Inches(1.8)
    table.columns[2].width = Inches(4.2)

    headers = ["Index", "Target Disease", "Symptom Narrative (Text Feature)"]
    for ci, h in enumerate(headers):
        cell = table.cell(0, ci)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(51, 65, 85)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = ACCENT_CYAN

    sample_nlp = [
        ("0", "Psoriasis", "I have been experiencing a skin rash on my arms, legs, and torso for the past few weeks. It is red, itchy, and covered in dry, scaly patches."),
        ("1", "Psoriasis", "My skin has been peeling, especially on my knees, elbows, and scalp accompanied by a burning sensation."),
        ("24", "Varicose veins", "I have noticed bulging and twisted veins on my legs. They appear blue and purple, and my legs feel heavy and swollen."),
        ("62", "Typhoid", "I have had a high fever and chills for three days with severe stomach pain, weakness, and loss of appetite."),
        ("118", "Pneumonia", "I have a persistent cough with green phlegm, high fever, and sharp pain in my chest whenever I take a deep breath.")
    ]
    for ri, row in enumerate(sample_nlp):
        for ci, val in enumerate(row):
            cell = table.cell(ri + 1, ci)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(30, 41, 59) if ri % 2 == 0 else RGBColor(24, 34, 53)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_MAIN

    # ==========================================
    # SLIDE 8: Dataset Description (Structured ML)
    # ==========================================
    s8 = prs.slides.add_slide(blank_slide_layout)
    apply_bg(s8)
    add_header(s8, "Dataset Description: Structured Clinical ML Engine", "Section 6 • Dataset Analysis (2/2)")

    # Left Stats Card
    add_card(s8, 0.8, 1.8, 4.2, 5.0)
    tb_s8_l = s8.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(3.8), Inches(4.6))
    tf8_l = tb_s8_l.text_frame
    tf8_l.word_wrap = True

    p = tf8_l.paragraphs[0]
    p.text = "Dataset Specifications"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_EMERALD

    ml_specs = [
        ("Dataset Name: ", "disease_symptoms.csv"),
        ("Source: ", "Kaggle Clinical Dataset"),
        ("Raw Size: ", "246,947 rows (190 MB)"),
        ("Sampled Size: ", "19,756 records (Chunked)"),
        ("Total Columns: ", "378 features"),
        ("Target Column: ", "diseases (673 classes)"),
        ("Input Features: ", "377 binary symptom flags (1 = present, 0 = absent)"),
        ("Role in AuraDX: ", "Powers structured clinical checklist triage.")
    ]
    for h, d in ml_specs:
        p = tf8_l.add_paragraph()
        p.text = h + d
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(4)

    # Right: Sample Data Table
    add_card(s8, 5.3, 1.8, 7.233, 5.0)
    tb_s8_r = s8.shapes.add_textbox(Inches(5.5), Inches(2.0), Inches(6.8), Inches(4.6))
    tf8_r = tb_s8_r.text_frame
    tf8_r.word_wrap = True

    p = tf8_r.paragraphs[0]
    p.text = "Representative Sample (disease_symptoms.csv - 377 Binary Flags)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    # Create Table on slide
    table_shape_ml = s8.shapes.add_table(6, 6, Inches(5.5), Inches(2.6), Inches(6.8), Inches(3.8))
    table_ml = table_shape_ml.table
    table_ml.columns[0].width = Inches(2.0)
    table_ml.columns[1].width = Inches(0.95)
    table_ml.columns[2].width = Inches(0.95)
    table_ml.columns[3].width = Inches(0.95)
    table_ml.columns[4].width = Inches(0.95)
    table_ml.columns[5].width = Inches(1.0)

    headers_ml = ["Target Disease", "headache", "fever", "cough", "vomiting", "chest pain"]
    for ci, h in enumerate(headers_ml):
        cell = table_ml.cell(0, ci)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(51, 65, 85)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = ACCENT_CYAN

    sample_ml = [
        ("panic disorder", "1", "0", "0", "0", "1"),
        ("influenza", "1", "1", "1", "0", "0"),
        ("gastroenteritis", "0", "1", "0", "1", "0"),
        ("migraine", "1", "0", "0", "1", "0"),
        ("pneumonia", "0", "1", "1", "0", "1")
    ]
    for ri, row in enumerate(sample_ml):
        for ci, val in enumerate(row):
            cell = table_ml.cell(ri + 1, ci)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(30, 41, 59) if ri % 2 == 0 else RGBColor(24, 34, 53)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10)
            p.font.color.rgb = TEXT_MAIN

    # ==========================================
    # SLIDE 9: System Architecture Diagram
    # ==========================================
    s9 = prs.slides.add_slide(blank_slide_layout)
    apply_bg(s9)
    add_header(s9, "System Architecture Diagram", "Section 7 • System Diagrams (1/2)")

    # Architecture Cards Flow
    add_card(s9, 0.8, 1.8, 11.733, 5.0)
    tb_s9 = s9.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.3), Inches(4.6))
    tf9 = tb_s9.text_frame
    tf9.word_wrap = True

    p = tf9.paragraphs[0]
    p.text = "High-Level Dual-Engine System Architecture"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    # Add 4 horizontal layer cards inside
    layers = [
        ("1. Presentation Layer (Frontend)", "HTML5 + Glassmorphism CSS3 + Vanilla JavaScript (ES6 Fetch API)\n• User symptom narrative textarea, clickable keyword pills, dynamic progress meters.", ACCENT_CYAN, 0.8, 2.6, 2.7, 3.8),
        ("2. Application Layer (Flask API)", "Flask 3.0+ REST Controller (src/app.py)\n• Endpoints: '/' (Dashboard) and 'POST /api/predict'\n• Coordinates parallel inference, text cleaning, vector mapping & JSON assembly.", ACCENT_BLUE, 3.8, 2.6, 2.7, 3.8),
        ("3. Dual-Engine Intelligence Layer", "Engine A (NLP): NLTK Lemmatizer -> TF-IDF (3,000 n-grams) -> Logistic Regression (24 classes)\nEngine B (ML): 377-Lexicon Matcher -> 1x377 Binary Vector -> 50-Tree Random Forest (673 classes).", ACCENT_EMERALD, 6.8, 2.6, 2.7, 3.8),
        ("4. Storage & Persistence Layer", "Stateless File-Based Architecture\n• data/: Symptom2Disease.csv & disease_symptoms.csv\n• saved_models/: Gzip-compressed .joblib binaries (41.4 MB) & evaluation heatmaps.", ACCENT_AMBER, 9.8, 2.6, 2.7, 3.8)
    ]

    for title, desc, col, l, t, w, h in layers:
        add_card(s9, l, t, w, h, bg=RGBColor(24, 34, 53), border=col)
        tb_layer = s9.shapes.add_textbox(Inches(l + 0.15), Inches(t + 0.15), Inches(w - 0.3), Inches(h - 0.3))
        tf_l = tb_layer.text_frame
        tf_l.word_wrap = True

        p_lt = tf_l.paragraphs[0]
        p_lt.text = title
        p_lt.font.size = Pt(13)
        p_lt.font.bold = True
        p_lt.font.color.rgb = col

        p_ld = tf_l.add_paragraph()
        p_ld.text = desc
        p_ld.font.size = Pt(10.5)
        p_ld.font.color.rgb = TEXT_MAIN
        p_ld.space_before = Pt(8)

    # ==========================================
    # SLIDE 10: Use Case Diagram
    # ==========================================
    s10 = prs.slides.add_slide(blank_slide_layout)
    apply_bg(s10)
    add_header(s10, "Use Case Diagram & Actor Interactions", "Section 7 • System Diagrams (2/2)")

    # Left: Actors & Responsibilities
    add_card(s10, 0.8, 1.8, 4.5, 5.0)
    tb_s10_l = s10.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(4.1), Inches(4.6))
    tf10_l = tb_s10_l.text_frame
    tf10_l.word_wrap = True

    p = tf10_l.paragraphs[0]
    p.text = "Primary Actors & Roles"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    actors = [
        ("Patient / End User: ", "Submits free-form symptom narratives, selects suggested keyword pills, and views dual-engine predictions with confidence scores."),
        ("Triage Nurse / Clinician: ", "Uses the side-by-side output as an auxiliary clinical decision-support tool to quickly prioritize patient queues."),
        ("Data Scientist / Admin: ", "Executes offline training pipelines (train_all.py), monitors classification metrics, tunes estimators, and manages compressed model binaries.")
    ]
    for h, d in actors:
        p = tf10_l.add_paragraph()
        p.text = "• " + h + d
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

    # Right: Use Cases Breakdown
    add_card(s10, 5.6, 1.8, 6.933, 5.0)
    tb_s10_r = s10.shapes.add_textbox(Inches(5.8), Inches(2.0), Inches(6.5), Inches(4.6))
    tf10_r = tb_s10_r.text_frame
    tf10_r.word_wrap = True

    p = tf10_r.paragraphs[0]
    p.text = "Key Functional Use Cases"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_EMERALD

    ucs = [
        ("UC-1: Enter Symptom Description", "User types unstructured conversational narrative into textarea."),
        ("UC-2: Select Quick Symptom Tags", "<<extend>> Appends verified clinical keywords to user input."),
        ("UC-3: Request Dual Disease Diagnosis", "Triggers asynchronous HTTP POST request to /api/predict."),
        ("UC-4: Clean & Lemmatize Text", "<<include>> NLTK removes stopwords and applies WordNet lemmatization."),
        ("UC-5: Map Keywords to 377 Symptom Flags", "<<include>> Vocabulary matching generates 1x377 binary vector."),
        ("UC-6: View Side-by-Side Triage Results", "Renders predicted conditions, mapped pills, and animated meters."),
        ("UC-7: Train & Compress ML/NLP Models", "Offline model fitting and gzip level 3 joblib serialization."),
        ("UC-8: Evaluate Metrics & Heatmaps", "<<include>> Generates accuracy, recall, and confusion matrix.")
    ]
    for h, d in ucs:
        p = tf10_r.add_paragraph()
        p.text = "• " + h + ": " + d
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(4)

    # ==========================================
    # SLIDE 11: Technologies Used & Requirements
    # ==========================================
    s11 = prs.slides.add_slide(blank_slide_layout)
    apply_bg(s11)
    add_header(s11, "Technologies Used & System Requirements", "Section 8 • Technical Specifications")

    tech_cards = [
        {
            "title": "Hardware Requirements",
            "color": ACCENT_CYAN,
            "items": [
                "Processor: Intel Core i3 / AMD Ryzen 3 (Quad Core) min; Core i5 / Ryzen 5 rec.",
                "RAM: 4 GB minimum; 8 GB – 16 GB DDR4 recommended.",
                "Storage: 1 GB free disk space (SSD recommended for fast binary loading).",
                "Display: Standard Full HD Monitor (1920x1080)."
            ]
        },
        {
            "title": "Software & Frameworks",
            "color": ACCENT_EMERALD,
            "items": [
                "Programming Language: Python 3.10 / 3.11+",
                "Web Framework: Flask 3.0+ (WSGI Local Web Server)",
                "ML & NLP Libraries: Scikit-Learn, NLTK, Pandas, NumPy",
                "Frontend: HTML5, CSS3 (Glassmorphism), JavaScript (ES6 Fetch API)"
            ]
        },
        {
            "title": "Operating System & Tools",
            "color": ACCENT_BLUE,
            "items": [
                "Operating System: Windows 10 / 11 or Linux (Ubuntu 20.04+)",
                "Development IDE: Visual Studio Code",
                "Version Control: Git & GitHub Repository",
                "Visualization: Matplotlib & Seaborn (Confusion Matrix Heatmaps)"
            ]
        },
        {
            "title": "Database Architecture Used",
            "color": ACCENT_AMBER,
            "items": [
                "Database Used: Stateless File-Based Storage Architecture",
                "Academic Justification: AuraDX is an inference-only web service without transactional OLTP or user accounts.",
                "Flat CSV Datasets: Symptom2Disease.csv & disease_symptoms.csv",
                "Serialized Model Binaries: Joblib gzip-compressed (.joblib) artifacts in saved_models/ (<42 MB)."
            ]
        }
    ]

    for idx, tc in enumerate(tech_cards):
        row = idx // 2
        col = idx % 2
        l = 0.8 + col * (5.6 + 0.533)
        t = 1.8 + row * (2.35 + 0.3)
        add_card(s11, l, t, 5.6, 2.35, border=tc["color"])

        tb = s11.shapes.add_textbox(Inches(l + 0.2), Inches(t + 0.2), Inches(5.2), Inches(1.95))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = tc["title"]
        p_t.font.size = Pt(16)
        p_t.font.bold = True
        p_t.font.color.rgb = tc["color"]

        for it in tc["items"]:
            p_it = tf.add_paragraph()
            p_it.text = "• " + it
            p_it.font.size = Pt(10.5)
            p_it.font.color.rgb = TEXT_MAIN
            p_it.space_before = Pt(3)

    # ==========================================
    # SLIDE 12: Important System Layouts
    # ==========================================
    s12 = prs.slides.add_slide(blank_slide_layout)
    apply_bg(s12)
    add_header(s12, "Important System Layouts & User Interfaces", "Section 9 • System Interfaces")

    layouts = [
        {
            "title": "1. Symptom Intake Panel",
            "color": ACCENT_CYAN,
            "desc": "Allows users to enter free-form English narratives describing their discomfort. Features 7 quick-select suggestion tags (e.g., headache, vomiting, fever) and an interactive 'Analyze Symptoms' button with live loading spinner."
        },
        {
            "title": "2. Welcome & Guidance Screen",
            "color": ACCENT_BLUE,
            "desc": "Displayed upon initial page load before inference is initiated. Guides clinicians on how to submit symptoms and explains the side-by-side dual evaluation mechanism."
        },
        {
            "title": "3. Dual-Engine Diagnostic Results Panel",
            "color": ACCENT_EMERALD,
            "desc": "Side-by-side cards comparing Model 1 (NLP) and Model 2 (Structured ML). Displays cleaned lemmatized text, dynamically mapped symptom pills, predicted disease names, and animated confidence progress bars."
        },
        {
            "title": "4. Terminal CLI & Evaluation Heatmap",
            "color": ACCENT_AMBER,
            "desc": "Interactive command-line interface (predict.py) for lightweight terminal triage, plus high-resolution confusion matrix heatmap (confusion_matrix_nlp.png) for academic model validation."
        }
    ]

    for idx, ly in enumerate(layouts):
        row = idx // 2
        col = idx % 2
        l = 0.8 + col * (5.6 + 0.533)
        t = 1.8 + row * (2.35 + 0.3)
        add_card(s12, l, t, 5.6, 2.35, border=ly["color"])

        tb = s12.shapes.add_textbox(Inches(l + 0.2), Inches(t + 0.2), Inches(5.2), Inches(1.95))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = ly["title"]
        p_t.font.size = Pt(16)
        p_t.font.bold = True
        p_t.font.color.rgb = ly["color"]

        p_d = tf.add_paragraph()
        p_d.text = ly["desc"]
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_MAIN
        p_d.space_before = Pt(6)

    # ==========================================
    # SLIDE 13: Results, Comparative Discussion & Viva Insights
    # ==========================================
    s13 = prs.slides.add_slide(blank_slide_layout)
    apply_bg(s13)
    add_header(s13, "Experimental Results & Comparative Model Analysis", "Performance & Viva Preparation")

    # Table on Left
    add_card(s13, 0.8, 1.8, 5.6, 5.0)
    tb_s13_l = s13.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6))
    tf13_l = tb_s13_l.text_frame
    tf13_l.word_wrap = True

    p = tf13_l.paragraphs[0]
    p.text = "Model Benchmark Performance"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    table_shape_res = s13.shapes.add_table(3, 4, Inches(1.0), Inches(2.6), Inches(5.2), Inches(2.2))
    table_res = table_shape_res.table
    table_res.columns[0].width = Inches(1.8)
    table_res.columns[1].width = Inches(1.0)
    table_res.columns[2].width = Inches(1.2)
    table_res.columns[3].width = Inches(1.2)

    headers_res = ["Model", "Classes", "Accuracy", "Macro F1"]
    for ci, h in enumerate(headers_res):
        cell = table_res.cell(0, ci)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(51, 65, 85)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = ACCENT_CYAN

    res_data = [
        ("NLP (LogReg)", "24", "96.0%", "96.0%"),
        ("ML (Random Forest)", "673", "81.6%", "75.5%")
    ]
    for ri, row in enumerate(res_data):
        for ci, val in enumerate(row):
            cell = table_res.cell(ri + 1, ci)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(30, 41, 59) if ri % 2 == 0 else RGBColor(24, 34, 53)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10)
            p.font.color.rgb = TEXT_MAIN

    # Add Top Predictive Features
    tb_top = s13.shapes.add_textbox(Inches(1.0), Inches(5.0), Inches(5.2), Inches(1.6))
    tf_top = tb_top.text_frame
    tf_top.word_wrap = True
    p_t = tf_top.paragraphs[0]
    p_t.text = "Top Predictive Symptoms (Feature Importance):"
    p_t.font.size = Pt(12)
    p_t.font.bold = True
    p_t.font.color.rgb = ACCENT_EMERALD

    p_feat = tf_top.add_paragraph()
    p_feat.text = "1. headache (1.88%)  2. vomiting (1.67%)  3. sharp abdominal pain (1.59%)\n4. cough (1.41%)  5. sharp chest pain (1.40%)  6. fever (1.26%)"
    p_feat.font.size = Pt(10)
    p_feat.font.color.rgb = TEXT_MUTED
    p_feat.space_before = Pt(4)

    # Right: Viva Discussion
    add_card(s13, 6.8, 1.8, 5.733, 5.0)
    tb_s13_r = s13.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf13_r = tb_s13_r.text_frame
    tf13_r.word_wrap = True

    p = tf13_r.paragraphs[0]
    p.text = "Why the Comparison is Not Apples-to-Apples"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_AMBER

    viva_points = [
        ("Class Cardinality: ", "NLP predicts across 24 classes (random baseline = 4.17%), while ML predicts across 673 classes (random baseline = 0.15%). An 81.6% accuracy across 673 diseases is exceptionally strong."),
        ("Data Sparsity: ", "Symptom2Disease is perfectly balanced (50 rows/class). The 673-disease dataset is highly sparse, causing rare diseases to challenge macro recall."),
        ("Feature Information Density: ", "Structured data eliminates syntactic noise and misspellings, whereas NLP captures colloquial patient phrasing."),
        ("Clinical Responsibility: ", "AuraDX is strictly a decision-support and triage prototype; it does not replace certified doctors nor prescribe medications.")
    ]
    for h, d in viva_points:
        p = tf13_r.add_paragraph()
        p.text = "• " + h + d
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(6)

    # ==========================================
    # SLIDE 14: Conclusion & Future Scope
    # ==========================================
    s14 = prs.slides.add_slide(blank_slide_layout)
    apply_bg(s14)
    add_header(s14, "Conclusion & Future Roadmap", "Summary & Next Steps")

    # Left: Conclusion
    add_card(s14, 0.8, 1.8, 5.6, 5.0)
    tb_s14_l = s14.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6))
    tf14_l = tb_s14_l.text_frame
    tf14_l.word_wrap = True

    p = tf14_l.paragraphs[0]
    p.text = "Project Summary & Achievements"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    concl_points = [
        "Successfully developed and unified a dual-paradigm symptom classification system bridging unstructured NLP and structured ML.",
        "Demonstrated 96.0% accuracy on natural language symptom descriptions and 81.6% accuracy across 673 medical conditions.",
        "Solved multi-class memory bottlenecks through 160x Joblib gzip compression (reducing model footprint to 41.4 MB).",
        "Built and deployed an intuitive, dark-mode glassmorphic Flask web dashboard for real-time outpatient triage assistance."
    ]
    for item in concl_points:
        p = tf14_l.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(10)

    # Right: Future Scope
    add_card(s14, 6.8, 1.8, 5.733, 5.0)
    tb_s14_r = s14.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf14_r = tb_s14_r.text_frame
    tf14_r.word_wrap = True

    p = tf14_r.paragraphs[0]
    p.text = "Future Research & Expansion"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_EMERALD

    future_points = [
        ("Clinical Transformers: ", "Integrate pretrained models like Bio_ClinicalBERT or PubMedBERT to capture complex negation (e.g., 'no fever') and contextual dependencies."),
        ("Hospital EHR Integration: ", "Connect with HL7 / FHIR protocol APIs to ingest patient medical history directly from hospital Electronic Health Records."),
        ("Multi-Lingual Clinical Triage: ", "Expand the NLP pipeline to support vernacular Indian languages (Hindi, Marathi) for rural healthcare access."),
        ("Severity Triage Score: ", "Incorporate clinical acuity scoring (ESI - Emergency Severity Index) to categorize triage urgency (Red, Yellow, Green).")
    ]
    for h, d in future_points:
        p = tf14_r.add_paragraph()
        p.text = "• " + h + d
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

    # Save presentation
    output_path = "AuraDX_Project_Presentation.pptx"
    prs.save(output_path)
    print(f"[SUCCESS] Presentation generated successfully at: {output_path}")

if __name__ == "__main__":
    create_deck()
