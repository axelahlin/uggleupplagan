import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import get_coords as gs, wikidata_query


#dummy list of places, connect to annotator later
places = ["Aabenraa","Aachen","Lyon","Saint-Étienne","Bastia","Abbekås"]

# dummy coordinates (nyc and addis ababa)
lats = [40.7128, 8.98367883874434]
lons = [-74.0060, 38.77507194881627]
  
for p in places:
    qid = wikidata_query.get_qid(p)
    coordinates = gs.get_coords(qid)
    lats.append(coordinates[1])
    lons.append(coordinates[0])

# create a new map
map = Basemap()
map.drawcoastlines(linewidth=0.5)
map.drawcountries(linewidth=0.5)
map.fillcontinents(color='lightgray', lake_color='white')

# convert the coordinates to map projection coordinates
x, y = map(lons, lats)
map.plot(x, y, 'bo', markersize=6)
plt.show()


