import AccessPoints.scraper as sc
import init_clients

clients = init_clients.get_clients()


def main(origin_airport: str,
         descriptors: str,
         departure_date: str,
         return_date: str,
         adults: str,
         children: str,
         infants: str,
         trav_class: str,
         non_stop: str,
         max_price: str):
    try:
        pass
        # Get location (airport) from gemini based on origin_airport, descriptors, and max_price
        # Get flight data using amadeus
    except Exception as e:
        return None


with open("stuff.txt", "w") as f:
    print(sc.get_airport().prettify(), file=f)
