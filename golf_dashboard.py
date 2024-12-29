import flask
import requests
import pandas
import streamlit as st
from geopy.geocoders import Nominatim
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()
loc = Nominatim(user_agent="GetLoc")
col1, col2 = st.columns(2)

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
        
def updatedLocation(golf_course):
    getLoc = loc.geocode(golf_course)
    location_address = getLoc.address
    
    lat = getLoc.latitude
    lon = getLoc.longitude
    geopy_api_key = os.getenv("GEOPY_API_KEY")
    
    result = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={geopy_api_key}&units=imperial")
    weather_data = result.json()
    wind_speed = weather_data['wind']['speed']
    wind_direction = weather_data['wind']['deg']
    wind_dir_string = wind_dir(wind_direction)
    
    dashboardUpdate(location_address, wind_speed, wind_direction, wind_dir_string, golf_course, lat, lon) 

def dashboardUpdate(location_address, wind_speed, wind_direction, wind_dir_string, golf_course, lat, lon):
    updateMap(golf_course, lat, lon)
    with col1:
        st.write(f"***Location***   {location_address}")
        st.write(f"**Wind Speed** {wind_speed} MPH")
        st.write(f"**Wind Direction** {wind_direction} Degrees, This is {wind_dir_string}")

        
    with st.form("my_form"):
        golf_course = st.text_input("Enter your golf course")
        distance = st.text_input("Enter the distance", value="0")
        wind_type = st.radio(
        "What type of wind is it",
        ["Into Wind", "Down Wind", "Crosswind"],
        index=None)
        
        real_distance = adjusted_distance(distance, wind_speed, wind_type)

        submitted = st.form_submit_button("Submit")
        if submitted:
            updatedLocation(golf_course)
            st.write(f"Yardage: ***{distance}*** yards", f" Wind Direction: {wind_type}")
            st.write(f"Adjusted Yardage: {real_distance}")

def updateMap(location_name, lat, lon):
    google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if location_name:
        # embed_url = f"https://www.google.com/maps/embed/v1/streetview?key={api_key}&q={golf_course.replace(' ', '+')}"
        embed_url = f"https://www.google.com/maps/embed/v1/view?key={google_maps_api_key}&center={lat},{lon}&zoom=18&maptype=satellite"
        st.markdown(f"""
            <iframe 
                width="600" 
                height="450" 
                style="border:0" 
                loading="lazy" 
                allowfullscreen 
                src="{embed_url}">
            </iframe>
        """, unsafe_allow_html=True)

def starterDashboard():
 
    # entering the default location name
    getLoc = loc.geocode("Uphall Golf Club")

    location_address = getLoc.address

    st.title("Golf Dashboard - Phase 1")

    lat = getLoc.latitude
    lon = getLoc.longitude
    geopy_api_key = os.getenv("GEOPY_API_KEY")

    result = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={geopy_api_key}&units=imperial")
    full_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={geopy_api_key}&units=imperial"
    print(full_url)
    weather_data = result.json()
    print(weather_data)
    wind_speed = weather_data['wind']['speed']
    wind_direction = weather_data['wind']['deg']

    wind_dir_string = wind_dir(wind_direction)

    with col1:
        st.write(f"***Location***   {location_address}")
        st.write(f"**Wind Speed** {wind_speed} MPH")
        st.write(f"**Wind Direction** {wind_direction} Degrees, This is {wind_dir_string}")

            
    with st.form("my_form"):
        golf_course = st.text_input("Enter your golf course")
        distance = st.text_input("Enter the distance", value="0")
        wind_type = st.radio(
        "What type of wind is it",
        ["Into Wind", "Down Wind", "Crosswind"],
        index=None)
        
        real_distance = adjusted_distance(distance, wind_speed, wind_type)

        submitted = st.form_submit_button("Submit")
        if submitted:
            updatedLocation(golf_course)
            st.write(f"Yardage: ***{distance}*** yards", f" Wind Direction: {wind_type}")
            st.write(f"Adjusted Yardage: {real_distance}")
            
    location_name = "Bathgate Golf Club"

    # Google Maps Embed URL
    google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if location_name:
        # embed_url = f"https://www.google.com/maps/embed/v1/streetview?key={api_key}&q={golf_course.replace(' ', '+')}"
        embed_url = f"https://www.google.com/maps/embed/v1/view?key={google_maps_api_key}&center={lat},{lon}&zoom=18&maptype=satellite"
        st.markdown(f"""
            <iframe 
                width="600" 
                height="450" 
                style="border:0" 
                loading="lazy" 
                allowfullscreen 
                src="{embed_url}">
            </iframe>
        """, unsafe_allow_html=True)

    st.caption("Golf Dashboard -Phase 1")
    

starterDashboard()
        