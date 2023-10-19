import matplotlib.pyplot as plt
# from mpl_toolkits.basemap import Basemap
#import scripts.coordinates_retreival as gs
import json
import time
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd



def twod_map_coords(config):
    data = config["visualization"]["data_file"]
    output_image = config["visualization"]["output_image"]


    data = pd.read_json(data)
    fig = px.scatter_geo(data, lat="longitude", 
                         lon="latitude", 
                         hover_name='qid',
                         hover_data='text',
                         projection="natural earth", opacity=0.3
                         )
    # fig.to_image(output_image)
    
    fig.write_html("2d_plot.html")
    fig.show()



def threed_map_coords(config):
    FILENAME_OUT_CSV = config["coords_fetch"]["output_csv_file"]

    lons, lats = [], []

    with open(FILENAME_OUT_CSV) as f:
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


