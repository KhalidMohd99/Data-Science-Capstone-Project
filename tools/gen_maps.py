# -*- coding: utf-8 -*-
"""Generate the three standalone Folium maps required by the presentation:
  assets/maps/map_1_all_launch_sites.html    -> all launch sites (slide 35)
  assets/maps/map_2_launch_outcomes.html     -> color-labelled outcomes in a cluster (slide 36)
  assets/maps/map_3_site_proximity.html      -> selected site + coastline/city/highway distances (slide 37)
Logic mirrors launch_site_location.ipynb.
"""
import io
import math
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import folium
import pandas as pd
from folium.features import DivIcon
from folium.plugins import MarkerCluster

ROOT = r"C:\Users\khali\Downloads\Claud_IBM-capstone-story"
OUT = os.path.join(ROOT, "assets", "maps")
os.makedirs(OUT, exist_ok=True)

df = pd.read_csv(os.path.join(ROOT, "spacex_launch_geo.csv"))
df = df[["Launch Site", "Lat", "Long", "class"]]
sites = df.groupby("Launch Site", as_index=False).first()[["Launch Site", "Lat", "Long"]]


def distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# ---------------------------------------------------------- map 1: all sites
site_map = folium.Map(location=[29.559684888503615, -95.0830971930759], zoom_start=4)
folium.Marker(
    [29.559684888503615, -95.0830971930759],
    popup="NASA Johnson Space Center",
    icon=DivIcon(icon_size=(140, 18), icon_anchor=(70, 9),
                 html='<div style="font-size:12px;color:#d35400;"><b>NASA JSC</b></div>'),
).add_to(site_map)

for _, r in sites.iterrows():
    coord = [r["Lat"], r["Long"]]
    folium.Circle(coord, radius=1000, color="#000000", fill=True,
                  popup=r["Launch Site"]).add_to(site_map)
    folium.map.Marker(
        coord,
        icon=DivIcon(icon_size=(120, 18), icon_anchor=(60, 9),
                     html=f'<div style="font-size:12px;color:#d35400;"><b>{r["Launch Site"]}</b></div>'),
    ).add_to(site_map)

p1 = os.path.join(OUT, "map_1_all_launch_sites.html")
site_map.save(p1)
print("saved", p1)

# -------------------------------------------------------- map 2: outcomes
df["marker_color"] = df["class"].apply(lambda x: "green" if x == 1 else "red")
out_map = folium.Map(location=[28.5, -80.6], zoom_start=6)
cluster = MarkerCluster(name="Launch outcomes").add_to(out_map)
for _, r in df.iterrows():
    folium.Marker(
        [r["Lat"], r["Long"]],
        popup=f'{r["Launch Site"]} - {"Success" if r["class"] == 1 else "Failure"}',
        icon=folium.Icon(color="white", icon_color=r["marker_color"],
                         icon="rocket", prefix="fa"),
    ).add_to(cluster)
for _, r in sites.iterrows():
    folium.map.Marker(
        [r["Lat"], r["Long"]],
        icon=DivIcon(icon_size=(120, 18), icon_anchor=(60, -10),
                     html=f'<div style="font-size:12px;color:#0043ce;"><b>{r["Launch Site"]}</b></div>'),
    ).add_to(out_map)
folium.LayerControl().add_to(out_map)

p2 = os.path.join(OUT, "map_2_launch_outcomes.html")
out_map.save(p2)
print("saved", p2)

# --------------------------------------------- map 3: proximity of one site
# selected site: CCAFS LC-40 (first row of launch_sites_df in the notebook)
lat0 = float(sites.loc[0, "Lat"])
lon0 = float(sites.loc[0, "Long"])
proximities = [
    ("Closest coastline", 28.56367, -80.57163, "#171717"),
    ("Closest city (Port Canaveral)", 28.4119, -80.6185, "#0f62fe"),
    ("Closest highway (I-95)", 28.572, -80.780, "#8a3ffc"),
]

prox_map = folium.Map(location=[lat0, lon0], zoom_start=10)
folium.Circle([lat0, lon0], radius=1000, color="#000000", fill=True,
              popup=sites.loc[0, "Launch Site"]).add_to(prox_map)
folium.map.Marker(
    [lat0, lon0],
    icon=DivIcon(icon_size=(130, 18), icon_anchor=(65, 9),
                 html=f'<div style="font-size:12px;color:#d35400;"><b>{sites.loc[0, "Launch Site"]}</b></div>'),
).add_to(prox_map)

for label, plat, plon, color in proximities:
    d = distance(lat0, lon0, plat, plon)
    folium.Marker(
        [plat, plon],
        icon=DivIcon(icon_size=(190, 20), icon_anchor=(-10, 10),
                     html=f'<div style="font-size:12px;color:{color};">'
                          f'<b>{label}: {d:.2f} KM</b></div>'),
    ).add_to(prox_map)
    folium.PolyLine(locations=[[lat0, lon0], [plat, plon]],
                    weight=2, color=color, dash_array="6").add_to(prox_map)
    print(f"  {label}: {d:.2f} KM")

p3 = os.path.join(OUT, "map_3_site_proximity.html")
prox_map.save(p3)
print("saved", p3)
print("done")
