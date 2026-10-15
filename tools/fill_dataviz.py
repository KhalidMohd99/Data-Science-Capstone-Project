# -*- coding: utf-8 -*-
"""Fill the TODO solution cells of jupyter-labs-eda-dataviz-v2.ipynb (IBM capstone)."""
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

NB = r"C:\Users\khali\Downloads\Claud_IBM-capstone-story\jupyter-labs-eda-dataviz-v2.ipynb"

# cell index -> (expected marker that must be present, new source lines)
SOLUTIONS = {
    25: (  # TASK 1: Flight Number vs Launch Site
        "y axis to be the launch site, and hue to be the class value",
        [
            "# Plot a scatter point chart with x axis to be Flight Number and y axis to be the launch site, and hue to be the class value\n",
            "sns.catplot(y=\"LaunchSite\", x=\"FlightNumber\", hue=\"Class\", data=df, aspect=5)\n",
            "plt.xlabel(\"Flight Number\", fontsize=20)\n",
            "plt.ylabel(\"Launch Site\", fontsize=20)\n",
            "plt.title(\"Flight Number vs. Launch Site\", fontsize=25)\n",
            "plt.show()\n",
        ],
    ),
    29: (  # TASK 2: Payload vs Launch Site
        "Pay Load Mass (kg) and y axis to be the launch site",
        [
            "# Plot a scatter point chart with x axis to be Pay Load Mass (kg) and y axis to be the launch site, and hue to be the class value\n",
            "sns.catplot(y=\"LaunchSite\", x=\"PayloadMass\", hue=\"Class\", data=df, aspect=5)\n",
            "plt.xlabel(\"Payload Mass (kg)\", fontsize=20)\n",
            "plt.ylabel(\"Launch Site\", fontsize=20)\n",
            "plt.title(\"Payload vs. Launch Site\", fontsize=25)\n",
            "plt.show()\n",
        ],
    ),
    34: (  # TASK 3: Success rate of each orbit type (bar chart)
        "groupby method on Orbit column",
        [
            "# HINT use groupby method on Orbit column and get the mean of Class column\n",
            "orbit_success_rate = df.groupby(\"Orbit\")[\"Class\"].mean().reset_index()\n",
            "plt.figure(figsize=(12, 6))\n",
            "sns.barplot(x=\"Orbit\", y=\"Class\", data=orbit_success_rate, order=orbit_success_rate.sort_values(\"Class\", ascending=False)[\"Orbit\"])\n",
            "plt.xlabel(\"Orbit Type\", fontsize=15)\n",
            "plt.ylabel(\"Success Rate\", fontsize=15)\n",
            "plt.title(\"Success Rate vs. Orbit Type\", fontsize=20)\n",
            "plt.ylim(0, 1.05)\n",
            "plt.xticks(rotation=45, ha=\"right\")\n",
            "plt.tight_layout()\n",
            "plt.show()\n",
        ],
    ),
    38: (  # TASK 4: Flight Number vs Orbit type
        "x axis to be FlightNumber and y axis to be the Orbit",
        [
            "# Plot a scatter point chart with x axis to be FlightNumber and y axis to be the Orbit, and hue to be the class value\n",
            "sns.catplot(y=\"Orbit\", x=\"FlightNumber\", hue=\"Class\", data=df, aspect=5)\n",
            "plt.xlabel(\"Flight Number\", fontsize=20)\n",
            "plt.ylabel(\"Orbit\", fontsize=20)\n",
            "plt.title(\"Flight Number vs. Orbit Type\", fontsize=25)\n",
            "plt.show()\n",
        ],
    ),
    42: (  # TASK 5: Payload vs Orbit type
        "x axis to be Payload and y axis to be the Orbit",
        [
            "# Plot a scatter point chart with x axis to be Payload and y axis to be the Orbit, and hue to be the class value\n",
            "sns.catplot(y=\"Orbit\", x=\"PayloadMass\", hue=\"Class\", data=df, aspect=5)\n",
            "plt.xlabel(\"Payload Mass (kg)\", fontsize=20)\n",
            "plt.ylabel(\"Orbit\", fontsize=20)\n",
            "plt.title(\"Payload vs. Orbit Type\", fontsize=25)\n",
            "plt.show()\n",
        ],
    ),
    47: (  # helper: extract years (make sure it also builds a usable Year column)
        "Extract_year",
        [
            "# A function to Extract years from the date\n",
            "year = []\n",
            "def Extract_year(date):\n",
            "    for i in df[\"Date\"]:\n",
            "        year.append(i.split(\"-\")[0])\n",
            "    return year\n",
            "\n",
            "Extract_year(df[\"Date\"])\n",
            "df[\"Year\"] = year\n",
            "df[[\"Date\", \"Year\"]].head()\n",
        ],
    ),
    48: (  # TASK 6: yearly average success rate line chart
        "x axis to be the extracted year",
        [
            "# Plot a line chart with x axis to be the extracted year and y axis to be the success rate\n",
            "yearly_success = df.groupby(\"Year\")[\"Class\"].mean().reset_index()\n",
            "plt.figure(figsize=(10, 6))\n",
            "sns.lineplot(data=yearly_success, x=\"Year\", y=\"Class\", marker=\"o\", linewidth=3)\n",
            "plt.xlabel(\"Year\", fontsize=15)\n",
            "plt.ylabel(\"Average Success Rate\", fontsize=15)\n",
            "plt.title(\"Launch Success Yearly Trend\", fontsize=20)\n",
            "plt.ylim(0, 1.05)\n",
            "plt.grid(True, alpha=0.3)\n",
            "plt.tight_layout()\n",
            "plt.show()\n",
        ],
    ),
    55: (  # TASK 7: dummy variables
        "get_dummies() function on the categorical columns",
        [
            "# HINT: Use get_dummies() function on the categorical columns\n",
            "features_one_hot = pd.get_dummies(features, columns=[\"Orbit\", \"LaunchSite\", \"LandingPad\", \"Serial\"])\n",
            "features_one_hot.head()\n",
        ],
    ),
    58: (  # TASK 8: cast to float64
        "astype function",
        [
            "# HINT: use astype function\n",
            "features_one_hot = features_one_hot.astype(\"float64\")\n",
            "features_one_hot.dtypes.value_counts()\n",
        ],
    ),
}


