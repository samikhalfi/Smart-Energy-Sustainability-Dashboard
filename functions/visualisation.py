import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from functions.ml_functions import (
    load_data,
    xgboost_cross_val,
    catboost_cross_val,
    train_prophet,
    predict_xgboost,
    predict_catboost,
    predict_prophet,
    evaluate_model
)

def run_visualisations():

    file_path = 'assets/data.csv'
    df = load_data(file_path)
    st.write(df.head())
    st.write("""
    **Why XGBoost, CatBoost,     and Prophet?**

    - **XGBoost**: We use XGBoost for its strong performance in structured data and its ability to handle complex relationships. It's efficient and robust, making it ideal for electricity consumption prediction.
    
    - **CatBoost**: CatBoost excels in dealing with categorical features and requires less tuning than other models. It’s highly effective in achieving high accuracy with less preprocessing.
    
    - **Prophet**: Prophet is specifically designed for time-series forecasting, allowing us to capture seasonality and trends in energy consumption over time, making it a perfect fit for predicting future usage.

    Each of these models provides unique advantages, helping us gain insights into different aspects of our data and predictions.
    """)

    features = ['Temperature_C', 'Humidity_%', 'Wind_Speed_m/s']
    target = 'Electricity_Consumption_kWh'
    df = df.copy()


    X = df[features]
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


    xgb_model = xgboost_cross_val(X, y)
    catboost_model = catboost_cross_val(X, y)
    prophet_model = train_prophet(df)


    xgb_predictions = predict_xgboost(xgb_model, X_test)
    catboost_predictions = predict_catboost(catboost_model, X_test)
    prophet_predictions = predict_prophet(prophet_model, df)

    def to_flat_array(predictions):
        if isinstance(predictions, np.ndarray):
            return predictions.ravel()
        if isinstance(predictions, pd.DataFrame):
            return predictions.values.ravel()
        raise ValueError("Unsupported type for predictions")

    xgb_predictions = to_flat_array(xgb_predictions)
    catboost_predictions = to_flat_array(catboost_predictions)
    prophet_predictions = to_flat_array(prophet_predictions)


    xgb_mae, xgb_r2 = evaluate_model(y_test, xgb_predictions)
    catboost_mae, catboost_r2 = evaluate_model(y_test, catboost_predictions)
    prophet_mae, prophet_r2 = evaluate_model(y, prophet_predictions)  # Use the full dataset for evaluation

    st.title('Energy Consumption and Prediction Analysis')


    st.subheader('Model Evaluation Metrics')
    st.write("- **Model Evaluation Metrics**: This section presents the Mean Absolute Error (MAE) and R-squared values for each model, showing the accuracy of predictions.")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("XGBoost MAE", f"{xgb_mae:.2f}", "R-squared: {:.2f}".format(xgb_r2))
    
    with col2:
        st.metric("CatBoost MAE", f"{catboost_mae:.2f}", "R-squared: {:.2f}".format(catboost_r2))
    
    with col3:
        st.metric("Prophet MAE", f"{prophet_mae:.2f}", "R-squared: {:.2f}".format(prophet_r2))


    st.subheader('Energy Consumption')
    st.write("- **Energy Consumption**: The bar chart visualizes the daily electricity and water consumption, giving a quick overview of usage patterns.")

    energy_data = df[['Date', 'Electricity_Consumption_kWh', 'Water_Consumption_m3']].set_index('Date')
    st.bar_chart(energy_data, use_container_width=True)


    st.subheader('Energy and Water Consumption Evolution')
    st.write("- **Consumption Evolution**: The line chart shows how electricity and water consumption trends have evolved over time, highlighting patterns and changes.")
    st.line_chart(energy_data, use_container_width=True)

    st.subheader('Mean Absolute Error and R-squared Over Time')
    st.write("- **MAE and R-squared Over Time**: This area chart shows how the accuracy of our models (in terms of MAE and R-squared) changes over time.")
    mae_r2_df = pd.DataFrame({
        'Date': df['Date'],
        'MAE': [xgb_mae] * len(df),
        'R-squared': [xgb_r2] * len(df)
    }).set_index('Date')

    st.area_chart(mae_r2_df, use_container_width=True)


    def plot_predictions(true_values, predictions, model_name):
        prediction_df = pd.DataFrame({
            'Date': X_test.index,
            'True Values': true_values,
            'Predictions': predictions
        }).set_index('Date')
        
        st.subheader(f'{model_name} Predictions vs Actual')
        st.line_chart(prediction_df, use_container_width=True)
        

    st.write("- **Predictions vs Actual**: The line chart compares the true values of energy consumption with the predictions made by each model, helping to visually assess the model's performance.")
    plot_predictions(y_test, xgb_predictions, 'XGBoost')


    plot_predictions(y_test, catboost_predictions, 'CatBoost')

    def plot_forecast(forecast):
        st.write("- **Prophet Forecast**: The line chart represents the forecasted values by the Prophet model, showing expected future consumption trends based on historical data.")
        st.subheader('Prophet Forecast')
        forecast.set_index('ds', inplace=True)
        st.line_chart(forecast, use_container_width=True)


    forecast = pd.DataFrame({
        'ds': df['Date'],
        'yhat': prophet_predictions  # No need to flatten here as it's already 1D
    })

    plot_forecast(forecast)


    def plot_feature_importance(model, feature_names, title):
        importance = model.feature_importances_
        feature_importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': importance
        }).sort_values(by='Importance', ascending=False)
        st.write("- **Feature Importance**: The bar chart ranks the features used in the XGBoost and CatBoost models based on their importance in making predictions, helping to identify which variables contribute the most to the model's accuracy.")
        st.subheader(title)
        st.bar_chart(feature_importance_df.set_index('Feature'), use_container_width=True)

    plot_feature_importance(xgb_model, features, 'XGBoost Feature Importance')
    plot_feature_importance(catboost_model, features, 'CatBoost Feature Importance')


    st.markdown("""
        <style>
        .streamlit-expanderHeader {
            color: #fe735d;
        }
        .css-1v3fvcr {
            background-color: beige;
        }
        .css-1z6f9w5 {
            background-color: beige;
        }
        .css-1r7h3t8 {
            background-color: beige;
        }
        .css-hyvrjf {
            background-color: beige;
        }
        </style>
        """, unsafe_allow_html=True)
