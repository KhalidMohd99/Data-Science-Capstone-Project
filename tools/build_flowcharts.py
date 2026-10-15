# -*- coding: utf-8 -*-
"""Generate flowcharts for the presentation."""
import matplotlib.pyplot as plt
import os

OUT = r"C:\Users\khali\Downloads\Claud_IBM-capstone-story\assets\flowcharts"
os.makedirs(OUT, exist_ok=True)
plt.rcParams['font.family'] = 'Segoe UI'
plt.rcParams['font.size'] = 9

# 1. Data collection pipeline (slide 7)
fig, ax = plt.subplots(figsize=(8.6, 4.2), dpi=160)
ax.axis('off')
txt = '''Project Objective → Problem Statement (Will Falcon 9 first stage land successfully?)
→ Data Sources: SpaceX REST API (v4) + Wikipedia HTML Tables
→ API Data Collection: get launches/cores/rockets → flatten & filter
→ Web Scraping: extract launch table → parse columns → clean
→ Merge / Normalize → Save as CSVs (dataset_part_1.csv, dataset_part_2.csv, spacex_web_scraped.csv)
→ Ready for EDA & Modeling'''
ax.text(0.02, 0.55, txt, va='center', ha='left', wrap=True, linespacing=1.4)
ax.set_title('Data Collection Pipeline', fontsize=10, fontweight='bold')
plt.tight_layout()
fig.savefig(os.path.join(OUT, 'data_collection_pipeline.png'), bbox_inches='tight')
plt.close(fig)

# 2. API flow (slide 8)
fig, ax = plt.subplots(figsize=(7.8, 4.0), dpi=160)
ax.axis('off')
txt = '''1. HTTP request to SpaceX API /launches/past (with params) → JSON
2. Parse response → extract cores, payloads, orbit, launch site, outcome, date
3. Build Pandas DataFrame (normalize nested JSON)
4. Handle missing values (imputation)
5. Save dataset_part_1.csv
6. Inspect → prepare for wrangling & feature engineering'''
ax.text(0.02, 0.55, txt, va='center', ha='left', wrap=True, linespacing=1.4)
ax.set_title('SpaceX REST API Collection Workflow', fontsize=10, fontweight='bold')
plt.tight_layout()
fig.savefig(os.path.join(OUT, 'api_workflow.png'), bbox_inches='tight')
plt.close(fig)

# 3. Scraping flow (slide 9)
fig, ax = plt.subplots(figsize=(7.8, 4.0), dpi=160)
ax.axis('off')
txt = '''1. Request Wikipedia page (List of Falcon 9/Heavy launches)
2. Parse HTML with BeautifulSoup
3. Locate the target HTML table
4. Extract table headers → apply extract_column_from_header
5. Parse rows → clean text (version, date/time, payload mass)
6. Build DataFrame → handle types
7. Export spacex_web_scraped.csv
8. Verify & export dataset_part_2.csv'''
ax.text(0.02, 0.55, txt, va='center', ha='left', wrap=True, linespacing=1.4)
ax.set_title('Web Scraping Workflow (Wikipedia)', fontsize=10, fontweight='bold')
plt.tight_layout()
fig.savefig(os.path.join(OUT, 'scraping_workflow.png'), bbox_inches='tight')
plt.close(fig)

# 4. Wrangling flow (slide 10)
fig, ax = plt.subplots(figsize=(7.8, 4.0), dpi=160)
ax.axis('off')
txt = '''1. Load datasets (API + scraped)
2. Explore structure (columns, dtypes, missing values)
3. Clean: drop irrelevant, convert dates, extract features (Year, Month)
4. One-hot encode categorical (LaunchSite, Orbit, LandingPad, Serial)
5. Filter Falcon 9 only → target Class (1=success, 0=failure)
6. Handle missing payload: impute with mean
7. Export dataset_part_2.csv & dataset_part_3.csv
8. Output ready for EDA & ML'''
ax.text(0.02, 0.55, txt, va='center', ha='left', wrap=True, linespacing=1.4)
ax.set_title('Data Wrangling Workflow', fontsize=10, fontweight='bold')
plt.tight_layout()
fig.savefig(os.path.join(OUT, 'wrangling_workflow.png'), bbox_inches='tight')
plt.close(fig)

# 5. ML pipeline (slide 15)
fig, ax = plt.subplots(figsize=(9.2, 4.8), dpi=160)
ax.axis('off')
txt = '''1. Prepare features/target from dataset_part_3.csv (One-hot + numeric)
2. Train/Test split (80%/20%) - stratified to preserve class balance
3. Feature scaling (StandardScaler) → avoid weight bias
4. Model training: Logistic Regression, SVM (RBF/Sigmoid), Decision Tree, KNN
5. Hyperparameter tuning via GridSearchCV (10-fold CV)
6. Evaluate on test set: Accuracy, Confusion Matrix, best params
7. Select best model (Logistic Regression) with test accuracy 0.8333
8. Validate & document results'''
ax.text(0.02, 0.55, txt, va='center', ha='left', wrap=True, linespacing=1.35)
ax.set_title('Predictive Analysis Pipeline (Classification)', fontsize=10, fontweight='bold')
plt.tight_layout()
fig.savefig(os.path.join(OUT, 'ml_pipeline.png'), bbox_inches='tight')
plt.close(fig)

print("flowcharts done")
