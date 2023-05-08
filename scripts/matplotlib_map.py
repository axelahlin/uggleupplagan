import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import get_coords as gs
import wikidata_query
import json

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

                for j in js:
                    if j['is_loc'] and j['qid']:

                        # for qid in j['qid']:
                        #     coordinates = gs.get_coords(qid)
                        #     if coordinates:
                        #         o.write(str(coordinates[0]) +
                        #                 "," + str(coordinates[1]) + '\n')
                        #         continue

                        coordinates = gs.get_coords(j['qid'])
                        if coordinates:
                            o.write(str(coordinates[0]) +
                                    "," + str(coordinates[1]) + '\n')
                        else:
                            # SETS THE IS_LOC TO FALSE TO PURGE ALL ENTRIES WITHOUT COORDINATES.
                            j['is_loc'] = False
                            j['qid'] = None
                            fails += 1

                        time.sleep(0.1)

                json.dump(js, jo, ensure_ascii=False)

    print(f"{fails=}")


def map_coords(filename=FILENAME_OUT_CSV):

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
    # map_coords()
