# Description: Main script for the website, does most of the logic
import os

from AccessPoints import gemini as gem
from AccessPoints import amadeus as amad
from AccessPoints import meteoblue as meb
import init_clients
from Tools import csv_processor as csvp
from Tools import custom_error as ce
import json
from datetime import datetime

clients = init_clients.get_clients()

def get_spec_flight_data(data) -> dict:
    cheapest_offer = data.sort(key=lambda x: float(x["price"]["total"]), reverse=False)[0]
    cost = cheapest_offer["price"]["total"]
    airline = cheapest_offer["validatingAirlineCodes"][0]
    airline = csvp.smart_get("../Data/airlines.csv", 3, airline)[0][1]
    seats = cheapest_offer["numberOfBookableSeats"]
    depart_time = cheapest_offer["itineraries"][0]["segments"][0]["departure"]["at"]
    arrival_time = cheapest_offer["itineraries"][0]["segments"][-1]["arrival"]["at"]
    depart_airport = cheapest_offer["itineraries"][0]["segments"][0]["departure"]["iataCode"]
    depart_airport = csvp.smart_get("../Data/airports.csv", 4, depart_airport)[0][1]
    arrival_airport = cheapest_offer["itineraries"][0]["segments"][-1]["arrival"]["iataCode"]
    arrival_airport = csvp.smart_get("../Data/airports.csv", 4, arrival_airport)[0][1]
    return {
        "cost": cost,
        "airline": airline,
        "seats": seats,
        "departure": {
            "time": depart_time,
            "airport": depart_airport
        },
        "arrival": {
            "time": arrival_time,
            "airport": arrival_airport
        }
    }


def valid_date(date: str) -> bool:
    """
    Check if a date is valid.

    :param date: The date to check.
        :type date: str

    :return: Whether the date is valid.
        :rtype: bool
    """
    month_max_len = lambda m, y: [31, 29 if is_leap(y) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1]
    is_leap = lambda year: year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    if len(date) != 10:
        return False
    if date[2] != "/" or date[5] != "/":
        return False
    if not date[:2].isnumeric() or not date[3:5].isnumeric() or not date[6:].isnumeric():
        return False
    if int(date[:2]) < 1 or int(date[:2]) > 12:
        return False
    if int(date[6:]) < 0:
        return False
    if int(date[3:5]) < 1 or int(date[3:5]) > month_max_len(int(date[:2]), int(date[6:])):
        return False
    return True

def format_date(date: str) -> str:
    """
    Format a date.

    :param date: The date to format.
        :type date: str

    :return: The formatted date.
        :rtype: str
    """
    return datetime.strptime(date, "%m/%d/%Y").strftime("%Y-%m-%d")

def date_compare(date1: str | datetime, date2: str | datetime, format:str="%m/%d/%Y") -> int:
    """
    Compare two dates.

    :param date1: The first date.
        :type date1: str | datetime.datetime
    :param date2: The second date.
        :type date2: str | datetime.datetime
    :param format: The format of the dates.
        :type format: str

    :return: The comparison result.
        :rtype: int
    """
    if isinstance(date1, str):
        date1 = datetime.strptime(date1, format)
    if isinstance(date2, str):
        date2 = datetime.strptime(date2, format)
    if date1 < date2:
        return -1
    elif date1 == date2:
        return 0
    else:
        return 1


