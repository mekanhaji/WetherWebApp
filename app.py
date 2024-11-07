import streamlit as st
import pandas as pd
import requests
import json
from datetime import timezone as tmz

# Title and description for your app
st.title("How's the weather? :sun_behind_rain_cloud:")

st.subheader("Choose location")

file = "worldcities.csv"
data = pd.read_csv(file)


# Select Country
country_set = set(data.loc[:,"country"])
country = st.selectbox('Select a country', options=country_set)

country_data = data.loc[data.loc[:,"country"] == country,:]

city_set = country_data.loc[:,"city_ascii"] 

city = st.selectbox('Select a city', options=city_set)


lat = float(country_data.loc[data.loc[:,"city_ascii"] == city, "lat"])
lng = float(country_data.loc[data.loc[:,"city_ascii"] == city, "lng"])

response_current = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lng}&current_weather=true')

st.subheader("Current weather")

result_current = json.loads(response_current._content)

current = result_current["current_weather"]
temp = current["temperature"]
speed = current["windspeed"]
direction = current["winddirection"]

# Increment added or substracted from degree values for wind direction
ddeg = 11.25

# Determine wind direction based on received degrees
if direction >= (360-ddeg) or direction < (0+ddeg):
    common_dir = "N"
elif direction >= (337.5-ddeg) and direction < (337.5+ddeg):
    common_dir = "N/NW"
elif direction >= (315-ddeg) and direction < (315+ddeg):
    common_dir = "NW"
elif direction >= (292.5-ddeg) and direction < (292.5+ddeg):
    common_dir = "W/NW"
elif direction >= (270-ddeg) and direction < (270+ddeg):
    common_dir = "W"
elif direction >= (247.5-ddeg) and direction < (247.5+ddeg):
    common_dir = "W/SW"
elif direction >= (225-ddeg) and direction < (225+ddeg):
    common_dir = "SW"
elif direction >= (202.5-ddeg) and direction < (202.5+ddeg):
    common_dir = "S/SW"
elif direction >= (180-ddeg) and direction < (180+ddeg):
    common_dir = "S"
elif direction >= (157.5-ddeg) and direction < (157.5+ddeg):
    common_dir = "S/SE"
elif direction >= (135-ddeg) and direction < (135+ddeg):
    common_dir = "SE"
elif direction >= (112.5-ddeg) and direction < (112.5+ddeg):
    common_dir = "E/SE"
elif direction >= (90-ddeg) and direction < (90+ddeg):
    common_dir = "E"
elif direction >= (67.5-ddeg) and direction < (67.5+ddeg):
    common_dir = "E/NE"
elif direction >= (45-ddeg) and direction < (45+ddeg):
    common_dir = "NE"
elif direction >= (22.5-ddeg) and direction < (22.5+ddeg):
    common_dir = "N/NE"


st.info(f"The current temperature is {temp} °C. \n The wind speed is {speed} m/s. \n The wind is coming from {common_dir}.")