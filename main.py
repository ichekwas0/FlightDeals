from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from datetime import datetime, timedelta

ORIGIN_CODE = "DFW"

notification_manager = NotificationManager()
add_user = input("Do you want to add a new user (yes/no)? ").lower()
if add_user == "yes":
    notification_manager.add_users()

data_manager = DataManager()
data_manager.get_sheet_data()
data_manager.get_user_data()

flight_search = FlightSearch()
sheet_data = data_manager.destination_data

today = datetime.now()
tomorrow = (today + timedelta(days=1)).strftime("%d/%m/%Y")
six_months_from_now = (today + timedelta(days=6 * 30)).strftime("%d/%m/%Y")

for data in sheet_data:
    if flight_search.find_cheapest_flights(fly_from=ORIGIN_CODE, fly_to=data['iataCode'], date_from=tomorrow,
                                           date_to=six_months_from_now, nights_in_dst_from=6, nights_in_dst_to=28,
                                           lowest_price=data['lowestPrice']):
        message = f"Subject:Low price alert\n\nOnly ${flight_search.flight_data.price} to fly from " \
                  f"{flight_search.flight_data.city_from}-{flight_search.flight_data.city_code_from} to " \
                  f"{flight_search.flight_data.city_to}-{flight_search.flight_data.city_code_to} for " \
                  f"{flight_search.flight_data.nights_in_dest} days, on {flight_search.flight_data.local_departure}"
        for user in data_manager.user_data:
            notification_manager.send_mail(message, user['email'])

# check if the iatacode key is "", if it is empty then replace all of it with what you returned from the flight search
# class
if sheet_data[0]['iataCode'] == "":
    # then update the destination_data with the iatacode value as testing
    for data in sheet_data:
        data['iataCode'] = flight_search.search_flights(data['city'])

# update sheet_data to have current iatacode values
data_manager.destination_data = sheet_data

# then we should use put request (update_sheet_data) to edit the row and add the iataCode after the iatacode has
# been added to the sheet_data
data_manager.update_sheet_data()
