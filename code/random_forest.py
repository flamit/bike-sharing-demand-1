import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv as csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.cross_validation import train_test_split
from math import *
from datetime import datetime

def rmsle(predicted, actual):
    error = 0
    for i in range(len(actual)):
        error += pow(log(actual[i]+1)-log(predicted[i]+1), 2)
    return sqrt(error/len(actual))

def transform_data(df):
    datetime_values = df['datetime'].values
    time_values = []
    date_values = []
    month_values = []
    weekday_values = []
    for datetime_value in datetime_values:
        datetime_object = datetime.strptime(datetime_value, '%Y-%m-%d %H:%M:%S')
        time_values.append(datetime_object.hour)
        date_values.append(datetime_object.day)
        month_values.append(datetime_object.month)
        weekday_values.append(datetime_object.weekday())
    df['time'] = time_values
    df['date'] = date_values
    df['month'] = month_values
    df['weekday'] = weekday_values
    return df


df = pd.read_csv('../data/train.csv')
test_df = pd.read_csv('../data/test.csv')

df = transform_data(df)
test_df = transform_data(test_df)

# # Convert data to categorical
# df['weather'] = df['weather'].astype('category')
# df['holiday'] = df['holiday'].astype('category')
# df['workingday'] = df['workingday'].astype('category')
# df['season'] = df['season'].astype('category')
# df['time'] = df['time'].astype('category')
# print df.dtypes

train_data = df[['season','holiday','workingday','weather','temp','atemp','humidity','windspeed','time','weekday','month','count']].values
test_data = test_df[['season','holiday','workingday','weather','temp','atemp','humidity','windspeed','time','weekday','month']].values

# Train rf
forest = RandomForestRegressor(n_estimators=120)
forest.fit(train_data[0::,1:-1], train_data[0::,-1])
output = forest.predict(test_data[0::,1::]).astype(int)
# Prepare Kaggle Submission
datetimes = test_df['datetime'].values
predictions_file = open("../data/random_forest_submission.csv", "wb")
open_file_object = csv.writer(predictions_file)
open_file_object.writerow(["datetime","count"])
open_file_object.writerows(zip(datetimes, output))
predictions_file.close()
print 'Done.'

# # Validation
# X_train, X_test, y_train, y_test = train_test_split(train_data[0::,1:-1], train_data[0::,-1], test_size=0.2, random_state=0)
# forest = RandomForestRegressor(n_estimators=120)
# forest.fit(X_train, y_train)
# output = forest.predict(X_test)
# print rmsle(output, y_test)
