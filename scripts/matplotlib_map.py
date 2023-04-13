import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import get_coords as gs, wikidata_query


ELMHOOD = wikidata_query.get_qid("Älmhult")
cs = gs.get_coords(ELMHOOD)


# dummy coordinates
lons = [40.7128, -74.0060, 139.6503, 35.6895, 6.083788]  # longitude values
lats = [74.0059, 40.7128, 35.6762, 139.6917, 50.776207]  # latitude values


lons.append(cs[0])
lats.append(cs[1])

# create a new map using the Basemap toolkit
map = Basemap()

# draw the coastlines, countries, and continents
map.drawcoastlines(linewidth=0.5)
map.drawcountries(linewidth=0.5)
map.fillcontinents(color='lightgray', lake_color='white')

# convert the coordinates to map projection coordinates
x, y = map(lons, lats)

# plot the coordinates on the map
map.plot(x, y, 'bo', markersize=6)

# show the map
plt.show()