def main(origin_airport,
         descriptors,
         departure_date,
         max_price,
         adults,
         return_date = None,
         children = None,
         infants = None,
         trav_class = None,
         non_stop = None):
    """
    Main function for the website, does most of the logic.

    :param origin_airport: The origin airport.
        :type origin_airport: str
    :param descriptors: The descriptors for the trip, comma-delimited.
        :type descriptors: str
    :param departure_date: The departure date.
        :type departure_date: str
    :param max_price: The maximum price.
        :type max_price: int
    :param adults: The number of adult passengers.
        :type adults: int
    :param return_date: The return date.
        :type return_date: str | None
    :param children: The number of child passengers.
        :type children: int | None
    :param infants: The number of infant passengers.
        :type infants: int | None
    :param trav_class: The travel class.
        :type trav_class: str | None
    :param non_stop: Whether the flight should be non-stop.
        :type non_stop: bool | None

    :return: The list of trips or an error.
        :rtype: Tools.custom_error.CustomException | list
    """
    try:
        # Check Inputs
        if True:
            # Check missing values (all)
            if True:
                if children == "" or children is None:
                    children = None
                if infants == "" or infants is None:
                    infants = None
                if non_stop == "" or non_stop is None:
                    non_stop = None
                if return_date == "" or return_date is None:
                    return_date = None
                if trav_class == "" or trav_class is None:
                    trav_class = None
                if descriptors == "" or descriptors is None:
                    return ce.CustomException("InvalidDescriptorsError",
                                              "The descriptors cannot be empty",
                                              ValueError("The descriptors cannot be empty"))
                if max_price == "" or max_price is None:
                    return ce.CustomException("InvalidPriceError",
                                              "The maximum price cannot be empty",
                                              ValueError("The maximum price cannot be empty"))
                if adults == "" or adults is None:
                    return ce.CustomException("InvalidPassengerError",
                                              "The number of passengers cannot be empty",
                                              ValueError("The number of passengers cannot be empty"))
                if departure_date == "" or departure_date is None:
                    return ce.CustomException("InvalidDepartureDateError",
                                              "The departure date cannot be empty",
                                              ValueError("The departure date cannot be empty"))
                if origin_airport == "" or origin_airport is None:
                    return ce.CustomException("InvalidAirportError",
                                              "The origin airport cannot be empty",
                                              ValueError("The origin airport cannot be empty"))
            # Check types (all)
            if True:
                if not isinstance(origin_airport, str):
                    return ce.CustomException("InvalidAirportError",
                                              "The origin airport must be a string",
                                              ValueError("The origin airport must be a string"))
                if not isinstance(adults, int):
                    if not isinstance(adults, str) or not adults.isnumeric():
                        return ce.CustomException("InvalidPassengerError",
                                                  "The number of passengers must be a number",
                                                  ValueError("The number of passengers must be a number"))
                    adults = int(adults)
                if not isinstance(children, int):
                    if not isinstance(children, str) or not children.isnumeric():
                        return ce.CustomException("InvalidPassengerError",
                                                  "The number of children must be a number",
                                                  ValueError("The number of children must be a number"))
                    children = int(children)
                if not isinstance(infants, int):
                    if not isinstance(infants, str) or not infants.isnumeric():
                        return ce.CustomException("InvalidPassengerError",
                                                  "The number of infants must be a number",
                                                  ValueError("The number of infants must be a number"))
                    infants = int(infants)
                if not isinstance(max_price, int):
                    if not isinstance(max_price, str) or not max_price.isnumeric():
                        return ce.CustomException("InvalidPriceError",
                                                  "The maximum price must be a number",
                                                  ValueError("The maximum price must be a number"))
                    max_price = int(max_price)
                if not isinstance(trav_class, str):
                    return ce.CustomException("InvalidClass",
                                              "The travel class must be a string",
                                              ValueError("The travel class must be a string"))
                if not isinstance(non_stop, bool):
                    if isinstance(non_stop, str):
                        if non_stop.lower() == "true":
                            non_stop = True
                        elif non_stop.lower() == "false":
                            non_stop = False
                        else:
                            return ce.CustomException("InvalidNonStopError",
                                                  "The non-stop value must be a boolean",
                                                  ValueError("The non-stop value must be a boolean"))
                    else:
                        return ce.CustomException("InvalidNonStopError",
                                                  "The non-stop value must be a boolean",
                                                  ValueError("The non-stop value must be a boolean"))
                if not isinstance(departure_date, str):
                    return ce.CustomException("InvalidDepartureDateError",
                                              "The departure date must be a string",
                                              ValueError("The departure date must be a string"))
                if not isinstance(return_date, str):
                    return ce.CustomException("InvalidReturnDateError",
                                              "The return date must be a string",
                                              ValueError("The return date must be a string"))
                if not isinstance(descriptors, str):
                    return ce.CustomException("InvalidDescriptorsError",
                                              "The descriptors must be a string",
                                              ValueError("The descriptors must be a string"))
            # Check values (all)
            if True:
                if not origin_airport.isalpha():
                    return ce.CustomException("InvalidAirportError",
                                              "The origin airport contains invalid characters",
                                              ValueError("The origin airport contains invalid characters"))
                airports = csvp.smart_get("../Data/airports.csv", 1, origin_airport)
                if len(airports) == 0:
                    return ce.CustomException("InvalidAirportError",
                                              "The specified airport could not be found",
                                              ValueError("The specified origin airport could not be found"))
                if max_price <= 0:
                    return ce.CustomException("InvalidPriceError",
                                              "The maximum price cannot be less than or equal to zero",
                                              ValueError("The maximum price cannot be less than or equal to zero"))
                if adults < 1:
                    return ce.CustomException("InvalidPassengerError",
                                              "There must be at least one adult passenger",
                                              ValueError("There must be at least one adult passenger"))
                if children < 0:
                    return ce.CustomException("InvalidPassengerError",
                                              "The number of children cannot be negative",
                                              ValueError("The number of children cannot be negative"))
                if infants < 0:
                    return ce.CustomException("InvalidPassengerError",
                                              "The number of infants cannot be negative",
                                              ValueError("The number of infants cannot be negative"))
                if adults + children > 9:
                    return ce.CustomException("TooManyPassengersError",
                                              "The number of passengers exceeds the limit of 9",
                                              ValueError("The number of passengers exceeds the limit of 9"))
                if infants > adults:
                    return ce.CustomException("TooManyInfantsError",
                                              "The number of infants exceeds the number of adults",
                                              ValueError("The number of infants exceeds the number of adults"))
                if not valid_date(departure_date):
                    return ce.CustomException("InvalidDepartureDateError",
                                              "The departure date is not a valid date",
                                              ValueError("The departure date is not a valid date"))
                if not valid_date(return_date):
                    return ce.CustomException("InvalidReturnDateError",
                                              "The return date is not a valid date",
                                              ValueError("The return date is not a valid date"))
                match date_compare(return_date, datetime.now()):
                    case -1:
                        return ce.CustomException("InvalidReturnDateError",
                                                  "The return date is before the current date",
                                                  ValueError("The return date is before the current date"))
                    case 0:
                        return ce.CustomException("InvalidReturnDateError",
                                                  "The return date is the current date",
                                                  ValueError("The return date is the current date"))
                    case 1:
                        pass
                match date_compare(departure_date, datetime.now()):
                    case -1:
                        return ce.CustomException("InvalidDepartureDateError",
                                                  "The departure date is before the current date",
                                                  ValueError("The departure date is before the current date"))
                    case 0:
                        return ce.CustomException("InvalidDepartureDateError",
                                                  "The departure date is the current date",
                                                  ValueError("The departure date is the current date"))
                    case 1:
                        pass
                if date_compare(departure_date, return_date) >= 0:
                    dep_error = ce.CustomException("InvalidDepartureDateError",
                                                   "The departure date is after the return date",
                                                   ValueError("The departure date is after the return date"))
                    ret_error = ce.CustomException("InvalidReturnDateError",
                                                   "The return date is before the departure date",
                                                   ValueError("The return date is before the departure date"))
                    return dep_error + ret_error
                if trav_class not in [None, "Economy", "Premium Economy", "Business", "First"]:
                    return ce.CustomException("InvalidClass",
                                              "The travel class is invalid",
                                              ValueError("The travel class is invalid"))
                descs = [desc.strip() for desc in descriptors.split(",")]
                for i in range(len(descs)):
                    if descs[i] == "":
                        descs.pop(i)
                if len(descs) == 0:
                    return ce.CustomException("InvalidDescriptorsError",
                                              "The descriptors cannot be empty",
                                              ValueError("The descriptors cannot be empty"))
        trip_list = gem.get_location(clients["gemini"], json.dumps({
            "max_price": max_price,
            "origin_airport": airports[0][1],
            "descriptors": descs
        }))
        flight_details = []
        if not trip_list:
            return ce.CustomException("NoTripsFoundError",
                                      "No trips were found with the specified parameters",
                                      ValueError("No trips were found with the specified parameters"))
        trip_list = [item["trip"] for item in trip_list]
        for item in trip_list:
            airports = csvp.smart_get("../Data/airports.csv", 1, item["destination_airport"])
            flight_info = amad.get_flight_data(clients["amadeus"],
                                 origin_airport,
                                 max_price,
                                 format_date(departure_date),
                                 adults,
                                 format_date(return_date) if return_date is not None else None,
                                 airports[0][4],
                                 children,
                                 infants,
                                 trav_class,
                                 non_stop)
            flight_details.append(get_spec_flight_data(flight_info["data"]))
        general_info = []
        for i in range(len(trip_list)):
            city = trip_list[i]["location"]["city"]
            state = trip_list[i]["location"]["state"]
            country = trip_list[i]["location"]["country"]
            loc = ", ".join([city, state, country]) if state is not None else ", ".join([city, country])
            weather_data = meb.get_weather(clients["geocoding"], clients["meteoblue"], loc)["data_day"]
            real_temp = {
                "min": weather_data["temperature_min"],
                "mean": weather_data["temperature_mean"],
                "max": weather_data["temperature_max"]
            }
            felt_temp = {
                "min": weather_data["felttemperature_min"],
                "mean": weather_data["felttemperature_mean"],
                "max": weather_data["felttemperature_max"]
            }
            wind_speed = {
                "min": weather_data["windspeed_min"],
                "mean": weather_data["windspeed_mean"],
                "max": weather_data["windspeed_max"]
            }
            precipitation = {
                "probability": weather_data["precipitation_probability"],
                "amount": weather_data["precipitation"]
            }
            days = []
            for i in range(7):
                days.append = {
                    "real_temp": {},
                    "felt_temp": {},
                    "wind_speed": {},
                    "precipitation": {}
                }
                days[i]["real_temp"] = {
                    "min": weather_data["temperature_min"][i],
                    "mean": weather_data["temperature_mean"][i],
                    "max": weather_data["temperature_max"][i]
                }
                days[i]["felt_temp"] = {
                    "min": weather_data["felttemperature_min"][i],
                    "mean": weather_data["felttemperature_mean"][i],
                    "max": weather_data["felttemperature_max"][i]
                }
                days[i]["wind_speed"] = {
                    "min": weather_data["windspeed_min"][i],
                    "mean": weather_data["windspeed_mean"][i],
                    "max": weather_data["windspeed_max"][i]
                }
                days[i]["precipitation"] = {
                    "probability": weather_data["precipitation_probability"][i],
                    "amount": weather_data["precipitation"][i]
                }

            general_info.append({"weather": days})
        info = [{
            "trip": trip_list[i],
            "flight": flight_details[i],
            "general": general_info[i]
        } for i in range(len(trip_list))]
        return info
    except Exception as e:
        return ce.CustomException(type(e).__name__, "An Unexpected Error Occurred, Please Try Again Later", e)

