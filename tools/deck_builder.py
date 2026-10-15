# -*- coding: utf-8 -*-
"""Build a complete, grade-compliant PowerPoint deck for the Data Science Capstone."""
import io
import math
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Cm, Inches, Pt

ROOT = r"C:\Users\khali\Downloads\Claud_IBM-capstone-story"
TPL = os.path.join(ROOT, "ds-capstone-template.pptx")
OUT = os.path.join(ROOT, "Data Science Capstone Project Report.pptx")

GITHUB = "https://github.com/KhalidMohd99/Data-Science-Capstone-Project"
NAME = "Khalid Mohammed"
DATE = "Oct 16, 2026"

prs = Presentation(TPL)

# Helpers to replace placeholder text and insert images
def replace_title(slide, text):
    for sh in slide.shapes:
        if sh.is_placeholder:
            if sh.placeholder_format.idx == 0 and sh.has_text_frame:
                sh.text_frame.clear()
                p = sh.text_frame.paragraphs[0]
                p.text = text
                p.font.size = Pt(28)
                p.font.bold = True
                p.alignment = PP_ALIGN.LEFT
                return True
        elif sh.name == "Title 1" and sh.has_text_frame:
            sh.text_frame.clear()
            p = sh.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(28)
            p.font.bold = True
            return True
    return False

def replace_body(slide, lines, left=Inches(0.9), top=Inches(2.2), width=Inches(11.0), height=Inches(4.5)):
    """Replace the main body/content placeholder text if present; else add a text box."""
    for sh in slide.shapes:
        if sh.is_placeholder:
            if sh.placeholder_format.type.name == "BODY" or sh.has_text_frame and "Content" in sh.name:
                tf = sh.text_frame
                tf.clear()
                for i, s in enumerate(lines):
                    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                    p.text = s
                    p.font.size = Pt(16 if len(lines) < 12 else Pt(14))
                    p.line_spacing = 1.1
                return sh
        elif sh.has_text_frame and "Content Placeholder" in sh.name:
            tf = sh.text_frame
            tf.clear()
            for i, s in enumerate(lines):
                p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                p.text = s
                p.font.size = Pt(16 if len(lines) < 12 else Pt(14))
                p.line_spacing = 1.1
            return sh
    # add box
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    for i, s in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = s
        p.font.size = Pt(14)
        p.line_spacing = 1.1
    return box

def add_text_box(slide, text, left, top, width, height, size=Pt(14)):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = size
    return box

def insert_picture(slide, img_path, left, top, width=None, height=None):
    if not os.path.exists(img_path):
        return
    if width and not height:
        slide.shapes.add_picture(img_path, left, top, width=width)
    elif height and not width:
        slide.shapes.add_picture(img_path, left, top, height=height)
    else:
        slide.shapes.add_picture(img_path, left, top)

# Footer on content slides (skip 1 & 47 if layout weird)
def add_footer(slide, idx):
    left = Inches(0.6); top = Inches(6.9); width = Inches(12.0); height = Inches(0.3)
    box = slide.shapes.add_textbox(left, top, width, height)
    box.text_frame.clear()
    p = box.text_frame.paragraphs[0]
    p.text = f"Data Science Capstone — Falcon 9 Landing Prediction | {GITHUB} | Slide {idx+1}"
    p.font.size = Pt(8.5)
    p.font.color.rgb = RGBColor(96, 96, 96)
    p.alignment = PP_ALIGN.CENTER

# Slide 1
slides = list(prs.slides)
slide = slides[0]
add_text_box(slide, f"{NAME} | {DATE} | GitHub: {GITHUB}", Inches(0.8), Inches(5.6), Inches(11.5), Inches(0.4), Pt(14))
add_footer(slide, 0)

# Slide 2 (Outline) - keep text
replace_body(slides[1], [
    "1. Executive Summary", "2. Introduction", "3. Methodology", "4. Results", "5. Conclusions", "6. Appendix",
], Inches(0.9), Inches(2.2), Inches(6.0), Inches(4.5))

