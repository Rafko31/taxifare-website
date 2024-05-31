import streamlit as st
import datetime
import requests
import pydeck as pdk

'''
# TaxiFareModel Predictor
'''

st.markdown('''
Fare Prediction Beta Tool
''')

'''
## Want to predict the price of your ride ?

1. Fill the following form :
'''

# Create a form and give it a key
with st.form(key='my_form'):
    date_ = st.date_input("Ride Date", datetime.date(2019, 7, 6))
    time_ = st.time_input("Ride Time", datetime.time(0, 45))
    pickup_long = st.number_input("Insert a pick-up longitude", value=40.7580, format="%.6f", min_value=-180.0, max_value=180.0)
    pickup_lat = st.number_input("Insert a pick up latitude", value=-73.9855, format="%.6f", min_value=-90.0, max_value=90.0)
    dropoff_long = st.number_input("Insert a dropoff longitude", value=40.7662, format="%.6f", min_value=-180.0, max_value=180.0)
    dropoff_lat = st.number_input("Insert a dropoff latitude", value=-73.9776, format="%.6f", min_value=-90.0, max_value=90.0)
    passenger_count = st.number_input("Insert a number of passengers", min_value=1, max_value=8, step=1, format="%d")


    date_and_time= f"{date_} {time_}"

    # submit button.
    submitted = st.form_submit_button("Predict Trip Fare")
    if submitted:
        st.write("Ride Date and Time:", date_and_time)
        st.write("Pickup longitude :", pickup_long)
        st.write("Pickup latitude :", pickup_lat)
        st.write("Dropoff longitude :", dropoff_long)
        st.write("Dropoff latitude :", dropoff_lat)
        st.write("Number of passengers :", passenger_count)


# Map
        map_data = {
            "type": "FeatureCollection",
            "features": [
                {"type": "Feature", "geometry": {"type": "Point", "coordinates": [pickup_long, pickup_lat]}},
                {"type": "Feature", "geometry": {"type": "Point", "coordinates": [dropoff_long, dropoff_lat]}}
            ]
        }

        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=40.748817,
                longitude=-73.985130,
                zoom=11,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                   'ScatterplotLayer',
                   data=map_data,
                   get_position='geometry.coordinates',
                   get_color='[200, 30, 0, 160]',
                   get_radius=200,
                ),
            ],
        ))

url = 'https://taxifare.lewagon.ai/predict'

params = {
    'pickup_datetime': date_and_time,
    'pickup_longitude': pickup_long,
    'pickup_latitude': pickup_lat,
    'dropoff_longitude': dropoff_long,
    'dropoff_latitude': dropoff_lat,
    "passenger_count": passenger_count
}
response = requests.get(url, params=params)

data = response.json()

st.header(data["fare"])
