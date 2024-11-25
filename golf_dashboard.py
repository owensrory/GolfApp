import flask
import requests
import pandas
import streamlit as st
from geopy.geocoders import Nominatim

wind_types = ["Into Wind", "Down Wind", "Crosswind"]

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
        
def adjusted_distance(distance, wind_speed, wind_type):
    distance = int(distance)
    wind_speed = int(wind_speed)
    percent = round(wind_speed)
    if wind_type == "Into Wind":
        result = distance + (distance/100 * percent)
    elif wind_type == "Down Wind":
        half_percent = (distance/100) / 2
        result = distance - (half_percent * percent)
    else:
        result = distance
    
    return result
        

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
wind_speed = weather_data['wind']['speed']
wind_direction = weather_data['wind']['deg']

wind_dir_string = wind_dir(wind_direction)

col1, col2 = st.columns(2)

with col1:
    st.write(f"**Wind Speed** {wind_speed} MPH")
    st.write(f"**Wind Direction** {wind_direction} Degrees, This is {wind_dir_string}")

        
with st.form("my_form"):
    distance = st.text_input("Enter the distance", value="0")
    wind_type = st.radio(
    "What type of wind is it",
    ["Into Wind", "Down Wind", "Crosswind"],
    index=None)
    
    real_distance = adjusted_distance(distance, wind_speed, wind_type)

    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write(f"Yardage: ***{distance}*** yards", f" Wind Direction: {wind_type}")
        st.write(f"Adjusted Yardage: {real_distance}")

st.caption("Golf Dashboard -Phase 1")

        