def main():
    with open(NB, encoding="utf-8") as f:
        nb = json.load(f)

    for idx, (marker, lines) in SOLUTIONS.items():
        cell = nb["cells"][idx]
        src = "".join(cell["source"])
        if cell["cell_type"] != "code":
            raise SystemExit(f"cell {idx} is not code ({cell['cell_type']})")
        if marker not in src:
            raise SystemExit(f"marker {marker!r} not found in cell {idx}: {src[:120]!r}")
        cell["source"] = lines
        cell["execution_count"] = None
        cell["outputs"] = []
        print(f"filled cell {idx}: {lines[0].strip()[:70]}")

    # Make the CSV export an actual code cell (it is markdown-only in the template)
    export_marker = "features_one_hot.to_csv('dataset_part_3.csv', index=False)"
    for i, cell in enumerate(nb["cells"]):
        if cell["cell_type"] == "markdown" and export_marker in "".join(cell["source"]):
            new_cell = {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Export the one-hot encoded features for the next lab\n",
                    "features_one_hot.to_csv('dataset_part_3.csv', index=False)\n",
                    "print('dataset_part_3.csv saved:', features_one_hot.shape)\n",
                ],
            }
            nb["cells"].insert(i + 1, new_cell)
            print(f"inserted export code cell after markdown cell {i}")
            break
    else:
        raise SystemExit("export markdown cell not found")

    with open(NB, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("notebook updated")


if __name__ == "__main__":
    main()
