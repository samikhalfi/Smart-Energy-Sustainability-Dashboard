import pandas as pd
import numpy as np
import xgboost as xgb
import catboost
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split, GridSearchCV, TimeSeriesSplit
from catboost import CatBoostRegressor
import matplotlib.pyplot as plt


def load_data(file_path):
    return pd.read_csv(file_path, parse_dates=['Date'])

def prepare_features(df, features):
    df = df.copy()
    for feature in features:
        df[feature] = df[feature].fillna(df[feature].median())
    return df

def train_test_split_dates(df, test_size=0.2):
    split_date = df['Date'].max() - pd.DateOffset(days=int(test_size * len(df)))
    train_df = df[df['Date'] <= split_date]
    test_df = df[df['Date'] > split_date]
    return train_df, test_df

def xgboost_cross_val(X, y):
    tscv = TimeSeriesSplit(n_splits=5)
    param_grid = {
        'learning_rate': [0.01, 0.1, 0.2],
        'max_depth': [3, 6, 9],
        'n_estimators': [100, 200, 300]
    }
    model = xgb.XGBRegressor(objective='reg:squarederror', eval_metric='mae')
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=tscv, scoring='neg_mean_absolute_error', n_jobs=-1)
    grid_search.fit(X, y)
    return grid_search.best_estimator_

def catboost_cross_val(X, y):
    tscv = TimeSeriesSplit(n_splits=5)
    param_grid = {
        'learning_rate': [0.01, 0.1, 0.2],
        'depth': [3, 6, 9],
        'iterations': [100, 200, 300]
    }
    model = CatBoostRegressor(loss_function='RMSE', verbose=0)
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=tscv, scoring='neg_mean_absolute_error', n_jobs=-1)
    grid_search.fit(X, y)
    return grid_search.best_estimator_


def train_prophet(df, target_col='Electricity_Consumption_kWh'):
    prophet_df = df[['Date', target_col]].rename(columns={'Date': 'ds', target_col: 'y'})
    model = Prophet(yearly_seasonality=True)  # Adjust for new seasonal patterns
    model.fit(prophet_df)
    return model

def predict_xgboost(model, X_test):
    return model.predict(X_test)


def predict_catboost(model, X_test):
    return model.predict(X_test)

def predict_prophet(model, df):
    future = df[['Date']].rename(columns={'Date': 'ds'})
    forecast = model.predict(future)
    return forecast[['ds', 'yhat']].set_index('ds')

def evaluate_model(true_values, predictions):
    return mean_absolute_error(true_values, predictions), r2_score(true_values, predictions)