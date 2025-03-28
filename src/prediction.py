import xgboost as xgb
from sklearn.ensemble import AdaBoostRegressor
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import lightgbm as lgb
import numpy as np
import joblib
from hyperopt import fmin, tpe, hp, Trials

import warnings

warnings.simplefilter("ignore")


def prediction(df):

    df.drop([
    'match_id',
    'sentiment_trend',
    "program_type",
    "big_race_ethnicity",
    "little_participant__race_ethnicity",
    "rationale_for_match",
    "index"
    ], axis=True, inplace=True)
    
    timely_features = ["call_count", "avg_cadence_day", "max_cadence_day", "number_of_call_std"]
    X = df[timely_features]  # Features (all columns except 'target')

    scaler_x = joblib.load("saved/scaler_x.pkl")
    scaler_y = joblib.load("saved/scaler_y.pkl")
    model = joblib.load("saved/model.pkl")

    X_scaled = scaler_x.fit_transform(X)

    # Make predictions
    y_pred_scaled = model.predict(X_scaled)

    # Inverse transform the predictions to original scale
    y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1)).ravel()

    return y_pred

def prediction2(df:pd.DataFrame):

    timely_features = ["call_count", "avg_cadence_day", "max_cadence_day", "number_of_call_std"]
    print(df.columns)

    X = df.drop(timely_features, axis=1 ) # Features (all columns except 'target')
    scaler_x = joblib.load("saved/scaler_x_2.pkl")
    scaler_y = joblib.load("saved/scaler_y_2.pkl")
    model = joblib.load("saved/model_2.pkl")

    X_scaled = scaler_x.fit_transform(X)

    # Make predictions
    y_pred_scaled = model.predict(X_scaled)

    # Inverse transform the predictions to original scale
    y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1)).ravel()

    return y_pred