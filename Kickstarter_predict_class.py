import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import time
import datetime as dt
import json
from pathlib import Path
import pickle
import os, glob

import warnings 
warnings.filterwarnings('ignore')

import feature_engineering_functions as fef 


# load the model from disk
model = pickle.load(open('RF_class_kick.sav', 'rb'))
X_test = pd.read_csv('data/X_test.csv')
y_test = pd.read_csv('data/y_test.csv')


## feature Engineering

X_test = pd.concat([X_test, y_test], axis=1)

X_test.reset_index(inplace = True)


## Create new columns
# Blurb Length
X_test = fef.add_blurb_len_w(X_test)
# Slug Length
X_test = fef.add_slug_len_w(X_test)

# Category name aka parent_name
X_test = fef.add_parent_id(X_test)
X_test = fef.add_category_id(X_test)
X_test = fef.add_category_name(X_test)
X_test = fef.fill_na(X_test, 'category_parent_id')

empty = []
for i in range(X_test.shape[0]):
    if X_test["category_parent_id"][i] != 0:
        empty.append(X_test["category_parent_id"][i])
    else:
        empty.append(X_test["category_id"][i])

X_test = fef.add_list_as_column(X_test, "filled_parent", empty)
X_test = fef.add_parent_name(X_test, "parent_name", "filled_parent", {1: "Art", 3: "Comics", 6: "Dance", 7: "Design", 9: "Fashion", 10: "Food",
                11: "Film & Video", 12: "Games", 13: "Journalism", 14: "Music", 15: "Photography", 16: "Technology",
               17: "Theater", 18: "Publishing", 26: "Crafts"})

#Month launched
X_test = fef.adding_month_launched(X_test)

# Duration
X_test = fef.adding_duration(X_test)

# Preparation 
X_test = fef.adding_preparation(X_test)

# Reward Size = pledged/backer
X_test = fef.adding_pledged_per_backer(X_test)

# Coverting Goal to USD
X_test = fef.usd_convert_goal(X_test, 'goal', 'static_usd_rate')

X_test.pledged_per_backer = X_test.pledged_per_backer.fillna(0).astype("int")

X_test['state'] = np.where(X_test['state'] == 'successful', 1, 0)



## Drop rows

#Missings in 'blurb'
X_test = fef.drop_rows_missings(X_test, 'blurb')

#Duplicates
X_test = fef.drop_duplicates(X_test, 'id')


# drop rows with goals = 0
X_test = fef.drop_rows_value(X_test, 'goal', 0)


## drop columns

X_test = fef.drop_columns(X_test, ['backers_count', 'blurb', 'category', 'converted_pledged_amount',
       'country', 'created_at', 'creator', 'currency', 'currency_symbol',
       'currency_trailing_code', 'current_currency', 'deadline',
       'disable_communication', 'friends', 'fx_rate', 'id',
       'is_backing', 'is_starrable', 'is_starred', 'launched_at', 'location',
       'name', 'permissions', 'photo', 'pledged', 'profile', 'slug',
       'source_url', 'spotlight', 'state_changed_at',
       'static_usd_rate', 'urls', 'usd_type', 'category_parent_id', 'category_id', 'category_name',
       'filled_parent', 'staff_pick'])




## Drop Rows and only keep relevant categories
categories = ["Games", "Art", "Photography", "Film & Video", "Design", "Technology"]
X_test = X_test[X_test.parent_name.isin(categories)]

## get Dummies
# convert the categorical variable parent_name into dummy/indicator variables
X_test_dum2 = pd.get_dummies(X_test.parent_name, prefix='parent_name')
X_test = X_test.drop(['parent_name'], axis=1)
X_test = pd.concat([X_test, X_test_dum2], axis=1)

# making a categorical variable for launched_month q1, q2, q3, q4 
X_test.loc[X_test['launched_month'] <  4, 'time_yr'] = 'q1'
X_test.loc[(X_test['launched_month'] >=  4) & (X_test['launched_month'] <  7), 'time_yr'] = 'q2'
X_test.loc[(X_test['launched_month'] >=  7) & (X_test['launched_month'] <  10), 'time_yr'] = 'q3'
X_test.loc[X_test['launched_month'] >  9, 'time_yr'] = 'q4'

X_test_dum3 = pd.get_dummies(X_test.time_yr, prefix='time_yr')
X_test = X_test.drop(['time_yr'], axis=1)
X_test = X_test.drop(['launched_month'], axis=1)
X_test = pd.concat([X_test, X_test_dum3], axis=1)

# Drop usd_pledged because continous Target for Regression

X_test = fef.drop_columns(X_test, ['usd_pledged'])

# we have to define which columns we want to scale.
col_scale = ['goal', 'blurb_len_w', 'slug_len_w', 'duration_days', 'preparation', 'pledged_per_backer']

# Scaling with standard scaler
scaler = StandardScaler()
X_test_scaled_st = scaler.fit_transform(X_test[col_scale])
#X_test_scaled_st = scaler.transform(X_test[col_scale])

# Concatenating scaled and dummy columns 
X_test_preprocessed_st = np.concatenate([X_test_scaled_st, X_test.drop(col_scale, axis=1)], axis=1)
#X_test_preprocessed_st = np.concatenate([X_test_scaled_st, X_test.drop(col_scale, axis=1)], axis=1)

y_test = X_test['state']
X_test = X_test.drop('state', axis=1)


# Testing predictions (to determine performance)
y_pred = model.predict(X_test_preprocessed_st)
y_probs = model.predict_proba(X_test_preprocessed_st)[:, 1]


# Compute confusion matrix
cnf_matrix = confusion_matrix(y_test, y_pred, labels=[0,1])
np.set_printoptions(precision=2)

print (classification_report(y_test, y_pred))

# Plot non-normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=['failed','successful'],normalize= False,  title='Confusion matrix')

print("Completed :)")