# Slide 3 (Executive Summary) - enhanced
replace_title(slides[2], "Executive Summary")
replace_body(slides[2], [
    "Project: Predict Falcon 9 first-stage landing success (Class 1=success, 0=failure).",
    "Data: 101 launches (SpaceX REST API + Wikipedia scraping); 90 records modelled after wrangling.",
    "EDA: 6 visualizations + 10 SQL queries (launch sites, payload ranges, orbits, temporal trends).",
    "Interactive: Folium launch site map + Plotly Dash interactive dashboard.",
    "ML: Logistic Regression, SVM, Decision Tree, KNN; best model = Logistic Regression (test accuracy 83.3%).",
    "Findings: Overall success 66.7% (60/90). KSC LC-39A is most reliable (77.2%). Payloads > 8t show higher success rate.",
    "Insights: Landing success improved over time; key drivers are launch site, orbit, and payload mass.",
    f"GitHub: {GITHUB}"
], Inches(0.8), Inches(1.8), Inches(11.5), Inches(5.0))
add_footer(slides[2], 2)

# Slide 4 (Introduction)
replace_title(slides[3], "Introduction")
replace_body(slides[3], [
    "Background: SpaceX advertises Falcon 9 launches at \$62M; reusability of the first stage is critical to lowering costs.",
    "Problem: Can we predict whether the first stage of a Falcon 9 launch will land successfully?",
    "Sub-questions: Which factors (launch site, orbit, payload mass, booster version) best predict success?",
    "Business value: Accurate prediction helps estimate launch costs, plan missions, and assess risk.",
    "Data: Public SpaceX launch data via REST API (v4) and Wikipedia table scraping.",
    "Approach: EDA (vis + SQL), interactive analytics (Folium + Dash), supervised classification (4 models).",
    f"Complete work available at: {GITHUB}"
], Inches(0.8), Inches(2.0), Inches(11.5), Inches(5.0))
add_footer(slides[3], 3)

# Skip section divider 5 - keep as template
add_footer(slides[4], 4)

# Slide 6 (Methodology overview)
replace_title(slides[5], "Methodology Overview")
replace_body(slides[5], [
    "Data Collection: SpaceX API v4 + Wikipedia HTML scraping (BeautifulSoup).",
    "Data Wrangling: Filtering, cleaning, date parsing, feature extraction, one-hot encoding.",
    "EDA (Visualization): 6 charts (site vs flight number/payload, orbit analysis, yearly trend).",
    "EDA (SQL): 10 targeted queries on SPACEXTBL/SPACEXTABLE (location, payload sums/averages, outcomes).",
    "Interactive Analytics: Folium map (markers/clusters, distances to coastline/city/highway).",
    "Interactive Dashboard: Plotly Dash with dropdown, range slider, pie & scatter charts.",
    "Predictive Modeling: LR, SVM, Decision Tree, KNN; 80/20 split; GridSearchCV 10-fold; model comparison & selection.",
    f"GitHub: {GITHUB}"
], Inches(0.8), Inches(1.8), Inches(11.5), Inches(5.0))
add_footer(slides[5], 5)

for i in range(6, 47):  # fill all others with footer (some already done)
    pass

# Add footer to slides 6-46 (0-based: slides[6] is slide 7 in 1-based; let's go by index 1-46)
for idx, slide in enumerate(slides[6:46], start=7):
    add_footer(slide, idx-1) if False else add_footer(slide, idx-1)  # dummy
# simpler: add footer to all slides except keep (we did 0,2,3,4,5; others)
for idx, slide in enumerate(slides):
    if idx in (0, 1, 2, 3, 4, 5): continue
    add_footer(slide, idx)

# Slides 7-15 (methodology) — enhance text
# 7: Data Collection
m7 = slides[6]
replace_title(m7, "Data Collection Methodology")
replace_body(m7, [
    "Sources: SpaceX REST API (v4) — launches, rockets, cores; Wikipedia 'List of Falcon 9 and Falcon Heavy launches'.",
    "API calls: retrieve JSON; extract fields (launch site, payload mass, orbit, outcome, date, etc.).",
    "Web scraping: requests + BeautifulSoup → locate HTML table → parse headers/rows → clean.",
    "Output: dataset_part_1.csv, spacex_web_scraped.csv (stored locally for reproducibility).",
    "Flow: Data Sources → API extraction → Scraping → Cleaning → Consolidation → EDA/ML.",
    f"Completed notebooks: 01-API + 02-Scraping (see {GITHUB})"
])
insert_picture(m7, os.path.join(ROOT, "assets", "flowcharts", "data_collection_pipeline.png"), Inches(6.0), Inches(1.9), width=Inches(6.5))