if __name__ == "__main__":
    print("Welcome to AdventureCue!")
    print("By following these instructions, you will be able to find the perfect trip for you!")
    print("Please enter the following information:")
    origin_airport = input("Enter the airport you will be departing from (eg. O'Hare, John F. Kennedy, etc.): ")
    airports = csvp.smart_get("../Data/airports.csv", 1, origin_airport)
    while len(airports) == 0:
        os.system("cls")
        origin_airport = input("The specified airport could not be found. Please enter the airport you will be departing from (eg. O'Hare, John F. Kennedy, etc.): ")
        airports = csvp.smart_get("../Data/airports.csv", 1, origin_airport)
    os.system("cls")
    descriptors = input("Enter comma-seperated descriptors for the trip (eg. beach, mountains, etc.): ")
    while descriptors == "":
        os.system("cls")
        descriptors = input("The descriptors cannot be empty. Please enter comma-seperated descriptors for the trip (eg. beach, mountains, etc.): ")
    os.system("cls")
    departure_date = input("Enter the departure date (MM/DD/YYYY): ")
    return_date = input("Enter the return date (MM/DD/YYYY) or Enter if it doesn't matter: ")
    restar_dates = False
    if not valid_date(departure_date):
        print("Please Enter a Valid Departure Date")
        restar_dates = True
    if not valid_date(return_date) and return_date != "":
        print("Please Enter a Valid Return Date or Enter if it doesn't matter")
        restar_dates = True
    if date_compare(departure_date, return_date) >= 0:
        print("The Departure Date Can Not Be After the Return Date")
        restar_dates = True
    while restar_dates:
        os.system("cls")
        departure_date = input("Enter the departure date (MM/DD/YYYY): ")
        return_date = input("Enter the return date (MM/DD/YYYY) or Enter if it doesn't matter: ")
        restar_dates = False
        if not valid_date(departure_date):
            print("Please Enter a Valid Departure Date")
            restar_dates = True
        if not valid_date(return_date) and return_date != "":
            print("Please Enter a Valid Return Date or Enter if it doesn't matter")
            restar_dates = True
        if date_compare(departure_date, return_date) >= 0:
            print("The Departure Date Can Not Be After the Return Date")
            restar_dates = True
    os.system("cls")
    max_price = input("Enter the maximum price for the trip: ")
    while not max_price.isnumeric():
        os.system("cls")
        max_price = input("The maximum price must be a number. Enter the maximum price for the trip: ")
    max_price = int(max_price)
    os.system("cls")
    adults = input("Enter the number of adult passengers: ")
    children = input("Enter the number of child passengers or Enter if there are none: ")
    infants = input("Enter the number of infant passengers or Enter if there are none: ")
    pass_restart = False
    if not adults.isnumeric():
        print("Please Enter a Valid Number of Adult Passengers")
        pass_restart = True
    if not children.isnumeric() and children != "":
        print("Please Enter a Valid Number of Child Passengers or Enter if there are none")
        pass_restart = True
    if not infants.isnumeric() and infants != "":
        print("Please Enter a Valid Number of Infant Passengers or Enter if there are none")
        pass_restart = True
    if adults.isnumeric() and children.isnumeric() and int(adults) + int(children) > 9:
        print("The Number of Passengers Can Not Exceed the Limit of 9")
        pass_restart = True
    if infants.isnumeric() and adults.isnumeric() and int(infants) > int(adults):
        print("The Number of Infants Can Not Exceed the Number of Adults")
        pass_restart = True
    while not adults.isnumeric():
        os.system("cls")
        adults = input("Enter the number of adult passengers: ")
        children = input("Enter the number of child passengers or Enter if there are none: ")
        infants = input("Enter the number of infant passengers or Enter if there are none: ")
        pass_restart = False
        if not adults.isnumeric():
            print("Please Enter a Valid Number of Adult Passengers")
            pass_restart = True
        if not children.isnumeric() and children != "":
            print("Please Enter a Valid Number of Child Passengers or Enter if there are none")
            pass_restart = True
        if not infants.isnumeric() and infants != "":
            print("Please Enter a Valid Number of Infant Passengers or Enter if there are none")
            pass_restart = True
        if int(adults) + int(children) > 9:
            print("The Number of Passengers Can Not Exceed the Limit of 9")
            pass_restart = True
        if int(infants) > int(adults):
            print("The Number of Infants Can Not Exceed the Number of Adults")
            pass_restart = True
    adults = int(adults)
    children = int(children) if children != "" else None
    infants = int(infants) if infants != "" else None
    os.system("cls")
    trav_class = input("Enter the travel class (Economy, Premium Economy, Business, First) or Enter if it doesn't matter: ")
    while trav_class not in ["Economy", "Premium Economy", "Business", "First", ""]:
        os.system("cls")
        print("Please Enter a Valid Travel Class")
        trav_class = input("Enter the travel class (Economy, Premium Economy, Business, First) or Enter if it doesn't matter: ")
    os.system("cls")
    non_stop = input("Enter whether the flight should be non-stop (True, False) or Enter if it doesn't matter: ")
    while non_stop not in ["True", "False", ""]:
        os.system("cls")
        print("Please Enter a Valid Non-Stop Value")
        non_stop = input("Enter whether the flight should be non-stop (True, False) or Enter if it doesn't matter: ")
    non_stop = True if non_stop.lower() == "true" else False
    os.system("cls")
    print("Please Wait While We Find the Perfect Trip for You!")
    data = main(origin_airport, descriptors, departure_date, max_price, adults, return_date, children, infants, trav_class, non_stop)
    print("Here is a trip that we found for you:")
    print("Trip Information:")
    print("Destination: " + data[0]["trip"]["location"]["city"])
    print("State: " + data[0]["trip"]["location"]["state"])
    print("Country: " + data[0]["trip"]["location"]["country"])
    print()
    print("Flight Information:")
    print("Airline: " + data[0]["flight"]["airline"])
    print("Cost: " + data[0]["flight"]["cost"])
    print("Number of Seats Available: " + data[0]["flight"]["seats"])
    print("Departure Time: " + data[0]["flight"]["departure"]["time"])
    print("Departure Airport: " + data[0]["flight"]["departure"]["airport"])
    print("Arrival Time: " + data[0]["flight"]["arrival"]["time"])
    print("Arrival Airport: " + data[0]["flight"]["arrival"]["airport"])
    print()
    print("Weather Information:")
    print("Day 1:")
    print("Real Temperature:")
    print("Minimum: " + data[0]["general"]["weather"][0]["real_temp"]["min"])
    print("Mean: " + data[0]["general"]["weather"][0]["real_temp"]["mean"])
    print("Maximum: " + data[0]["general"]["weather"][0]["real_temp"]["max"])
    print("Felt Temperature:")
    print("Minimum: " + data[0]["general"]["weather"][0]["felt_temp"]["min"])
    print("Mean: " + data[0]["general"]["weather"][0]["felt_temp"]["mean"])
    print("Maximum: " + data[0]["general"]["weather"][0]["felt_temp"]["max"])
    print()
    print("Wind Speed:")
    print("Minimum: " + data[0]["general"]["weather"][0]["wind_speed"]["min"])
    print("Mean: " + data[0]["general"]["weather"][0]["wind_speed"]["mean"])
    print("Maximum: " + data[0]["general"]["weather"][0]["wind_speed"]["max"])