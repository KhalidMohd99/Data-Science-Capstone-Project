# -*- coding: utf-8 -*-
"""Compute every technical number quoted in the presentation deck (from the real data)."""
import io
import sys

import pandas as pd

OUT = r"C:\Users\khali\Downloads\Claud_IBM-capstone-story\deck_numbers.txt"
f = open(OUT, "w", encoding="utf-8")


def p(*a):
    print(*a, file=f)


ROOT = r"C:\Users\khali\Downloads\Claud_IBM-capstone-story"
df = pd.read_csv(ROOT + r"\dataset_part_2.csv")
geo = pd.read_csv(ROOT + r"\spacex_launch_geo.csv")

p("=== DATASET ===")
p("rows:", len(df), "cols:", list(df.columns))
p("date range:", df["Date"].min(), "->", df["Date"].max())
p("overall success rate:", round(df["Class"].mean(), 4), "| successes:", int(df["Class"].sum()))

p("\n=== LAUNCH SITE ===")
g = df.groupby("LaunchSite")["Class"].agg(["count", "sum", "mean"]).sort_values("mean", ascending=False)
p(g.round(4).to_string())

p("\n=== ORBIT ===")
o = df.groupby("Orbit")["Class"].agg(["count", "sum", "mean"]).sort_values("mean", ascending=False)
p(o.round(4).to_string())

p("\n=== PAYLOAD MASS ===")
p("min/mean/max:", round(df["PayloadMass"].min(), 1), round(df["PayloadMass"].mean(), 1), round(df["PayloadMass"].max(), 1))
bins = [0, 2000, 4000, 6000, 8000, 10000, 12000, 20000]
lab = ["0-2t", "2-4t", "4-6t", "6-8t", "8-10t", "10-12t", "12t+"]
df["band"] = pd.cut(df["PayloadMass"], bins=bins, labels=lab)
pb = df.groupby("band", observed=True)["Class"].agg(["count", "sum", "mean"])
p(pb.round(4).to_string())

p("\n=== YEARLY ===")
df["Year"] = df["Date"].str.slice(0, 4)
y = df.groupby("Year")["Class"].agg(["count", "sum", "mean"])
p(y.round(4).to_string())

p("\n=== BOOSTER VERSION (top) ===")
bv = df.groupby("BoosterVersion")["Class"].agg(["count", "sum", "mean"]).sort_values("count", ascending=False)
p(bv.round(4).to_string())

p("\n=== FLIGHT NUMBER ===")
p("min/max:", df["FlightNumber"].min(), df["FlightNumber"].max())

p("\n=== GEO FILE ===")
p("rows:", len(geo), "cols:", list(geo.columns))
p(geo.groupby("Launch Site")[["Lat", "Long"]].first().to_string())
p("class counts:", geo["class"].value_counts().to_dict())

p("\n=== HIGHEST PAYLOAD RECORDS ===")
p(df.nlargest(5, "PayloadMass")[["FlightNumber", "Date", "BoosterVersion", "PayloadMass", "Orbit", "LaunchSite", "Class"]].to_string(index=False))

p("\n=== PAYLOAD 4000-6000 SUCCESS (drone ship context) ===")
sub = df[(df.PayloadMass > 4000) & (df.PayloadMass < 6000)]
p("count:", len(sub), "success rate:", round(sub["Class"].mean(), 4))

p("\n=== NAN CHECK ===")
p(df.isna().sum().to_dict())
f.close()
print("written deck_numbers.txt")
