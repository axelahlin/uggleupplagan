import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import get_coords as gs
import wikidata_query
import json

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import time
# dummy list of places, connect to annotator later
FILENAME_IN = "annotated.json"
FILENAME_OUT_CSV = "coords.csv"
FILENAME_OUT_JSON = "purged.json"


def get_and_save_coords():

    fails = 0

    with open(FILENAME_OUT_CSV, 'w') as o:

        with open(FILENAME_OUT_JSON, 'w') as jo:

            with open(FILENAME_IN, encoding='utf-8') as i:
                js = json.load(i)
                o.write("lons,lats,texts")
                for j in js:
                    if j['is_loc'] and j['qid']:

                        # for qid in j['qid']:
                        #     coordinates = gs.get_coords(qid)
                        #     if coordinates:
                        #         o.write(str(coordinates[0]) +
                        #                 "," + str(coordinates[1]) + '\n')
                        #         continue

                        coordinates = gs.get_coords(j['qid'])
                        text = j['text']
                        if coordinates:

                            o.write(str(coordinates[0]) +
                                    "," + str(coordinates[1]) + "," + text + '\n')
                        else:
                            # SETS THE IS_LOC TO FALSE TO PURGE ALL ENTRIES WITHOUT COORDINATES.
                            j['is_loc'] = False
                            j['qid'] = None
                            fails += 1

                        time.sleep(0.1)

                json.dump(js, jo, ensure_ascii=False)

    print(f"{fails=}")


def twod_map_coords(filename=FILENAME_OUT_CSV):

    df = pd.read_csv(filename)
    # if you are passing just one lat and lon, put it within "[]"
    # editing the marker
    fig = px.scatter_geo(df, lat="lats", lon="lons", projection="natural earth", opacity=0.3
                         )
    fig.show()
    fig.write_html("2d_plot.html")
    fig.show()


def threed_map_coords(filename=FILENAME_OUT_CSV):

    lons, lats = [], []

    with open(filename) as f:
        for line in f.readlines():
            lon, lat = line.split(',')

            # print(lon, lat)
            lons.append(float(lon))
            lats.append(float(lat))

    print(f"Successful coords: {len(lons)}")

    # if you are passing just one lat and lon, put it within "[]"
    # editing the marker
    fig = go.Figure(go.Scattergeo(lat=lats, lon=lons))
    # this projection_type = 'orthographic is the projection which return 3d globe map'
    fig.update_traces(marker={"opacity": 0.4, 'size': 5, "color": "blue"})
    # layout, exporting html and showing the plot
    fig.update_geos(projection_type="orthographic")
    fig.update_layout(width=800, height=800, margin={
                      "r": 0, "t": 0, "l": 0, "b": 0})
    fig.write_html("3d_plot.html")
    fig.show()


if __name__ == "__main__":
    # get_and_save_coords()
    twod_map_coords()
    # threed_map_coords()
