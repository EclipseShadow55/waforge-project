import requests
from bs4 import BeautifulSoup
import urllib.parse


def scrape(url):
    return BeautifulSoup(requests.get(url).text, "html.parser")


def get_airport():
    return scrape("https://airportcodes.aero/name/A")