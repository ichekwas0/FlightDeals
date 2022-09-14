import requests
import smtplib
import os
from dotenv import load_dotenv

load_dotenv("keys.env")

API_KEY = os.getenv("FLIGHT_API_KEY")
ADD_USER_ENDPOINT = "https://api.sheety.co/6289147b93801c0365d3623d6475b956/flightDeals/users"
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")


class NotificationManager:

    def send_mail(self, message, email):
        """sends the mail"""
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=email,
                                msg=message)

    def add_users(self):
        """adds users that want to receive cheap deals to the users spreadsheet"""
        print("Welcome to Ifeanyi's Flight Club")
        print("We find the best flight deals and email you")
        first_name = input("What is your first name? ")
        last_name = input("What is your last name? ")
        email = input("What is your email? ").lower()
        verify_email = input("Enter your email again? ").lower()
        if email == verify_email:
            print("Welcome to the flight club")
            headers = {
                "apikey": API_KEY
            }
            post_params = {
              "user": {
                  "firstName": first_name,
                  "lastName": last_name,
                  "email": email
              }
            }
            add_user_response = requests.post(url=ADD_USER_ENDPOINT, json=post_params, headers=headers)
            print("Success your email has been added, look forward to deals.")
        else:
            print("Email does not match")
            return



