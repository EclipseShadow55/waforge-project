import json
import googlemaps

def get_clients():
    with open("data.json") as f:
        data = json.load(f)
    gmap = googlemaps.Client(data["google"])

    return {"gmap": gmap}