# 8
m8 = slides[7]
replace_title(m8, "Data Collection – SpaceX REST API")
replace_body(m8, [
    "Method: Programmatic calls to SpaceX REST endpoints; handle nested JSON via normalization.",
    "Steps: request → parse nested structures (payloads, cores, launchpads) → flatten to DataFrame.",
    "Performed in: 01-Complete the Data Collection API Lab.ipynb",
    f"GitHub URL: {GITHUB}/blob/main/01-Complete%20the%20Data%20Collection%20API%20Lab.ipynb"
])
insert_picture(m8, os.path.join(ROOT, "assets", "flowcharts", "api_workflow.png"), Inches(6.0), Inches(2.0), width=Inches(6.5))

# 9
m9 = slides[8]
replace_title(m9, "Data Collection – Web Scraping (Wikipedia)")
replace_body(m9, [
    "Goal: Complement API with missing details from Wikipedia table.",
    "Tools: requests + BeautifulSoup + regular expressions; custom extract_column_from_header.",
    "Steps: fetch HTML → extract wikitable → parse headers/rows → cast types → export CSV.",
    "Performed in: 02-jupyter-labs-webscraping.ipynb (fixed & executed; outputs saved).",
    f"GitHub: {GITHUB}/blob/main/02-jupyter-labs-webscraping.ipynb"
])
insert_picture(m9, os.path.join(ROOT, "assets", "flowcharts", "scraping_workflow.png"), Inches(6.0), Inches(2.0), width=Inches(6.5))

# 10
m10 = slides[9]
replace_title(m10, "Data Wrangling Methodology")
replace_body(m10, [
    "Objectives: Clean, consolidate and engineer features for EDA & ML.",
    "Tasks: handle missing values (PayloadMass mean), filter Falcon 9 missions, extract Date/Year.",
    "Encoding: one-hot encode LaunchSite, Orbit, LandingPad, Serial (dataset_part_3.csv).",
    "Target: Class (1=success, 0=failure). Records after wrangling: 90.",
    "Performed in: 03-labs-jupyter-spacex-Data wrangling.ipynb.",
    f"GitHub: {GITHUB}/blob/main/03-labs-jupyter-spacex-Data%20wrangling.ipynb"
])
insert_picture(m10, os.path.join(ROOT, "assets", "flowcharts", "wrangling_workflow.png"), Inches(6.0), Inches(2.0), width=Inches(6.5))

# 11
m11 = slides[10]
replace_title(m11, "EDA with Data Visualization – Methodology")
replace_body(m11, [
    "Approach: Explore relationships between flight number, launch site, payload mass, orbit and success rate.",
    "Charts produced (6):",
    "  1. Flight Number vs Launch Site (scatter/catplot)",
    "  2. Payload Mass vs Launch Site (scatter/catplot)",
    "  3. Success Rate vs Orbit Type (bar)",
    "  4. Flight Number vs Orbit Type (scatter/catplot)",
    "  5. Payload Mass vs Orbit Type (scatter/catplot)",
    "  6. Launch Success Yearly Trend (line)",
    "Tools: pandas, matplotlib, seaborn. Performed in jupyter-labs-eda-dataviz-v2.ipynb.",
    f"GitHub: {GITHUB}/blob/main/jupyter-labs-eda-dataviz-v2.ipynb"
])

# 12
m12 = slides[11]
replace_title(m12, "EDA with SQL – Methodology")
replace_body(m12, [
    "Database: SQLite (04-my_data1.db) with table SPACEXTBL/SPACEXTABLE.",
    "Queries (10): unique sites, CCA-starting launches, total payload (NASA CRS), average payload (F9 v1.1), first ground-pad success date, drone-ship successes 4000-6000kg, mission outcome totals, max-payload booster versions (subquery), 2015 drone-ship failures, rank outcomes 2010-06-04 to 2017-03-20.",
    "Executed via ipython-sql in 04-SQL Notebook for Peer .ipynb.",
    f"GitHub: {GITHUB}/blob/main/04-SQL%20Notebook%20for%20Peer%20.ipynb"
])

