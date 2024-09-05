import streamlit as st
import pandas as pd
import numpy as np

def generate_simulated_data(start_date, num_days):

    dates = pd.date_range(start=start_date, periods=num_days, freq='D')
    

    seasonal_effect = np.sin(2 * np.pi * dates.dayofyear / 365)  # Sinusoidal pattern for seasonality

    base_electricity = 250 
    electricity_seasonal_effect = seasonal_effect * 60
    electricity_consumption = base_electricity + electricity_seasonal_effect + np.random.normal(0, 30, size=num_days)


    base_water = 20  
    water_seasonal_effect = seasonal_effect * 8
    water_consumption = base_water + water_seasonal_effect + np.random.normal(0, 4, size=num_days)

    data = {
        'Date': dates,
        'Electricity_Consumption_kWh': np.clip(electricity_consumption, 100, 400),  
        'Tranche_1_Limit_kWh': [150]*num_days,
        'Tranche_2_Limit_kWh': [300]*num_days,
        'Tranche_3_Limit_kWh': [450]*num_days,
        'Tranche_1_Price_MAD': [0.7]*num_days, 
        'Tranche_2_Price_MAD': [1.0]*num_days, 
        'Tranche_3_Price_MAD': [1.3]*num_days,  
        'Tranche_1_Water_Limit_m3': [10]*num_days,
        'Tranche_2_Water_Limit_m3': [20]*num_days,
        'Tranche_3_Water_Limit_m3': [30]*num_days,
        'Water_Price_Tranche_1_MAD': [5.5]*num_days,  
        'Water_Price_Tranche_2_MAD': [8]*num_days,  
        'Water_Price_Tranche_3_MAD': [11]*num_days  
    }

    billing_df = pd.DataFrame(data)

    temperature = 22 + (seasonal_effect * 12) + np.random.normal(0, 6, size=num_days)  # Seasonal temperature with some noise
    humidity = 55 - (seasonal_effect * 15) + np.random.normal(0, 12, size=num_days)  # Higher humidity in winter, lower in summer
    wind_speed = 4 + np.random.normal(0, 2, size=num_days)  # Random wind speed with some variation
    rainfall = np.clip(np.random.normal(2, 1, size=num_days), 0, 10)  # Simulated rainfall in mm

    weather_data = {
        'Date': dates,
        'Temperature_C': np.clip(temperature, 5, 45),  # Temperature between 5°C and 45°C
        'Humidity_%': np.clip(humidity, 10, 90),  # Humidity between 10% and 90%
        'Wind_Speed_m/s': np.clip(wind_speed, 0, 15),  # Wind speed between 0 and 15 m/s
        'Rainfall_mm': rainfall  # Rainfall in mm
    }

    weather_df = pd.DataFrame(weather_data)

    combined_df = pd.merge(billing_df, weather_df, on='Date', how='inner')

    return combined_df

def predictions():
    st.title("Energy Consumption Prediction")

    st.write("""
    **Why We Use Generated Data and How It Was Created**

    As a data science student and developer, I often encounter situations where real-world data is confidential or unavailable. To address this, I create simulated data for thorough testing and validation. Here’s why and how:

    - **Confidentiality:** Using generated data allows us to test applications without exposing sensitive information, ensuring privacy and security.

    - **Controlled Testing:** I generate data that mimics real-world patterns to create a controlled environment for validating features and functionalities.

    - **Model Robustness:** By incorporating various patterns and scenarios, we can assess model performance under different conditions, enhancing accuracy and resilience.

    - **Expertise Applied:** The generated dataset simulates energy, water consumption, and weather trends, reflecting real-world dynamics while protecting client confidentiality.

    This approach ensures our models and applications are reliable and effective, even in the absence of actual data.
    """)

    if st.button("Test with Sample Data"):
        from functions.visualisation import run_visualisations
        run_visualisations()
    else:

        st.subheader("Enter Data to Generate Simulated Data")

        with st.form("input_form"):
            start_date = st.date_input("Start Date", value=pd.to_datetime('2022-01-01'))
            num_days = st.number_input("Number of Days", min_value=1, max_value=365*2, value=730)

            submit_button = st.form_submit_button("Generate Data")

            if submit_button:
                df = generate_simulated_data(start_date, num_days)
                st.write("Simulated Data:")
                st.write(df.head())
                df.to_csv('assets/data.csv', index=False)
                st.success("Data has been generated and saved to 'generated_data.csv'.")

if __name__ == "__main__":
    predictions()
