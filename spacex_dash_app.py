# -*- coding: utf-8 -*-
"""SpaceX Falcon 9 Launch Records Dashboard - Plotly Dash lab.

Run:  python spacex_dash_app.py   then open http://localhost:8050

Dashboard components
  1. Pie chart  - total successful launches for ALL launch sites
  2. Pie chart  - success vs failure for the selected site (default: best success ratio)
  3. Scatter    - Payload (kg) vs Launch Outcome with a Range Slider filter
"""
import os

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# ------------------------------------------------------------------ data
CSV = "dataset_part_2.csv"
S3 = ("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
      "IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv")

df = pd.read_csv(CSV) if os.path.exists(CSV) else pd.read_csv(S3)
df = df.dropna(subset=["PayloadMass"])

# ------------------------------------------------------------------ stats
site_stats = (
    df.groupby("LaunchSite")["Class"]
    .agg(["count", "sum", "mean"])
    .rename(columns={"count": "launches", "sum": "successes", "mean": "success_ratio"})
    .sort_values("success_ratio", ascending=False)
)
best_site = site_stats.index[0]

slider_min = int(df["PayloadMass"].min() // 1000 * 1000)
slider_max = int(-(-df["PayloadMass"].max() // 1000) * 1000)
marks = {v: str(v) for v in range(slider_min, slider_max + 1, 2500)}

# Initial state of the widgets.  It can be overridden with environment variables,
# which is handy for automated screenshots:
#   DASH_INITIAL_SITE="KSC LC 39A" DASH_INITIAL_MIN=0 DASH_INITIAL_MAX=6000 DASH_PORT=8061
INITIAL_SITE = os.environ.get("DASH_INITIAL_SITE", "ALL")
INITIAL_MIN = int(os.environ.get("DASH_INITIAL_MIN", slider_min))
INITIAL_MAX = int(os.environ.get("DASH_INITIAL_MAX", slider_max))

# ------------------------------------------------------------------ app
app = Dash(__name__)

app.layout = html.Div(
    style={"fontFamily": "Segoe UI, Arial, sans-serif", "maxWidth": "1100px",
           "margin": "0 auto", "padding": "18px"},
    children=[
        html.H1("SpaceX Falcon 9 Launch Records Dashboard",
                style={"color": "#0f62fe", "textAlign": "center"}),
        html.P("Interactive analytics of Falcon 9 launches, landing outcomes and "
               "payload mass - data source: dataset_part_2.csv (90 launches).",
               style={"textAlign": "center", "color": "#525252"}),

        html.H3("1. Select a Launch Site"),
        dcc.Dropdown(
            id="site-dropdown",
            options=[{"label": "All Sites", "value": "ALL"}] +
                    [{"label": s, "value": s} for s in sorted(df["LaunchSite"].unique())],
            value=INITIAL_SITE,
            placeholder="Select a Launch Site here",
            style={"width": "60%"},
        ),
        html.Div(id="site-info", style={"marginTop": "8px", "fontWeight": "600"}),

        html.H3("2. Launch Success Distribution"),
        dcc.Graph(id="success-pie"),

        html.H3("3. Payload (kg) vs Launch Outcome"),
        dcc.Graph(id="payload-scatter"),
        dcc.RangeSlider(
            id="payload-slider",
            min=slider_min,
            max=slider_max,
            step=100,
            marks=marks,
            value=[INITIAL_MIN, INITIAL_MAX],
        ),
        html.Div(id="payload-info", style={"marginTop": "6px", "color": "#525252"}),
    ],
)


@app.callback(
    Output("success-pie", "figure"),
    Output("site-info", "children"),
    Input("site-dropdown", "value"),
)
def update_pie(selected_site):
    if selected_site == "ALL":
        success = (
            df[df["Class"] == 1]
            .groupby("LaunchSite")
            .size()
            .reset_index(name="Successful Launches")
            .sort_values("Successful Launches", ascending=False)
        )
        fig = px.pie(
            success,
            names="LaunchSite",
            values="Successful Launches",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Safe,
            title="Total Successful Launches per Launch Site",
        )
        info = (f"Highest success ratio: {best_site} "
                f"({site_stats.loc[best_site, 'success_ratio']:.0%})")
        return fig, info

    sub = df[df["LaunchSite"] == selected_site]
    counts = sub["Class"].value_counts().rename({1: "Success", 0: "Failure"})
    fig = px.pie(
        names=counts.index,
        values=counts.values,
        hole=0.4,
        color={"Success": "#24a148", "Failure": "#da1e28"},
        title=f"Launch outcomes at {selected_site}",
    )
    ratio = sub["Class"].mean()
    info = (f"{selected_site}: {len(sub)} launches, success ratio {ratio:.0%}"
            f" (best site: {best_site})")
    return fig, info


@app.callback(
    Output("payload-scatter", "figure"),
    Output("payload-info", "children"),
    Input("payload-slider", "value"),
    Input("site-dropdown", "value"),
)
def update_scatter(payload_range, selected_site):
    low, high = payload_range
    mask = (df["PayloadMass"] >= low) & (df["PayloadMass"] <= high)
    if selected_site != "ALL":
        mask &= df["LaunchSite"] == selected_site
    sub = df[mask]
    fig = px.scatter(
        sub,
        x="PayloadMass",
        y="Class",
        color=sub["Class"].map({1: "Success", 0: "Failure"}),
        color_discrete_map={"Success": "#24a148", "Failure": "#da1e28"},
        hover_data=["FlightNumber", "LaunchSite", "Orbit", "BoosterVersion"],
        labels={"PayloadMass": "Payload Mass (kg)", "Class": "Launch Outcome"},
        title="Payload vs Launch Outcome",
    )
    fig.update_yaxes(dtick=1, tickvals=[0, 1], ticktext=["Failure", "Success"])
    fig.update_layout(height=430, legend_title_text="")
    info = (f"Showing {len(sub)} of {len(df)} launches with payload in "
            f"[{low:,}, {high:,}] kg")
    return fig, info


if __name__ == "__main__":
    app.run(debug=False, port=int(os.environ.get("DASH_PORT", 8050)))
