import streamlit as st
import datetime
import requests
import pydeck as pdk
import pandas as pd  # Ensure pandas is imported

'''
# TaxiFareModel Predictor
'''

st.markdown('''
## Fare Prediction Beta Tool
''')

'''
### Want to predict the price of your ride? Fill in the following form:
'''

# Create a form and give it a key
with st.form(key='my_form'):
    date_ = st.date_input("Ride Date", datetime.date(2019, 7, 6))
    time_ = st.time_input("Ride Time", datetime.time(0, 45))
    pickup_long = st.number_input("Insert a pick-up longitude", value=-73.9855, format="%.6f", min_value=-180.0, max_value=180.0)
    pickup_lat = st.number_input("Insert a pick-up latitude", value=40.7580, format="%.6f", min_value=-90.0, max_value=90.0)
    dropoff_long = st.number_input("Insert a dropoff longitude", value=-73.7781, format="%.6f", min_value=-180.0, max_value=180.0)
    dropoff_lat = st.number_input("Insert a dropoff latitude", value=40.6413, format="%.6f", min_value=-90.0, max_value=90.0)
    passenger_count = st.number_input("Insert the number of passengers", min_value=1, max_value=8, step=1, format="%d")

    date_and_time = f"{date_} {time_}"

    # submit button
    submitted = st.form_submit_button("Predict Trip Fare")
    if submitted:
        st.write("Ride Date and Time:", date_and_time)
        st.write("Pickup longitude:", pickup_long)
        st.write("Pickup latitude:", pickup_lat)
        st.write("Dropoff longitude:", dropoff_long)
        st.write("Dropoff latitude:", dropoff_lat)
        st.write("Number of passengers:", passenger_count)

        # Define map data
        route_data = pd.DataFrame({
            'lat': [pickup_lat, dropoff_lat],
            'lon': [pickup_long, dropoff_long]
        })

        # Map with line layer to show the route
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=(pickup_lat + dropoff_lat) / 2,
                longitude=(pickup_long + dropoff_long) / 2,
                zoom=12,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    "LineLayer",
                    data=pd.DataFrame({
                        'start_lon': [pickup_long],
                        'start_lat': [pickup_lat],
                        'end_lon': [dropoff_long],
                        'end_lat': [dropoff_lat]
                    }),
                    get_source_position='[start_lon, start_lat]',
                    get_target_position='[end_lon, end_lat]',
                    get_color='[200, 30, 0, 160]',
                    get_width=5,
                ),
                pdk.Layer(
                    'ScatterplotLayer',
                    data=route_data,
                    get_position='[lon, lat]',
                    get_color='[200, 30, 0, 160]',
                    get_radius=100,
                ),
            ]
        ))

# Call to API for fare prediction
if submitted:
    url = 'https://taxifare.lewagon.ai/predict'
    params = {
        'pickup_datetime': date_and_time,
        'pickup_longitude': pickup_long,
        'pickup_latitude': pickup_lat,
        'dropoff_longitude': dropoff_long,
        'dropoff_latitude': dropoff_lat,
        'passenger_count': passenger_count
    }
    response = requests.get(url, params=params)
    data = response.json()

    st.header(f"Fare: ${data['fare']}")
