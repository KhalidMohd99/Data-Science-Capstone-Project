# -*- coding: utf-8 -*-
"""Fix the three incomplete/broken notebooks so they execute cleanly top-to-bottom.

1) jupyter-labs-eda-dataviz-v2.ipynb : pip cell -> %pip (local kernel)
2) 02-jupyter-labs-webscraping.ipynb : real column extraction, single parse loop,
                                       df cleanup + CSV export cell
3) launch_site_location.ipynb        : remove JupyterLite-only code (piplite/js fetch),
                                       define nasa_coordinate before use, complete the
                                       MarkerCluster TODO, fix ellipsis error cell,
                                       complete the PolyLine cell
"""
import json
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = r"C:\Users\khali\Downloads\Claud_IBM-capstone-story"


def load(name):
    with open(f"{ROOT}\\{name}", encoding="utf-8") as f:
        return json.load(f)


def save(name, nb):
    with open(f"{ROOT}\\{name}", "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
        f.write("\n")


def src(cell):
    return "".join(cell["source"])


def set_src(cell, text):
    lines = text.splitlines(keepends=True)
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    cell["source"] = lines
    if cell["cell_type"] == "code":
        cell["execution_count"] = None
        cell["outputs"] = []


def check(cell, marker, name):
    if marker not in src(cell):
        raise SystemExit(f"[{name}] marker {marker!r} not found: {src(cell)[:120]!r}")


# ---------------------------------------------------------------- 1) DATAVIZ
name = "jupyter-labs-eda-dataviz-v2.ipynb"
nb = load(name)
if "!pip install pandas" in src(nb["cells"][13]):
    check(nb["cells"][13], "!pip install pandas", name)
    set_src(nb["cells"][13], "# Install the required libraries (already available in the local environment)\n"
                            "%pip install -q pandas numpy seaborn matplotlib")
    save(name, nb)
    print(f"[{name}] pip cell fixed")
else:
    print(f"[{name}] already fixed")

# ------------------------------------------------------------ 2) WEB SCRAPING
name = "02-jupyter-labs-webscraping.ipynb"
nb = load(name)

if "!pip3 install beautifulsoup4" in src(nb["cells"][14]):
    set_src(nb["cells"][14], "# Install the required libraries (already available in the local environment)\n"
                             "%pip install -q beautifulsoup4 requests")
else:
    print(f"[{name}] pip cell already fixed")

# TASK 2: real header extraction instead of a pasted list literal
check(nb["cells"][37], "column_names = []", name)
set_src(nb["cells"][37], """# Apply find_all() function with `th` element on first_launch_table
# Iterate each th element and apply the provided extract_column_from_header() to get a column name
# Append the Non-empty column name (`if name is not None and len(name) > 0`) into a list called column_names

column_names = []

for th in first_launch_table.find_all('th'):
    name = extract_column_from_header(th)
    if name is not None and len(name) > 0:
        column_names.append(name)
""")

# Cell 42: keep ONLY the initialisation (the parsing loop lives in cell 46;
# running both would duplicate every launch record)
check(nb["cells"][42], "launch_dict = dict.fromkeys(column_names)", name)
set_src(nb["cells"][42], """# Initialize dictionary
launch_dict = dict.fromkeys(column_names)

# Header keys that are parsed later into separate 'Date' / 'Time' / 'Version Booster'
# columns must start as empty lists, not None
launch_dict = {key: (value if value is not None else []) for key, value in launch_dict.items()}

# Initialize lists
launch_dict['Flight No.'] = []
launch_dict['Launch site'] = []
launch_dict['Payload'] = []
launch_dict['Payload mass'] = []
launch_dict['Orbit'] = []
launch_dict['Customer'] = []
launch_dict['Launch outcome'] = []
launch_dict['Version Booster'] = []
launch_dict['Booster landing'] = []
launch_dict['Date'] = []
launch_dict['Time'] = []

extracted_row = 0
""")

# Cell 48: build the dataframe, drop never-filled header columns, show a preview
check(nb["cells"][48], "pd.DataFrame", name)
set_src(nb["cells"][48], """df = pd.DataFrame({key: pd.Series(value) for key, value in launch_dict.items()})

# Drop header-only keys that were never filled during parsing
# (e.g. 'Date and time ( )' and 'Version, Booster' are handled by 'Date'/'Time'/'Version Booster')
df = df.dropna(axis=1, how='all')

print('Scraped records:', df.shape[0])
df.head()
""")

# Turn the markdown-only export instruction into a real code cell
export_md = "<code>df.to_csv('spacex_web_scraped.csv', index=False)</code>"
already_has_export = any(
    c["cell_type"] == "code" and "spacex_web_scraped.csv" in src(c)
    for c in nb["cells"]
)
if already_has_export:
    print(f"[{name}] export code cell already present")
for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] == "markdown" and export_md in src(cell) and not already_has_export:
        nb["cells"].insert(i + 1, {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Export the scraped records for the next lab\n",
                "df.to_csv('spacex_web_scraped.csv', index=False)\n",
                "print('spacex_web_scraped.csv saved:', df.shape)\n",
            ],
        })
        print(f"[{name}] export code cell inserted after cell {i}")
        break
else:
    if not already_has_export:
        raise SystemExit(f"[{name}] export markdown cell not found")

save(name, nb)
print(f"[{name}] fixed")

# ----------------------------------------------------------------- 3) FOLIUM
name = "launch_site_location.ipynb"
nb = load(name)