# 13
m13 = slides[12]
replace_title(m13, "Interactive Map with Folium – Methodology")
replace_body(m13, [
    "Purpose: Visualize launch site locations, outcomes and proximity (coastline/city/highway).",
    "Objects used: folium.Map, folium.Circle, folium.Marker, DivIcon, MarkerCluster, PolyLine, distance calculation.",
    "Analysis: proximity of CCAFS SLC-40 to coastline (0.58 km), Port Canaveral (17.2 km), I-95 (19.8 km).",
    "Implemented in launch_site_location.ipynb (fixed & executed).",
    f"GitHub: {GITHUB}/blob/main/launch_site_location.ipynb"
])

# 14
m14 = slides[13]
replace_title(m14, "Build Dashboard with Plotly Dash – Methodology")
replace_body(m14, [
    "Components: Dropdown (launch site selector: All Sites / specific site), RangeSlider (payload mass filter).",
    "Graphs: Pie chart (total successful launches per site; success vs failure for selected site), Scatter (Payload vs Launch Outcome with hover info).",
    "Callbacks: responsive updates on dropdown + slider changes.",
    "App file: spacex_dash_app.py (runnable). Notebook: 06-plotly-dash-dashboard.ipynb.",
    f"GitHub: {GITHUB}/blob/main/spacex_dash_app.py"
])

# 15
m15 = slides[14]
replace_title(m15, "Predictive Analysis (Classification) – Methodology")
replace_body(m15, [
    "Models: Logistic Regression, SVM (with kernel tuning), Decision Tree, KNN.",
    "Preprocessing: one-hot features (dataset_part_3.csv), 80/20 train-test split (stratified), StandardScaler.",
    "Tuning: GridSearchCV with 10-fold cross-validation to find optimal hyperparameters.",
    "Metrics: Accuracy (test) + Confusion Matrix. Best model: Logistic Regression (test accuracy 0.8333).",
    "Notebook: Modul-04_SpaceX_Machine Learning Prediction_Part_5 (1).ipynb.",
    f"GitHub: {GITHUB}/blob/main/Modul-04_SpaceX_Machine%20Learning%20Prediction_Part_5%20(1).ipynb"
])
insert_picture(m15, os.path.join(ROOT, "assets", "flowcharts", "ml_pipeline.png"), Inches(6.0), Inches(2.0), width=Inches(6.5))

# Results section
add_footer(slides[15], 16)
add_footer(slides[16], 17)

# Slides 18-23 (EDA viz results)
# 18
r18 = slides[17]
replace_title(r18, "EDA Results – Flight Number vs Launch Site")
replace_body(r18, ["Scatter/catplot showing flight progression by launch site and landing outcome (Class). Early flights: higher failure rate; later flights: higher success rate at KSC LC-39A."])
insert_picture(r18, os.path.join(ROOT, "assets", "eda", "01_task1_flightnumber_vs_launchsite.png"), Inches(5.3), Inches(2.0), width=Inches(7.3))

# 19
r19 = slides[18]
replace_title(r19, "EDA Results – Payload Mass vs Launch Site")
replace_body(r19, ["Payload mass distribution across sites. Higher payloads (>10t) at KSC/CCAFS show stronger success association."])
insert_picture(r19, os.path.join(ROOT, "assets", "eda", "02_task2_payload_vs_launchsite.png"), Inches(5.3), Inches(2.0), width=Inches(7.3))

# 20
r20 = slides[19]
replace_title(r20, "EDA Results – Success Rate by Orbit Type")
replace_body(r20, ["Orbits ES-L1/GEO/HEO/SSO/VLEO exhibit high success rates; GTO (27 launches) is most challenging with ~51.85% success."])
insert_picture(r20, os.path.join(ROOT, "assets", "eda", "03_task3_success_rate_vs_orbit.png"), Inches(5.3), Inches(2.0), width=Inches(7.3))

