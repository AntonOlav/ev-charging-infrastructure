from shapely.geometry import shape, mapping
import json

with open(r"C:\Users\anton\Documents\Master-Oppgave\Kode\geo\network_43.geojson") as f:
    data = json.load(f)

for feature in data['features']:
    geometry = shape(feature['geometry'])

    feature['properties']['geometry'] = mapping(geometry)

with open("C:/Users/anton/Documents/Master-Oppgave/Kode/geo/network_43.geojson", 'w') as f:
    json.dump(data, f)
