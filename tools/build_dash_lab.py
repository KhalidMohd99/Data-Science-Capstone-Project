# -*- coding: utf-8 -*-
"""Create the missing Plotly Dash dashboard lab:
- spacex_dash_app.py            : runnable Dash server (used for screenshots)
- 06-plotly-dash-dashboard.ipynb : the lab notebook (charts inline + app definition, no blocking server)
"""
import io
import json
import os
import sys
import uuid

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = r"C:\Users\khali\Downloads\Claud_IBM-capstone-story"

# --------------------------------------------------------------- app script
APP = '''# -*- coding: utf-8 -*-
"""SpaceX Falcon 9 Launch Records Dashboard - Plotly Dash lab.

Run:  python spacex_dash_app.py   then open http://localhost:8050

Dashboard components
  1. Pie chart  - total successful launches for ALL launch sites
  2. Pie chart  - success vs failure for the selected site (default: best success ratio)
  3. Scatter    - Payload (kg) vs Launch Outcome with a Range Slider filter
"""
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# ------------------------------------------------------------- data
CSV = "dataset_part_2.csv"
S3 = ("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
      "IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv")
df = pd.read_csv(CSV) if os_path_exists(CSV) else pd.read_csv(S3)

def os_path_exists(p):
    import os
    return os.path.exists(p)


df = df.dropna(subset=["PayloadMass"])

# ------------------------------------------------------------- stats
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

# ------------------------------------------------------------- app
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

        # -------- selector
        html.H3("1. Select a Launch Site"),
        dcc.Dropdown(
            id="site-dropdown",
            options=[{"label": "All Sites", "value": "ALL"}] +
                    [{"label": s, "value": s} for s in sorted(df["LaunchSite"].unique())],
            value="ALL",
            placeholder="Select a Launch Site here",
            style={"width": "60%"},
        ),
        html.Div(id="site-info", style={"marginTop": "8px", "fontWeight": "600"}),

        # -------- graph 1 & 2: pie charts
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
            value=[slider_min, slider_max],
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
        # total successful launches for every site
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
        info = f"Highest success ratio: {best_site} ({site_stats.loc[best_site, 'success_ratio']:.0%})"
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
    info = f"Showing {len(sub)} of {len(df)} launches with payload in [{low:,}, {high:,}] kg"
    return fig, info


if __name__ == "__main__":
    app.run(debug=False, port=8050)
'''

# the draft above references os_path_exists before definition - rewrite cleanly
APP = '''# -*- coding: utf-8 -*-
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
            value="ALL",
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
            value=[slider_min, slider_max],
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
    app.run(debug=False, port=8050)
'''

with open(os.path.join(ROOT, "spacex_dash_app.py"), "w", encoding="utf-8") as f:
    f.write(APP)
print("wrote spacex_dash_app.py")

# --------------------------------------------------------------- notebook
def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text, "id": uuid.uuid4().hex[:8]}


def code(text):
    return {"cell_type": "code", "execution_count": None, "outputs": [],
            "metadata": {}, "source": text, "id": uuid.uuid4().hex[:8]}


