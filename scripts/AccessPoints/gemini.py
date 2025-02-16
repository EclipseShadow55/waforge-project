# Description: Access point for the Gemini Flash 2.0 Model API.
from google.genai import types
from pydantic import BaseModel
import json

class Location(BaseModel):
    """
    A location
    Used for Gemini Structured Output.

    :ivar city: The city of the location.
        :type city: str
    :ivar state: The state of the location.
        :type state: str
    :ivar country: The country of the location.
        :type country: str
    :ivar description: A short description of the location.
        :type description: str
    :ivar activities: A list of activities that can be done at the location.
        :type activities: list[str]
    :ivar warnings: A list of cons/warnings about the location.
        :type warnings: list[str] | None
    :ivar culture: str - A short description of the cultural norms of the location.
        :type culture: str
    :ivar history: A short description of the historical significance of the location.
        :type history: str
    """
    city: str
    state: str
    country: str
    description: str
    activities: list[str]
    warnings: list[str] | None
    culture: str
    history: str

class Trip(BaseModel):
    """
    A trip that can be taken.
    Used for Gemini Structured Output.

    :ivar location: The location of the trip.
        :type location: Location
    :ivar destination_airport: The name of the airport to land at.
        :type destination_airport: str
    :ivar price: The total price of the trip.
        :type price: int
    """
    location: Location
    destination_airport: str
    price: int

def get_location(client, data: str):
    """
    Get a list of locations from the Gemini model

    :param client: Client object for the Gemini API.
        :type client: client init_clients.Auth
    :param data: The data to send to the Gemini model.
        :type data: str

    :return: A list of trips that can be taken.
        :rtype: list[Trip]
    """

    sys_instruct = "\n".join([
        "You are a travel assistant that is trying to find the best places for a user to go based on some info.",
        "",
        "You get data in json dict format, like this"
        "{",
        "   'max_price': int,",
        "   'origin_airport': str,",
        "   'descriptors': list[str]",
        "}.",
        "Max price is the maximum price the user is willing to pay for the trip, origin_airport is the full name of the airport the user is starting from, and descriptors is a list of strings that describe the trip the user wants to take.",
        "Your goal is to take this information and plan out the best trip for the user.",
        "",
        "You need to return a list of trips (one is okay though), and for each you need:",
        "   the location with:",
        "       city",
        "       state (Optional, return None if there is none)",
        "       country",
        "       a short description of the location (general vibe, what's there, etc.)",
        "       a list of activities that can be done there",
        "       any cons/warnings about the place (safety, accessibility, etc.)",
        "       a short description of the cultural norms of the place",
        "       a short description of the historical significance of the place",
        "   the full english name of the airport to land at, not IATA code",
        "   a guestimated total price of the trip, including all the necessary things they might have to pay for (round tickets, hotels, food). For the price, aim for a bit below the maximum to leave some wiggle-room for bad-pricing, etc."
    ])
    response = client.client.models.generate_content(
        model='gemini-2.0-flash',
        contents=[data],
        config=types.GenerateContentConfig(response_mime_type="application/json",
                                           response_schema=list[Trip],
                                           system_instruction=sys_instruct)
    )

    return json.loads(response.text)
