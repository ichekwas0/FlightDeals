import requests
from pprint import pprint
from flight_data import FlightData
import os
from dotenv import load_dotenv

load_dotenv("keys.env")

API_KEY = os.getenv("FLIGHT_API_KEY")
LOCATION_ENDPOINT = "https://tequila-api.kiwi.com/locations/query"
SEARCH_ENDPOINT = "https://tequila-api.kiwi.com/v2/search"


# responsible for communicating with the kiwi api, to search for the cheapest flights

class FlightSearch:
    def __init__(self):
        self.flight_data = None

    def search_flights(self, city_name):
        """searches for the iataCode of a location and adds it to the spreadsheet"""
        header = {
            "apikey": API_KEY,
            "type": "application/json"
        }
        params = {
            'term': city_name
        }
        search_response = requests.get(url=LOCATION_ENDPOINT, params=params, headers=header)
        search_response.raise_for_status()
        data = search_response.json()['locations'][0]['code']
        return data

    def find_cheapest_flights(self, fly_from, fly_to, date_from, date_to, nights_in_dst_from, nights_in_dst_to,
                              lowest_price):
        """searches for the cheapest flight, and returns True if a flight can be found, false otherwise"""
        headers = {
            "apikey": API_KEY,
        }
        params = {
            "fly_from": fly_from,
            "fly_to": fly_to,
            "date_from": date_from,
            "date_to": date_to,
            "nights_in_dst_from": nights_in_dst_from,
            "nights_in_dst_to": nights_in_dst_to,
            "price_to": lowest_price,
            "curr": "USD",
        }
        search_response = requests.get(url=SEARCH_ENDPOINT, params=params, headers=headers)
        search_response.raise_for_status()
        search_data = search_response.json()

        try:
            data = search_data['data']
            if not data:
                return False
            pprint(data[0])
            print("\n")
        except KeyError:
            print("Such flight is not available")
            return False
        else:
            self.flight_data = FlightData(
                price=data[0]['price'],
                city_from=data[0]['cityFrom'],
                city_to=data[0]['cityTo'],
                city_code_from=data[0]['cityCodeFrom'],
                city_code_to=data[0]['cityCodeTo'],
                local_departure=data[0]['local_departure'].split("T")[0],
                nights_in_dest=data[0]['nightsInDest'],
            )
            return True