cells = [
    md("""# **SpaceX Falcon 9 First Stage Landing Prediction**
## Hands-on Lab: Build a Dashboard with Plotly Dash

**Estimated time needed: 45 minutes**

In this lab you will build an interactive dashboard with Plotly Dash that lets the user
explore the SpaceX launch records:

1. a pie chart with the **total successful launches for all launch sites**
2. a pie chart for **a selected launch site** (default: the site with the highest success ratio)
3. a **Payload vs Launch Outcome** scatter plot filtered with a Range Slider
"""),
    code("""%pip install -q pandas plotly dash"""),
    code("""import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

print('libraries loaded')"""),
    md("""### Load the SpaceX launch records (`dataset_part_2.csv`, 90 launches)"""),
    code("""CSV = 'dataset_part_2.csv'
S3 = ('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/'
      'IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv')

import os
df = pd.read_csv(CSV) if os.path.exists(CSV) else pd.read_csv(S3)
df = df.dropna(subset=['PayloadMass'])
df[['FlightNumber', 'LaunchSite', 'PayloadMass', 'Orbit', 'Class']].head()"""),
    md("""### TASK 1: Success counts per launch site (all sites)

The pie chart below shows how many **successful** launches each site achieved. It is the
default view of the dashboard and answers *which sites carry the most successful missions*.
"""),
    code("""success = (df[df['Class'] == 1]
           .groupby('LaunchSite').size()
           .reset_index(name='Successful Launches')
           .sort_values('Successful Launches', ascending=False))

fig1 = px.pie(success, names='LaunchSite', values='Successful Launches',
              hole=0.4, color_discrete_sequence=px.colors.qualitative.Safe,
              title='Total Successful Launches per Launch Site')
fig1.show()"""),
    md("""### TASK 2: Success ratio of each launch site

Which site is the most reliable? The dashboard shows this site by default when the user
picks it in the dropdown.
"""),
    code("""site_stats = (df.groupby('LaunchSite')['Class']
              .agg(['count', 'sum', 'mean'])
              .rename(columns={'count': 'launches', 'sum': 'successes',
                               'mean': 'success_ratio'})
              .sort_values('success_ratio', ascending=False))
best_site = site_stats.index[0]
print(site_stats)
print('Best site:', best_site)"""),
    code("""def site_pie(site):
    sub = df[df['LaunchSite'] == site]
    counts = sub['Class'].value_counts().rename({1: 'Success', 0: 'Failure'})
    return px.pie(names=counts.index, values=counts.values, hole=0.4,
                  color={'Success': '#24a148', 'Failure': '#da1e28'},
                  title=f'Launch outcomes at {site}')

site_pie(best_site).show()"""),
    md("""### TASK 3: Payload vs Launch Outcome with a Range Slider

The scatter plot lets the user restrict the analysis to a payload range
(e.g. *which payload band has the highest success rate?*).
"""),
    code("""slider_min = int(df['PayloadMass'].min() // 1000 * 1000)
slider_max = int(-(-df['PayloadMass'].max() // 1000) * 1000)
marks = {v: str(v) for v in range(slider_min, slider_max + 1, 2500)}
print('slider range:', slider_min, '-', slider_max)

fig3 = px.scatter(df, x='PayloadMass', y='Class',
                  color=df['Class'].map({1: 'Success', 0: 'Failure'}),
                  color_discrete_map={'Success': '#24a148', 'Failure': '#da1e28'},
                  hover_data=['FlightNumber', 'LaunchSite', 'Orbit', 'BoosterVersion'],
                  labels={'PayloadMass': 'Payload Mass (kg)', 'Class': 'Launch Outcome'},
                  title='Payload vs Launch Outcome')
fig3.update_yaxes(dtick=1, tickvals=[0, 1], ticktext=['Failure', 'Success'])
fig3.show()"""),
    md("""### Build the Dash application

The layout and the two callbacks below are exactly what `spacex_dash_app.py` serves on
`http://localhost:8050`. Set `RUN_SERVER = True` to launch it from here (the cell blocks
until you stop the kernel), or run `python spacex_dash_app.py` in a terminal.
"""),
    code("""app = Dash(__name__)

app.layout = html.Div(
    style={'fontFamily': 'Segoe UI, Arial, sans-serif', 'maxWidth': '1100px',
           'margin': '0 auto', 'padding': '18px'},
    children=[
        html.H1('SpaceX Falcon 9 Launch Records Dashboard',
                style={'color': '#0f62fe', 'textAlign': 'center'}),
        html.P('Interactive analytics of Falcon 9 launches, landing outcomes and '
               'payload mass - data source: dataset_part_2.csv (90 launches).',
               style={'textAlign': 'center', 'color': '#525252'}),

        html.H3('1. Select a Launch Site'),
        dcc.Dropdown(
            id='site-dropdown',
            options=[{'label': 'All Sites', 'value': 'ALL'}] +
                    [{'label': s, 'value': s} for s in sorted(df['LaunchSite'].unique())],
            value='ALL',
            placeholder='Select a Launch Site here',
            style={'width': '60%'},
        ),
        html.Div(id='site-info', style={'marginTop': '8px', 'fontWeight': '600'}),

        html.H3('2. Launch Success Distribution'),
        dcc.Graph(id='success-pie'),

        html.H3('3. Payload (kg) vs Launch Outcome'),
        dcc.Graph(id='payload-scatter'),
        dcc.RangeSlider(id='payload-slider', min=slider_min, max=slider_max,
                        step=100, marks=marks, value=[slider_min, slider_max]),
        html.Div(id='payload-info', style={'marginTop': '6px', 'color': '#525252'}),
    ],
)


@app.callback(Output('success-pie', 'figure'),
              Output('site-info', 'children'),
              Input('site-dropdown', 'value'))
def update_pie(selected_site):
    if selected_site == 'ALL':
        return fig1, (f'Highest success ratio: {best_site} '
                      f'({site_stats.loc[best_site, "success_ratio"]:.0%})')
    sub = df[df['LaunchSite'] == selected_site]
    counts = sub['Class'].value_counts().rename({1: 'Success', 0: 'Failure'})
    fig = px.pie(names=counts.index, values=counts.values, hole=0.4,
                 color={'Success': '#24a148', 'Failure': '#da1e28'},
                 title=f'Launch outcomes at {selected_site}')
    return fig, (f'{selected_site}: {len(sub)} launches, '
                 f'success ratio {sub["Class"].mean():.0%} (best site: {best_site})')


@app.callback(Output('payload-scatter', 'figure'),
              Output('payload-info', 'children'),
              Input('payload-slider', 'value'),
              Input('site-dropdown', 'value'))
def update_scatter(payload_range, selected_site):
    low, high = payload_range
    mask = (df['PayloadMass'] >= low) & (df['PayloadMass'] <= high)
    if selected_site != 'ALL':
        mask &= df['LaunchSite'] == selected_site
    sub = df[mask]
    fig = px.scatter(sub, x='PayloadMass', y='Class',
                     color=sub['Class'].map({1: 'Success', 0: 'Failure'}),
                     color_discrete_map={'Success': '#24a148', 'Failure': '#da1e28'},
                     hover_data=['FlightNumber', 'LaunchSite', 'Orbit', 'BoosterVersion'],
                     labels={'PayloadMass': 'Payload Mass (kg)', 'Class': 'Launch Outcome'},
                     title='Payload vs Launch Outcome')
    fig.update_yaxes(dtick=1, tickvals=[0, 1], ticktext=['Failure', 'Success'])
    fig.update_layout(height=430, legend_title_text='')
    return fig, (f'Showing {len(sub)} of {len(df)} launches with payload in '
                 f'[{low:,}, {high:,}] kg')


RUN_SERVER = False  # set True to launch the dashboard (blocking cell)
if RUN_SERVER:
    app.run(debug=False, port=8050)
else:
    print('Dashboard app built. Launch it with:  python spacex_dash_app.py')"""),
    md("""### Run the dashboard

```bash
python spacex_dash_app.py
```

Then open <http://localhost:8050>. The dropdown drives the pie chart and the range slider
filters the payload scatter plot.

## Authors
Capstone project - Data Science with Python
"""),
]

nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python (capstone)", "language": "python",
                       "name": "capstone"},
        "language_info": {"name": "python", "version": "3.14"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

path = os.path.join(ROOT, "06-plotly-dash-dashboard.ipynb")
with open(path, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("wrote 06-plotly-dash-dashboard.ipynb")
print("done")
