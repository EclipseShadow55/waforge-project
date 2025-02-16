# Description: Access point for the Amadeus API.
import json
import requests


def get_auth_token(client):
    """
    Get an authentication token from the Amadeus API.

    :param client: Client object for the Amadeus API.
        :type client: init_clients.Auth

    :return: The authentication token.
        :rtype: dict
    """
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client.key,
        "client_secret": client.secret
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, headers=headers, data=data)
    return json.loads(response.text)


def get_flight_data(client,
                    originLocationCode,
                    maxPrice,
                    departure,
                    adults,
                    returnDate = None,
                    destinationLocationCode = None,
                    children = None,
                    infants = None,
                    travelClass = None,
                    nonStopp = None):
    """
    Get flight data from the Amadeus API.

    :param client: Client object for the Amadeus API.
        :type client: init_clients.Auth
    :param originLocationCode: The origin location.
        :type originLocationCode: str
    :param destinationLocationCode: The destination location.
        :type destinationLocationCode: str
    :param departure: The departure date.
        :type departure: str
    :param returnDate: The return date.
        :type returnDate: str | None
    :param adults: The number of adults.
        :type adults: int
    :param children: The number of children.
        :type children: int | None
    :param infants: The number of infants.
        :type infants: int | None
    :param travelClass: The travel class.
        :type travelClass: str | None
    :param nonStopp: Whether the flight is non-stop.
        :type nonStopp: bool | None
    :param maxPrice: The maximum price.
        :type maxPrice: int

    :return: The flight data.
        :rtype: dict
    """
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    data = {
        "originLocationCode": originLocationCode,
        "destinationLocationCode": destinationLocationCode,
        "departureDate": departure,
        "adults": adults,
        "maxPrice": maxPrice
    }
    if returnDate is not None:
        data["returnDate"] = returnDate
    if children is not None:
        data["children"] = children
    if infants is not None:
        data["infants"] = infants
    if travelClass is not None:
        data["travelClass"] = travelClass
    if nonStopp is not None:
        data["nonStop"] = nonStopp
    headers = {
        "Authorization": f"Bearer {get_auth_token(client)['access_token']}"
    }
    response = requests.get(url, headers=headers, params=data)
    return response.json()