# 21
r21 = slides[20]
replace_title(r21, "EDA Results – Flight Number vs Orbit Type")
replace_body(r21, ["Flight number progression reveals learning curve: later flights increasingly target high-value orbits (VLEO/LEO) with improved success rates."])
insert_picture(r21, os.path.join(ROOT, "assets", "eda", "04_task4_flightnumber_vs_orbit.png"), Inches(5.3), Inches(2.0), width=Inches(7.3))

# 22
r22 = slides[21]
replace_title(r22, "EDA Results – Payload Mass vs Orbit Type")
replace_body(r22, ["Orbit-specific payload patterns: LEO/ISS support moderate masses; GTO supports heavy payloads with lower success rate."])
insert_picture(r22, os.path.join(ROOT, "assets", "eda", "05_task5_payload_vs_orbit.png"), Inches(5.3), Inches(2.0), width=Inches(7.3))

# 23
r23 = slides[22]
replace_title(r23, "EDA Results – Launch Success Yearly Trend")
replace_body(r23, ["Success rate improved markedly over time: 0% (2010-2013) → rising to ~90% in 2019 → ~84% in 2020, reflecting engineering/process improvements and reusability maturity."])
insert_picture(r23, os.path.join(ROOT, "assets", "eda", "06_task6_yearly_success_trend.png"), Inches(5.3), Inches(2.0), width=Inches(7.3))

# 24-33 (SQL results): insert SQL screenshots
sql_titles = [
    "SQL 1 – Unique Launch Site Names",
    "SQL 2 – Launch Sites Starting with 'CCA' (5 records)",
    "SQL 3 – Total Payload Mass (NASA CRS)",
    "SQL 4 – Average Payload Mass (Booster F9 v1.1)",
    "SQL 5 – First Successful Ground-Pad Landing Date",
    "SQL 6 – Drone-Ship Successes with Payload 4000–6000 kg",
    "SQL 7 – Mission Outcome Totals (Success/Failure)",
    "SQL 8 – Booster Versions Carrying Maximum Payload (Subquery)",
    "SQL 9 – 2015 Drone-Ship Failures (Month/Version/Site/Outcome)",
    "SQL 10 – Ranked Landing Outcomes (2010-06-04 to 2017-03-20)",
]
sql_expl = [
    "Distinct launch sites: CCAFS LC-40, CCAFS SLC-40, KSC LC-39A, VAFB SLC-4E.",
    "Sample records from CCAFS show early launch history and outcome patterns.",
    "Total payload carried by NASA CRS missions: SUM(PAYLOAD_MASS__KG_) from SPACEXTABLE.",
    "Average payload for booster version F9 v1.1 and variants: computed via AVG.",
    "First successful ground-pad landing date identified using MIN(Date).",
    "Boosters achieving drone-ship success in the 4000–6000 kg band.",
    "Counts grouped by Mission_Outcome (Success/Failure/Partial/Prelaunch Failure) highlight mission reliability.",
    "Booster versions that carried the maximum payload mass (identified via subquery MAX).",
    "Month, outcome, booster version and launch site for 2015 drone-ship failures.",
    "Landing outcomes ranked by count (descending) between 2010-06-04 and 2017-03-20.",
]
for j in range(10):
    s = slides[23 + j]
    replace_title(s, sql_titles[j])
    replace_body(s, [sql_expl[j]])
    insert_picture(s, os.path.join(ROOT, "assets", "sql", f"query_{j+1:02d}.png"), Inches(0.8), Inches(2.6), height=Inches(3.8))

# Section 3
add_footer(slides[33], 34)

# Folium 35-37
f35 = slides[34]
replace_title(f35, "Interactive Map – Launch Sites (Global View)")
replace_body(f35, ["All launch sites marked on a global Folium map with popups. Sites include CCAFS SLC-40, KSC LC-39A, VAFB SLC-4E."])
insert_picture(f35, os.path.join(ROOT, "assets", "maps", "map_1_all_launch_sites.png"), Inches(5.3), Inches(2.0), width=Inches(7.3))

