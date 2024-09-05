import streamlit as st
import streamlit_shadcn_ui as ui
from utils.api_calls import get_lat_lon, get_weather_data

def display_weather_data():
    st.write("## Weather 🌦️")
    st.write("""
        The Weather tab allows you to view current weather conditions, including temperature 🌡️, humidity 💧, cloud coverage ☁️, 
        and wind speed 🌬️ for any city you input. 

        ### Why Weather Data is Important for This Smart Platform:
        Weather data plays a crucial role in understanding energy and water consumption patterns. By analyzing weather conditions, 
        we can make more accurate predictions about future consumption and provide better recommendations on sustainability. 
        For example, higher temperatures might lead to increased energy usage for cooling, while certain weather patterns 
        can impact water availability and consumption.

        Simply enter the city name and optionally the country, then click 'Get Weather' to see the data displayed on this tab.
        """)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.header("City Input")
        city = st.text_input("City Name")
        country = st.text_input("Country Name (optional)")

        if st.button("Get Weather"):
            if city:
                with st.spinner("Fetching data..."):
                    lat, lon = get_lat_lon(city, country)
                    if lat and lon:
                        weather_data = get_weather_data(lat, lon)
                        if weather_data:
                            st.session_state.weather_data = weather_data
                            st.session_state.lat = lat
                            st.session_state.lon = lon
                        else:
                            st.error("Failed to get weather data.")
                    else:
                        st.error("Failed to get location data.")
            else:
                st.error("Please enter a city name.")

    with col2:
        if 'weather_data' in st.session_state:
            ui.card(title="Weather Data", key="weather_data_card")
            data = st.session_state.weather_data

            metric_col1, metric_col2, metric_col3 = st.columns(3)
            with metric_col1:
                ui.metric_card(
                    title="Temperature",
                    content=f"{data['temp']} °C",
                    description="Current temperature",
                    key="temp_metric"
                )
            with metric_col2:
                ui.metric_card(
                    title="Feels Like",
                    content=f"{data['feels_like']} °C",
                    description="Feels like temperature",
                    key="feels_like_metric"
                )
            with metric_col3:
                ui.metric_card(
                    title="Humidity",
                    content=f"{data['humidity']}%",
                    description="Current humidity",
                    key="humidity_metric"
                )

            metric_col4, metric_col5 = st.columns(2)
            with metric_col4:
                ui.metric_card(
                    title="Cloud Coverage",
                    content=f"{data['cloud_pct']}%",
                    description="Current cloud coverage",
                    key="cloud_coverage_metric"
                )
            with metric_col5:
                ui.metric_card(
                    title="Wind Speed",
                    content=f"{data['wind_speed']} m/s",
                    description="Current wind speed",
                    key="wind_speed_metric"
                )


            ui.card(title="Location", key="location_card")
            st.map({
                'latitude': [st.session_state.lat],
                'longitude': [st.session_state.lon]
            }, zoom=10)
        else:
            ui.card(title="Weather Data", key="no_data_card")
            st.info("Enter a city and click 'Get Weather' to see the results.")
