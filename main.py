import AccessPoints.scraper as sc
import AccessPoints.geoloc as gl
import init_clients

clients = init_clients.get_clients()


def get_data(origin: str,
             descriptors: str,
             departure_date: str,
             return_date: str,
             adults: str,
             cildren: str,
             infants: str,
             trav_class: str,
             airlines: str,
             non_stop: str,
             max_price: str):
    try:
        pass
    except Exception as e:
        return None


with open("stuff.txt", "w") as f:
    print(sc.get_airport().prettify(), file=f)