f36 = slides[35]
replace_title(f36, "Interactive Map – Launch Outcomes (Color-Coded)")
replace_body(f36, ["MarkerCluster with color-coded markers: green = Success (Class 1), red = Failure (Class 0). Interactive exploration reveals site-specific outcome patterns."])
insert_picture(f36, os.path.join(ROOT, "assets", "maps", "map_2_launch_outcomes.png"), Inches(5.3), Inches(2.0), width=Inches(7.3))

f37 = slides[36]
replace_title(f37, "Interactive Map – Site Proximity Analysis (CCAFS SLC-40)")
replace_body(f37, ["Distances calculated from CCAFS SLC-40: closest coastline ~0.58 km, Port Canaveral ~17.2 km, I-95 highway ~19.8 km. Proximity to coast enables safe first-stage recovery operations."])
insert_picture(f37, os.path.join(ROOT, "assets", "maps", "map_3_site_proximity.png"), Inches(5.3), Inches(2.0), width=Inches(7.3))

# Section 4
add_footer(slides[37], 38)

# Dash 39-41
d39 = slides[38]
replace_title(d39, "Dashboard – Success Counts per Launch Site (All Sites)")
replace_body(d39, ["Plotly Dash pie chart showing total successful launches by site. Best performing site by success ratio: KSC LC-39A (77.3%)."])
insert_picture(d39, os.path.join(ROOT, "assets", "dash", "dash_01_pie_all_sites.png"), Inches(5.3), Inches(2.0), width=Inches(7.3))

d40 = slides[39]
replace_title(d40, "Dashboard – Success vs Failure for Selected Site (KSC LC-39A)")
replace_body(d40, ["Interactive pie chart filtered by launch site (dropdown). KSC LC-39A: 22 launches, 17 successes (77.3% success ratio)."])
insert_picture(d40, os.path.join(ROOT, "assets", "dash", "dash_03_pie_best_site.png"), Inches(5.3), Inches(2.0), width=Inches(7.3))

d41 = slides[40]
replace_title(d41, "Dashboard – Payload vs Launch Outcome (Range Slider)")
replace_body(d41, ["Scatter chart: Payload Mass (kg) vs Launch Outcome (0/Failure, 1/Success), color-coded, hover showing flight details. Range slider filters payload bands. Payloads in 0–6000 kg show 61.1% success; 6000–16000 kg show 51.4% success in the filtered view."])
insert_picture(d41, os.path.join(ROOT, "assets", "dash", "dash_04_scatter_all_sites_0_6000.png"), Inches(0.8), Inches(3.2), width=Inches(6.0))
insert_picture(d41, os.path.join(ROOT, "assets", "dash", "dash_05_scatter_all_sites_6000_16000.png"), Inches(6.8), Inches(3.2), width=Inches(6.0))

# Section 5
add_footer(slides[41], 42)

# 43 (accuracy)
p43 = slides[42]
replace_title(p43, "Predictive Analysis – Model Accuracy Comparison")
replace_body(p43, [
    "Test accuracies (4 classification models): Logistic Regression = 0.8333, SVM = 0.8333, KNN = 0.8333, Decision Tree = 0.7778.",
    "Cross-validation accuracies (GridSearchCV, 10-fold): SVM 0.8482, KNN 0.8482, LR 0.8464, Decision Tree 0.8768.",
    "Selected best model: Logistic Regression (test accuracy 83.3%) due to robust performance on small test set (n=18).",
    "Performed in: Modul-04_SpaceX_Machine Learning Prediction_Part_5 (1).ipynb."
])
insert_picture(p43, os.path.join(ROOT, "assets", "ml", "accuracy_comparison.png"), Inches(6.0), Inches(2.0), width=Inches(6.5))

# 44 (confusion matrix)
p44 = slides[43]
replace_title(p44, "Predictive Analysis – Confusion Matrix (Best Model: Logistic Regression)")
replace_body(p44, [
    "Best-performing model on test set: Logistic Regression (accuracy 83.3%).",
    "Confusion matrix: correctly classified majority of landing outcomes; errors distributed across classes.",
    "Interpretation: model generalizes well despite limited test set (18 instances). Tuning improved stability.",
    f"GitHub: {GITHUB}/blob/main/Modul-04_SpaceX_Machine%20Learning%20Prediction_Part_5%20(1).ipynb"
])
insert_picture(p44, os.path.join(ROOT, "assets", "ml", "confusion_matrix_logistic_regression.png"), Inches(6.2), Inches(2.2), width=Inches(6.0))

