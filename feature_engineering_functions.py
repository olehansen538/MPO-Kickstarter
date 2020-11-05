import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import time
import datetime as dt
import json
from pathlib import Path
import pickle
import os, glob



def string_len_w(string):
    '''Return length of string (number of word, seperated by Space).'''
    string_str = str(string)
    string_list = string_str.split()
    string_len = len(string_list)
    return string_len

def add_blurb_len_w (df):
    '''Adding column that contains the length of the Blurb (words) and returns the updated Dataframe'''
    df['blurb_len_w'] = df.apply(lambda x: string_len_w(x['blurb']), axis=1)
    return df

def string_len_slug_w(string):
    '''Returns length of string (number of words, seperated by "-").'''
    string_str = str(string)
    string_list = string_str.split("-")
    string_len = len(string_list)
    return string_len

def add_slug_len_w (df):
    '''Adding column that contains the length of the Slug (words) and returns the updated Dataframe'''
    df['slug_len_w'] = df.apply(lambda x: string_len_slug_w(x['slug']), axis=1)
    return df

def add_parent_id(df):
    '''Extracts Parent ID out of the Category json and adds the Column to Dataframe. Returns updated Dataframe'''
    df['category_parent_id'] = pd.DataFrame([json.loads(df["category"][i]).get("parent_id") for i in range(df.shape[0])])
    return df

def add_category_id(df):
    '''Extracts category ID out of the Category json and adds the Column to Dataframe. Returns updated Dataframe'''
    df['category_id'] = pd.DataFrame([json.loads(df["category"][i]).get("id") for i in range(df.shape[0])])
    return df

def add_category_name(df):
    '''Extracts category name out of the Category json and adds the Column to Dataframe. Returns updated Dataframe'''
    df['category_name'] = pd.DataFrame([json.loads(df["category"][i]).get("name") for i in range(df.shape[0])])
    return df

def fill_na(df, column_name):
    '''Fill Missings with 0 as type integer. Returns updated dataframe. eg, for parent ID and pledged per backer'''
    df[column_name] = df[column_name].fillna(0).astype("int")
    return df

# Making a list based on entry in one category and if missing adds entry of another Column
def helper_list():
    '''Making a list based on entry in one category and if missing adds entry of another Column'''
    empty = []
    for i in range(df.shape[0]):
        if df["category_parent_id"][i] != 0:
            empty.append(df["category_parent_id"][i])
        else:
            empty.append(df["category_id"][i])
    return empty

# adds helper list as column to dataframe 
def add_list_as_column(df, column_name, list_name):
    '''Adds helper list as column to dataframe and retruns updated dataframe'''
    df[column_name] = pd.DataFrame(list_name)
    return df

def add_parent_name(df, column_name1, column_name2, dictionary):
    '''based on key value in a column, column with value is added as a column and updated dataframe is returned. 
    Example:
        parents_dict = {1: "Art", 3: "Comics", 6: "Dance", 7: "Design", 9: "Fashion", 10: "Food",
                11: "Film & Video", 12: "Games", 13: "Journalism", 14: "Music", 15: "Photography", 16: "Technology",
               17: "Theater", 18: "Publishing", 26: "Crafts"}
            df["parent_name"] = df["filled_parent"].apply(lambda x: parents_dict.get(x))'''
    df[column_name1] = df[column_name2].apply(lambda x: dictionary.get(x))
    return df

#funtion to extract the month out of the number
def extract_month(number):
    '''Extracts the month out of the number and returns the month'''
    gmtime = time.gmtime(number)
    return gmtime[1]

# Adding column with month the project was launched
def adding_month_launched(df):  
    '''Adding column with month the project was launched and returns the updated dataframe'''
    df["launched_month"] = df.apply(lambda x: extract_month(x["launched_at"]), axis=1)
    return df

def duration(deadline, launched_at):
    '''Calculating difference between two timepoints and returns it in days'''
    duration = deadline - launched_at
    duration_complete = dt.timedelta(seconds=duration)
    return duration_complete.days

# Adding column with duration in days
def adding_duration(df):
    '''Adding column with duration in days and returns updated dataframe'''
    df["duration_days"] = df.apply(lambda x: duration(x["deadline"], x["launched_at"]), axis=1)
    return df

def adding_preparation(df):
    '''Adding column with preparation in days and returns updated dataframe'''
    df["preparation"] = df.apply(lambda x: duration(x["launched_at"], x["created_at"]), axis=1)
    return df

def adding_pledged_per_backer(df):
    '''Adding column that is the averaged amount pledged per backer, returns updated dataframe'''
    df['pledged_per_backer'] = (df['usd_pledged'] / df['backers_count']).round(2)
    return df

def usd_convert_goal(df, column_name, exchange_rate): 
    '''Converts a Column based on given exchange rate, rounds it to two decimal spaces  
    and returns updated dataframe, e.g. 
    df['goal'] = (df['goal'] * df['static_usd_rate']).round(2)'''
    df[column_name] = (df[column_name] * df[exchange_rate]).round(2)
    return df

def drop_rows_missings(df, column_name):
    '''Drop rows with missing values in column, eg. Blurb. Retruns dataframe.'''
    df.dropna(subset = [column_name], inplace=True)
    return df

def drop_duplicates(df, column_name):
    '''Creating dataframe and dropping all duplicates, based on a column_name (eg, ID) 
    and keep the last ("newest") duplicate'''
    df = df.drop_duplicates(subset=['id'], keep='last')
    return df

# drop rows with values certain values in a dataframe and returns updated dataframe, eg 'suspended' and 'live' in column 'state'
def drop_rows_value (df, column_name, value):
    '''drop rows with values certain values in a dataframe and returns updated dataframe'''
    df = df.drop(df[df[column_name] == value ].index)
    return df

def drop_columns(df, list_columns):
    '''Drops columns in the list and returns updated datadrame'''
    df.drop(list_columns, axis=1, inplace=True)
    return df

def convert_to_int(df, column_name):
    '''Converting Column type to Integer and returns updated df'''
    df[column_name] = df[column_name].astype("int")
    return df