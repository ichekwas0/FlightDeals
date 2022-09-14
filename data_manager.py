import requests
import os
from dotenv import load_dotenv

load_dotenv("keys.env")

API_KEY = os.getenv("FLIGHT_API_KEY")

# responsible for communicating with sheety api
API_KEY = API_KEY
headers = {
    "apikey":  API_KEY,
}


class DataManager:
    def __init__(self):
        # create an init that saves the list as a variable
        self.destination_data = []
        self.user_data = []

# perform a get request and get the sheety data in a list
    def get_sheet_data(self):
        """gets the data from the prices sheet in the spreadsheet"""
        response = requests.get(url="https://api.sheety.co/6289147b93801c0365d3623d6475b956/flightDeals/prices",
                                headers=headers)
        data = response.json()['prices']
        for city in data:
            self.destination_data.append(city)

# write a function that writes to the sheety api, editing the country id column
    def update_sheet_data(self):
        """updates the iatacode in the spreadsheet"""
        for data in self.destination_data:
            params = {
                "price": {
                    "iataCode": data['iataCode']
                }
            }
            put_response = requests.put(url=f"https://api.sheety.co/6289147b93801c0365d3623d6475b956/flightDeals"
                                            f"/prices/{data['id']}", json=params, headers=headers)

    def get_user_data(self):
        """gets data from the user sheet in the spreadsheet"""
        user_data_headers = {
            "apikey": API_KEY
        }
        user_data_response = requests.get(url="https://api.sheety.co/6289147b93801c0365d3623d6475b956/flightDeals/users"
                                          , headers=user_data_headers)
        self.user_data = user_data_response.json()['users']
