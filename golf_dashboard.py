import flask
import requests
import pandas
import streamlit as st
from geopy.geocoders import Nominatim

def wind_dir(wind_direction):
    north = 0
    east = 90
    south = 180
    west = 270
    second_north = 360
    
    if wind_direction < south:
        if wind_direction < east and wind_direction is not north:
            return "North East"
        elif wind_direction > east:
            return "South East"
        elif wind_direction == east:
            return "East"
        else:
            return "North"            
    else:
        if wind_direction < west and wind_direction is not south:
            return "South West"
        elif wind_direction > west and wind_direction is not second_north:
            return "North West"
        elif wind_direction == south:
            return "South"
        else:
            return "West"

loc = Nominatim(user_agent="GetLoc")
 
# entering the location name
getLoc = loc.geocode("Bathgate")

print(getLoc.address)

st.title("Golf Dashboard - Phase 1")

lat = getLoc.latitude
lon = getLoc.longitude
api_key = "cfc54dfa691b9699aa872b7e241e0227"

result = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=imperial")
weather_data = result.json()
print(weather_data)
wind_speed = weather_data['wind']['speed']
wind_direction = weather_data['wind']['deg']

wind_dir_string = wind_dir(wind_direction)

st.write(f"**Wind Speed** {wind_speed} MPH")
st.write(f"**Wind Direction** {wind_direction} Degrees, This is {wind_dir_string}")


st.caption("Golf Dashboard -Phase 1")

        