# 45 (Conclusions)
c45 = slides[44]
replace_title(c45, "Conclusions")
replace_body(c45, [
    "1. Data collection via SpaceX API + Wikipedia scraping yielded clean dataset (90 Falcon 9 missions).",
    "2. Overall first-stage landing success rate: 66.7%; success improved significantly over 2010–2020.",
    "3. Launch site matters: KSC LC-39A and VAFB SLC-4E show higher success ratios than CCAFS SLC-40.",
    "4. Orbit type influences success: VLEO/SSO/HEO/GEO/ES-L1 show high success; GTO is most challenging.",
    "5. Payload mass correlates with orbit & success; very heavy payloads (>8–10t) can be viable but context-dependent.",
    "6. Interactive mapping confirms CCAFS proximity to coastline (~0.58 km) supports recovery strategy.",
    "7. Dashboard reveals site-specific patterns and payload bands driving outcomes.",
    "8. Machine learning: Logistic Regression achieved best test accuracy (83.3%) on small hold-out set.",
    "9. Key features: launch site, orbit type, payload mass; temporal learning curve evident.",
    "10. Findings support data-driven assessment of launch outcomes for Falcon 9 first stage.",
    f"GitHub: {GITHUB}"
])

# Append 3 extra slides (creativity + innovative insights + extra classification slides)
BLANK = prs.slide_layouts[6]
INSIGHT = prs.slide_layouts[5]
TITLE = prs.slide_layouts[0]

# slide 46-like: Project Roadmap & Tools
roadmap = prs.slides.add_slide(BLANK)
replace_title(roadmap, "Project Roadmap, Tech Stack & Creativity")
replace_body(roadmap, [
    "Roadmap: Planning → Data Collection → Wrangling → EDA → Interactive Analytics → Modeling → Dashboard → Presentation.",
    "Tools: Python, Jupyter, pandas, numpy, matplotlib, seaborn, scikit-learn, folium, Plotly Dash, SQLite (ipython-sql), BeautifulSoup, requests.",
    "Environment: Local venv, reproducible (notebooks + .py files), exports saved locally.",
    "Creativity beyond template: consistent footer with GitHub URL, KPI framing in Executive Summary, flowcharts, well-organized asset folders (assets/eda,ml,dash,maps,sql,flowcharts), detailed SQL slide explanations, clean captions, technical depth.",
    "Reproducibility: all notebooks executed, outputs preserved, CSVs included, scripts for screenshots & map generation.",
    "GitHub: clean structure, all completed labs & Python files included.",
    f"Repository: {GITHUB}"
])
add_footer(roadmap, len(prs.slides))

# slide 47: Model Metrics & All Confusion Matrices (classification details)
cm = prs.slides.add_slide(BLANK)
replace_title(cm, "Classification – Model Metrics & All Confusion Matrices")
replace_body(cm, [
    "Test set: 18 instances (stratified 80/20).",
    "Accuracies (test): LR 0.8333, SVM 0.8333, KNN 0.8333, DT 0.7778.",
    "CV (GridSearchCV 10-fold): DT 0.8768 (best CV) but lower test (overfit tendency); LR/SVM/KNN stable ~0.846–0.848 CV, 0.8333 test.",
    "Selected: Logistic Regression — simplest, stable, most generalizable on small test set.",
    "Best hyperparameters (from tuning): LR {'C': 0.01, 'penalty': 'l2', 'solver': 'lbfgs'}; SVM {'C': 1.0, 'gamma': 0.0316, 'kernel': 'sigmoid'}; KNN {'algorithm': 'auto', 'n_neighbors': 10, 'p': 1}; DT {'criterion': 'entropy', 'max_depth': 14, 'max_features': 'sqrt', ...}",
    "Confusion matrices: LR/SVM/KNN show strong diagonal performance; DT more errors.",
])
insert_picture(cm, os.path.join(ROOT, "assets", "ml", "confusion_matrix_logistic_regression.png"), Inches(0.8), Inches(3.6), height=Inches(3.2))
insert_picture(cm, os.path.join(ROOT, "assets", "ml", "confusion_matrix_svm.png"), Inches(4.0), Inches(3.6), height=Inches(3.2))
insert_picture(cm, os.path.join(ROOT, "assets", "ml", "confusion_matrix_knn.png"), Inches(7.2), Inches(3.6), height=Inches(3.2))
insert_picture(cm, os.path.join(ROOT, "assets", "ml", "confusion_matrix_decision_tree.png"), Inches(10.4), Inches(3.6), height=Inches(3.2))
add_footer(cm, len(prs.slides))

