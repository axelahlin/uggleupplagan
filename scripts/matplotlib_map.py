import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import get_coords as gs
import wikidata_query
import json

# dummy list of places, connect to annotator later
FILENAME_IN = "json_dump.json"
FILENAME_OUT = "coords.csv"


def get_and_save_coords():

    with open(FILENAME_OUT, 'w') as o:
        with open(FILENAME_IN, encoding='utf-8') as i:
            js = json.load(i)

            for j in js[:500]:
                if j['qid']:
                    coordinates = gs.get_coords(j['qid'])
                    if coordinates:
                        o.write(str(coordinates[0]) +
                                "," + str(coordinates[1]) + '\n')


def map_coords(filename=FILENAME_OUT):

    lons, lats = [], []

    with open(filename) as f:
        for line in f.readlines():
            lon, lat = line.split(',')

            lat = lat[:-1]
            lons.append(float(lon))
            lats.append(float(lat))

    print(f"Successful coords: {len(lons)}")

    map = Basemap()
    map.drawcoastlines(linewidth=0.5)
    map.drawcountries(linewidth=0.5)
    map.fillcontinents(color='lightgray', lake_color='white')
    x, y = map(lons, lats)
    map.plot(x, y, 'bo', markersize=6)
    plt.show()


if __name__ == "__main__":
    get_and_save_coords()
    map_coords()
