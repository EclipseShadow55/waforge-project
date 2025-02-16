import requests
import json
from urllib.parse import quote_plus


def geocode(geoclient, place):
    data = requests.get(f"https://api.opencagedata.com/geocode/v1/json?q={quote_plus(place)}&key={geoclient.key}").json()
    data = data["results"][0]["bounds"]
    lat = (data["northeast"]["lat"] + data["southwest"]["lat"]) / 2
    lng = (data["northeast"]["lng"] + data["southwest"]["lng"]) / 2
    return lat, lng

def get_weather(geoclient, weatherclient, place):
    lat, lng = geocode(geoclient, place)
    return requests.get(f"https://my.meteoblue.com/packages/basic-day?lat={lat}&lon={lng}&apikey={weatherclient.key}&format=json&temperature=F&windspeed=mph&precipitationamount=inch").json()