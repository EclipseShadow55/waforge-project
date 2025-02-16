import json
from google import genai


class Auth:
    def __init__(self, key = None, secret = None, client = None):
        self.key = key
        self.secret = secret
        self.client = client


def get_clients():
    with open("creds.json") as f:
        data = json.load(f)
    gemini = Auth(client=(genai.Client(data["gemini"])))
    amadeus = Auth(key=data["amadeus"][0], secret=data["amadeus"][1])

    return {"gemini": gemini,
            "amadeus": amadeus}