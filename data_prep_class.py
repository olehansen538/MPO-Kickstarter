# import packages
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
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


### Merge and Read files

path = '/Users/petrapinger/neuefische/MPO-Kickstarter/data'

def read_files():
    """ Only create new csv if not already done"""
    if not Path("./data/Kickstarter_merged.csv").exists():
        # Read and merge .csv-files
        # Read all .csv-files
        all_files = glob.glob(os.path.join(path, "Kickstarter*.csv"))
        df_from_each_file = (pd.read_csv(f, sep=',') for f in all_files)
        # Merge .csv-files
        df_merged = pd.concat(df_from_each_file, ignore_index=True)
        df_merged.to_csv('./data/Kickstarter_merged.csv')
    """Otherwise just read in dataframe from merged .csv file"""
    return pd.read_csv('./data/Kickstarter_merged.csv', index_col=0)


df = read_files()

# drop rows with suspended, live and canceled status
df = fef.drop_rows_value(df, 'state', 'suspended')
df = fef.drop_rows_value(df, 'state', 'live')
df = fef.drop_rows_value(df, 'state', 'canceled')

## splitting into X and y 
y = df.state
X = df.drop('state', axis=1)

# splittin into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify = y)
## in order to exemplify how the predict will work.. we will save the y_train
print("Saving test data in the data folder")
X_test.to_csv("data/X_test.csv", index=False)
y_test.to_csv("data/y_test.csv", index=False)


X_train = pd.concat([X_train, y_train], axis=1)

X_train.reset_index(inplace = True)
X_test.reset_index(inplace= True)
#y_train.reset_index(inplace = True)
#y_test.reset_index(inplace = True)


## Create new columns
# Blurb Length
X_train = fef.add_blurb_len_w(X_train)
# Slug Length
X_train = fef.add_slug_len_w(X_train)

# Category name aka parent_name
X_train = fef.add_parent_id(X_train)
X_train = fef.add_category_id(X_train)
X_train = fef.add_category_name(X_train)
X_train = fef.fill_na(X_train, 'category_parent_id')

empty = []
for i in range(X_train.shape[0]):
    if X_train["category_parent_id"][i] != 0:
        empty.append(X_train["category_parent_id"][i])
    else:
        empty.append(X_train["category_id"][i])

X_train = fef.add_list_as_column(X_train, "filled_parent", empty)
X_train = fef.add_parent_name(X_train, "parent_name", "filled_parent", {1: "Art", 3: "Comics", 6: "Dance", 7: "Design", 9: "Fashion", 10: "Food",
                11: "Film & Video", 12: "Games", 13: "Journalism", 14: "Music", 15: "Photography", 16: "Technology",
               17: "Theater", 18: "Publishing", 26: "Crafts"})

#Month launched
X_train = fef.adding_month_launched(X_train)

# Duration
X_train = fef.adding_duration(X_train)

# Preparation 
X_train = fef.adding_preparation(X_train)

# Reward Size = pledged/backer
X_train = fef.adding_pledged_per_backer(X_train)

# Coverting Goal to USD
X_train = fef.usd_convert_goal(X_train, 'goal', 'static_usd_rate')

X_train.pledged_per_backer = X_train.pledged_per_backer.fillna(0).astype("int")

X_train['state'] = np.where(X_train['state'] == 'successful', 1, 0)



## Drop rows

#Missings in 'blurb'
X_train = fef.drop_rows_missings(X_train, 'blurb')

#Duplicates
X_train = fef.drop_duplicates(X_train, 'id')


# drop rows with goals = 0
X_train = fef.drop_rows_value(X_train, 'goal', 0)


## drop columns

X_train = fef.drop_columns(X_train, ['backers_count', 'blurb', 'category', 'converted_pledged_amount',
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
X_train = X_train[X_train.parent_name.isin(categories)]

## get Dummies
# convert the categorical variable parent_name into dummy/indicator variables
X_train_dum2 = pd.get_dummies(X_train.parent_name, prefix='parent_name')
X_train = X_train.drop(['parent_name'], axis=1)
X_train = pd.concat([X_train, X_train_dum2], axis=1)

# making a categorical variable for launched_month q1, q2, q3, q4 
X_train.loc[X_train['launched_month'] <  4, 'time_yr'] = 'q1'
X_train.loc[(X_train['launched_month'] >=  4) & (X_train['launched_month'] <  7), 'time_yr'] = 'q2'
X_train.loc[(X_train['launched_month'] >=  7) & (X_train['launched_month'] <  10), 'time_yr'] = 'q3'
X_train.loc[X_train['launched_month'] >  9, 'time_yr'] = 'q4'

X_train_dum3 = pd.get_dummies(X_train.time_yr, prefix='time_yr')
X_train = X_train.drop(['time_yr'], axis=1)
X_train = X_train.drop(['launched_month'], axis=1)
X_train = pd.concat([X_train, X_train_dum3], axis=1)

# Drop usd_pledged because continous Target for Regression

X_train = fef.drop_columns(X_train, ['usd_pledged'])


y_train = X_train['state']
X_train = X_train.drop('state', axis=1)
X_train = X_train.drop('index', axis=1)

# we have to define which columns we want to scale.
col_scale = ['goal', 'blurb_len_w', 'slug_len_w', 'duration_days', 'preparation', 'pledged_per_backer']

# Scaling with standard scaler
scaler = StandardScaler()
X_train_scaled_st = scaler.fit_transform(X_train[col_scale])
#X_test_scaled_st = scaler.transform(X_test[col_scale])

# Concatenating scaled and dummy columns 
X_train_preprocessed_st = np.concatenate([X_train_scaled_st, X_train.drop(col_scale, axis=1)], axis=1)
#X_test_preprocessed_st = np.concatenate([X_test_scaled_st, X_test.drop(col_scale, axis=1)], axis=1)



# Create the model with 100 trees
model = RandomForestClassifier(n_estimators=100, 
                               random_state=42, 
                               max_features = 'sqrt',
                               n_jobs=-1, verbose = 1)

# Fit on training data
model.fit(X_train_preprocessed_st, y_train)

print(X_train_preprocessed_st.shape)

#saving the model
print("Saving model in the model folder")
filename = 'RF_class_kick.sav'
pickle.dump(model, open(filename, 'wb'))

print("Completed")




