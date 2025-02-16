# Description: This script initializes the clients for the APIs used in the project.
import json
from google import genai


class Auth:
    """
    Class for holding clients and other auth information
    """
    def __init__(self, key = None, secret = None, client = None):
        """
        Initialize the Auth object.

        :param key: str | None - The key.
        :param secret: str | None - The secret.
        :param client: object | None - The client.
        """
        self.key = key
        self.secret = secret
        self.client = client


def get_clients():
    """
    Get the clients for the APIs used in the project.

    :return: dict - The clients for the APIs.
    """
    with open("creds.json") as f:
        data = json.load(f)
    gemini = Auth(client=(genai.Client(api_key=data["gemini"])))
    amadeus = Auth(key=data["amadeus"][0], secret=data["amadeus"][1])
    meteoblue = Auth(key=data["meteoblue"])

    return {"gemini": gemini,
            "amadeus": amadeus,
            "meteoblue": meteoblue}