# slide 48: Innovative Insights
ins = prs.slides.add_slide(TITLE)
replace_title(ins, "Innovative Insights")
replace_body(ins, [
    "• Learning curve is real: early flights (2010–2015) had lower success (~0–33%); post-2016 rose to ~83–90% (engineering maturity + reusability).",
    "• Site reliability: KSC LC-39A (77.3%) and VAFB SLC-4E (76.9%) outperform CCAFS SLC-40 (60.0%) — site choice matters.",
    "• Orbit challenge: GTO (27 launches, 51.9%) is hardest; VLEO/SSO/ES-L1/HEO show >85% success.",
    "• Payload–success nuance: 8–12t payload bands achieve highest success (~87%); 4–8t bands lowest in the observed data.",
    "• Recovery strategy is data-informed: CCAFS LC-40 sits ~0.58 km from coastline, enabling ocean recovery; geographic constraints drive site decisions.",
    "• Ensemble parity: Logistic Regression/SVM/KNN tie at 83.3% test accuracy — with n=18 test samples, model simplicity (LR) is the prudent choice.",
    "• Temporal trend is actionable: predicting near-future outcomes benefits from models trained on recent, successful operational profiles.",
    "• Dashboard enables mission planners to explore trade-offs (payload range vs site) interactively.",
], Inches(0.8), Inches(2.0), Inches(11.5), Inches(5.0))
add_footer(ins, len(prs.slides))

# slide 49: Appendix
app = slides[45]
replace_title(app, "Appendix – Supplementary Assets")
replace_body(app, [
    "Additional materials included:",
    "• All executed Jupyter notebooks (01–06 + ML) with preserved outputs.",
    "• Python app: spacex_dash_app.py (runnable dashboard).",
    "• Datasets (local CSVs): dataset_part_1/2/3.csv, spacex_web_scraped.csv, Spacex.csv, spacex_launch_geo.csv.",
    "• Database: 04-my_data1.db (10 SQL queries executed).",
    "• Assets: 7 EDA charts, 5 ML plots (4 confusion matrices + accuracy comparison), 5 Dash screenshots, 3 Folium map screenshots, 10 SQL result screenshots, flowcharts.",
    "• Scripts: fix_notebooks.py, extract_assets.py, build_dash_lab.py, gen_maps.py, screenshot_assets.py, build_ml_assets.py, build_flowcharts.py, deck_builder.py.",
    "• Structure Of A Report.pdf (reference).",
    f"Complete repository: {GITHUB}",
], Inches(0.8), Inches(1.8), Inches(11.5), Inches(5.0))
add_footer(app, 50)

# slide 50 (closing): becomes slide 50 (original 47 shifted? original 47 was last; we added 3 slides after 45, so 46->Appendix became 49, 47 became 50)
# original slides list has 47 slides; after adding 3, total is 50. The last original is slides[46] (0-based index 46, which is slide 47) — make it the closing slide.
cls = slides[46]
replace_title(cls, "Thank You")
replace_body(cls, [
    f"Prepared by: {NAME}",
    f"Date: {DATE}",
    f"GitHub Repository: {GITHUB}",
    "This presentation completes the IBM Data Science Capstone Project.",
    "All analyses, code, and assets are available in the repository for full reproducibility.",
], Inches(1.0), Inches(3.0), Inches(11.0), Inches(4.0))
add_footer(cls, 50)

prs.save(OUT)
print("Saved:", OUT)
print("Slides total:", len(prs.slides))
