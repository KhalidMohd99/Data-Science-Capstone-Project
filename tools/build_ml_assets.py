# -*- coding: utf-8 -*-
"""Rename confusion matrices to model names, write the accuracy report, and build
assets/ml/accuracy_comparison.png from the exact values printed in the notebook."""
import io
import os
import shutil
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = r"C:\Users\khali\Downloads\Claud_IBM-capstone-story"
ML = os.path.join(ROOT, "assets", "ml")

# Exact values from the executed notebook (cells 44/55/65/75/80)
test_acc = {
    "Logistic\nRegression": 0.8333333333333334,
    "SVM": 0.8333333333333334,
    "Decision\nTree": 0.7777777777777778,
    "KNN": 0.8333333333333334,
}
cv_acc = {
    "Logistic\nRegression": 0.8464285714285713,
    "SVM": 0.8482142857142856,
    "Decision\nTree": 0.8767857142857143,
    "KNN": 0.8482142857142858,
}

# 1) rename confusion matrices (order of extraction == order of cells 46,57,67,77)
renames = {
    "01_confusion_matrix_cell46.png": "confusion_matrix_logistic_regression.png",
    "02_confusion_matrix_cell57.png": "confusion_matrix_svm.png",
    "03_confusion_matrix_cell67.png": "confusion_matrix_decision_tree.png",
    "04_confusion_matrix_cell77.png": "confusion_matrix_knn.png",
}
for old, new in renames.items():
    src, dst = os.path.join(ML, old), os.path.join(ML, new)
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"renamed {old} -> {new}")

# 2) accuracy report (exact notebook output)
report = """Model Test Accuracies:
Logistic Regression: 0.8333333333333334
SVM: 0.8333333333333334
Decision Tree: 0.7777777777777778
KNN: 0.8333333333333334

The best performing method on the test data is: Logistic Regression

Cross-validation accuracies (GridSearchCV best):
Logistic Regression: 0.8464285714285713  {'C': 0.01, 'penalty': 'l2', 'solver': 'lbfgs'}
SVM:                 0.8482142857142856  {'C': 1.0, 'gamma': 0.03162277660168379, 'kernel': 'sigmoid'}
Decision Tree:       0.8767857142857143  {'criterion': 'entropy', 'max_depth': 14, ...}
KNN:                 0.8482142857142858  {'algorithm': 'auto', 'n_neighbors': 10, 'p': 1}
"""
with open(os.path.join(ML, "accuracy_report.txt"), "w", encoding="utf-8") as f:
    f.write(report)
print("wrote accuracy_report.txt")

# 3) bar chart: model accuracy comparison (test + CV)
labels = list(test_acc.keys())
x = range(len(labels))
w = 0.38

fig, ax = plt.subplots(figsize=(9, 5.2), dpi=140)
b1 = ax.bar([i - w / 2 for i in x], [test_acc[k] for k in labels], w,
            label="Test accuracy", color="#0f62fe")
b2 = ax.bar([i + w / 2 for i in x], [cv_acc[k] for k in labels], w,
            label="Cross-validation accuracy", color="#8a3ffc")

ax.set_ylim(0, 1.0)
ax.set_ylabel("Accuracy", fontsize=12)
ax.set_title("Classification Model Accuracy Comparison (Falcon 9 landing prediction)",
             fontsize=14, fontweight="bold")
ax.set_xticks(list(x))
ax.set_xticklabels(labels, fontsize=11)
ax.legend(loc="lower right", fontsize=10)
ax.grid(axis="y", alpha=0.3)

for bars in (b1, b2):
    for r in bars:
        ax.annotate(f"{r.get_height():.3f}",
                    xy=(r.get_x() + r.get_width() / 2, r.get_height()),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", fontsize=9)

# highlight the winner
ax.annotate("best model", xy=(0, test_acc["Logistic\nRegression"]),
            xytext=(-10, 118), textcoords="offset points", fontsize=10,
            color="#0f62fe", fontweight="bold",
            arrowprops=dict(arrowstyle="->", color="#0f62fe"))

plt.tight_layout()
out = os.path.join(ML, "accuracy_comparison.png")
fig.savefig(out)
plt.close(fig)
print(f"saved accuracy_comparison.png ({os.path.getsize(out)//1024} KB)")

for f in sorted(os.listdir(ML)):
    print("  ", f)
