# Importing the required libraries
import json
import requests
import pytz
import datetime
import os
from dotenv import load_dotenv
from prettytable import PrettyTable

load_dotenv()
table = PrettyTable()
table.field_names = ["Temperature", "Temperature Feels like", "Temperature Min", "Temperature Max",
                     "Coordinates", "Weather", "Pressure", "Humidity", "Wind", "Clouds", "Sunrise", "Sunset"]


def utc_to_ist(timestamp):
    utc_dt = datetime.datetime.utcfromtimestamp(timestamp)
    dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(
        pytz.timezone("Asia/Kolkata"))
    return dt.strftime("%Y-%m-%d %H:%M:%S %Z")


def kelvin_to_celsius(temp_kelvin):
    temp_celsius = temp_kelvin - 273.15
    temp_celsius_str = "{0:.2f}".format(temp_celsius)
    return temp_celsius_str


def get_api_data():
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            return json.loads(response.content)
        else:
            print("No such city found")
            return None
    except Exception as e:
        print(e)
        return None


def print_api_data(data):
    if data is None:
        return
    table.add_row([
        kelvin_to_celsius(data["main"]["temp"]),
        kelvin_to_celsius(data["main"]["feels_like"]),
        kelvin_to_celsius(data["main"]["temp_min"]),
        kelvin_to_celsius(data["main"]["temp_max"]),
        data["coord"],
        data["weather"][0]["description"],
        data["main"]["pressure"],
        data["main"]["humidity"],
        data["wind"]["speed"],
        data["clouds"]["all"],
        utc_to_ist(data["sys"]["sunrise"]),
        utc_to_ist(data["sys"]["sunset"])
    ])
    print(table.get_string(title=f"Weather in {city}"))
    table.clear_rows()


while True:
    city = input("Enter Your City --> ")
    API_KEY = os.getenv("API_KEY")  # API ID
    data = get_api_data()
    print_api_data(data)
    if (input("Do you want to continue (y/else any key to exit) --> ").lower() != "y"):
        break