# JupyterLite-only installation cell
check(nb["cells"][5], "import piplite", name)
set_src(nb["cells"][5], "# Local environment note: folium and pandas are already installed here.\n"
                        "# (In JupyterLite this cell ran: import piplite; await piplite.install(['folium', 'pandas']))")

# site_map is created before nasa_coordinate existed -> define it there
check(nb["cells"][10], "site_map = folium.Map(location=nasa_coordinate, zoom_start=5)", name)
set_src(nb["cells"][10], """## Task 1: Mark all launch sites on a map

# Start location is NASA Johnson Space Center
nasa_coordinate = [29.559684888503615, -95.0830971930759]
site_map = folium.Map(location=nasa_coordinate, zoom_start=5)
""")

# JupyterLite-only data loading
check(nb["cells"][13], "from js import fetch", name)
set_src(nb["cells"][13], """# Download and read the `spacex_launch_geo.csv`
URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv'
spacex_df = pd.read_csv(URL)
""")

# tidy the "closest coastline" cell (was bare `Lat: 28.56367` annotations)
check(nb["cells"][55], "closet coastline", name)
set_src(nb["cells"][55], """# Find the coordinates of the closest coastline point (read with MousePosition on the map)
# e.g.: Lat 28.56367, Lon -80.57163
coastline_lat = 28.56367
coastline_lon = -80.57163
""")

# Cell 40: attach the cluster only; the per-row markers are added in cell 42 (its TODO)
check(nb["cells"][40], "marker_cluster = MarkerCluster()", name)
set_src(nb["cells"][40], """# Apply a function to check the value of `class` column
# If class=1, marker_color value will be green
# If class=0, marker_color value will be red
spacex_df['marker_color'] = spacex_df['class'].apply(lambda x: 'green' if x == 1 else 'red')

# Create a MarkerCluster object and add it to the map
marker_cluster = MarkerCluster()
site_map.add_child(marker_cluster)

spacex_df[['Launch Site', 'class', 'marker_color']].head()
""")

# Cell 42 TODO: actually create one Marker per launch record
check(nb["cells"][42], "TODO: Create and add a Marker cluster", name)
set_src(nb["cells"][42], """# Add marker_cluster to current site_map
site_map.add_child(marker_cluster)

# for each row in spacex_df data frame
# create a Marker object with its coordinate
# and customize the Marker's icon property to indicate if this launch was successed or failed,
# e.g., icon=folium.Icon(color='white', icon_color=row['marker_color']
for index, record in spacex_df.iterrows():

    # Get the launch coordinates
    coordinate = [record['Lat'], record['Long']]

    # Create a marker coloured by the launch outcome
    marker = folium.Marker(
        coordinate,
        icon=folium.Icon(
            color='white',
            icon_color=record['marker_color'],
            icon='rocket',
            prefix='fa'
        )
    )

    # Add the marker to the cluster
    marker_cluster.add_child(marker)

site_map
""")

# Cell 58: `lines` was never created here -> create the PolyLine in this cell
check(nb["cells"][58], "site_map.add_child(lines)", name)
set_src(nb["cells"][58], """# Create a `folium.PolyLine` object using the coastline coordinates and launch site coordinate
coordinates = [
    [launch_site_lat, launch_site_lon],
    [coastline_lat, coastline_lon]
]

lines = folium.PolyLine(
    locations=coordinates,
    weight=1
)

site_map.add_child(lines)

site_map
""")

# Cell 69: draw the line to the closest highway (I-95) instead of repeating the coastline line
check(nb["cells"][69], "folium.PolyLine", name)
set_src(nb["cells"][69], """# Coordinates for the line to the closest highway (I-95 near Port St. John, read with MousePosition)
highway_lat = 28.572
highway_lon = -80.780

highway_distance = calculate_distance(launch_site_lat, launch_site_lon, highway_lat, highway_lon)

# Create the line
lines = folium.PolyLine(
    locations=[
        [launch_site_lat, launch_site_lon],
        [highway_lat, highway_lon]
    ],
    weight=1,
    color='blue'
)

# Add the line
site_map.add_child(lines)

print("Distance to highway I-95:", round(highway_distance, 2), "KM")
site_map
""")

# Cell 70: `point_lat = ...` raised TypeError -> use the closest city (Port Canaveral)
check(nb["cells"][70], "point_lat = ...", name)
set_src(nb["cells"][70], """# 1. Coordinates of the closest city read with MousePosition (Port Canaveral, FL)
point_lat = 28.4119
point_lon = -80.6185

# 2. Calculate distance
distance = calculate_distance(
    launch_site_lat,
    launch_site_lon,
    point_lat,
    point_lon
)

# 3. Create a marker
distance_marker = folium.Marker(
    [point_lat, point_lon],
    icon=DivIcon(
        icon_size=(20, 20),
        icon_anchor=(0, 0),
        html='<div style="font-size: 12; color:#d35400;">'
             '<b>%s</b></div>' %
             "{:10.2f} KM".format(distance)
    )
)

# 4. Add marker
site_map.add_child(distance_marker)

# 5. Draw connecting line
lines = folium.PolyLine(
    locations=[
        [launch_site_lat, launch_site_lon],
        [point_lat, point_lon]
    ],
    weight=1
)

site_map.add_child(lines)

print("Distance to Port Canaveral:", round(distance, 2), "KM")
site_map
""")

save(name, nb)
print(f"[{name}] fixed")
print("ALL FIXES APPLIED")
