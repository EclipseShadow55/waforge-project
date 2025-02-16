from encodings.utf_8 import encode, decode

import init_clients as ic
from Tools import csv_processor as csvp
import json
from AccessPoints import amadeus


clients = ic.get_clients()
client = clients['amadeus']
airport1 = csvp.smart_get('./Data/airports.csv', 1, "O'Hare")[0]
airport2 = csvp.smart_get('./Data/airports.csv', 1, "John F. Kennedy")[0]
flight_data = amadeus.get_flight_data(client, airport1[4], 8000, '2025-03-01', 2, children=3, destinationLocationCode=airport2[4])
print(flight_data)