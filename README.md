# MPO-Kickstarter

Business case: Mr. Brain invented a Meme Master Memory and needs money for the implementation. He wants to do the project in 4 weeks, wants to get 100,000USD and wants to launch the campaign in summertime in the category photography.
Under these circumstances, will the project be successful? Furthermore we want to recommend Mr. Brain different improvements to increase his chance for success. In addition we also want to predict his potential pledged amount. 


Requirements:

condamini or conda
or pyenv with Python: 3.8.5

### Final presentation

https://docs.google.com/presentation/d/1CT6pC7G57GTv4-Bc5trhiG4ldJ0mKqcRWn7vG4x33lw/edit#slide=id.p


### Setup

Having Anaconda installed then create your ENV with

make setup-conda
With pyenv installed

make setup-pyenv

````
conda create --name kickstarter python=3.8.5
conda install -n kickstarter pytest==6.1.1
conda install -n kickstarter ipython
conda install -n kickstarter jupyterlab
conda install -n kickstarter seaborn
conda install -n kickstarter scikit-learn
conda install -n kickstarter scipy
conda install -n kickstarter -c anaconda statsmodels 
conda install -n kickstarter -c conda-forge xgboost
````

### Usage

In order to train the model and store test data in the data folder and the model in models run:

python train.py  
In order to test that predict works on a test set you created run:

python predict.py models/linear_regression_model.sav data/X_test.csv data/y_test.csv



**Description column names for business case**

name | purpose
-|-
goal | Goal amount in USD
usd_pledged | Pledged amount in USD 
state | State of the project
blurb_len_w | Number of words in blurb description
slug_len_w | Number of words in slug
duration_days | How long the project could be pledged in days
preparation | Time from day of creation until day of launch
pledged_per_backer | Average pledge per backer
parent_name | Category of the project 
time_yr | q1: January - March, q2: April - June, q3: July - September, q4: October - December


**Description of raw data columns:**

Index | Name | Interpretation
-|-|-
0 | backers_count | how many people backed the campaign
1   | blurb | a brief description of the project, probably limited in terms of number of words
2   | category | category of project, including subcategories
3   | converted_pledged_amount | amount pledged (index #25) converted into ???
 4   | country | ncountry of project
 5   | created_at | date of project creation
 6   | creator | account that created the project with lots of additional info in a dict
 7   | currency | currency of the country
 8   | currency_symbol | corresponding currency symbol
 9   | currency_trailing_code | is the currency symbol displayed after the amount?
 10  | current_currency | another currency
 11  | deadline | time and date until which the project can get pledges - evaluation of whether goal was reached will happen at this point
 12  | disable_communication | whether or not to allow for communication with backers
 13  | friends | tbd
 14  | fx_rate | rate from currency to current_currency
 15  | goal | amount of money to be collected if the project is successful
 16  | id | ID of project
 17  | is_backing | | ???
 18  | is_starrable | indicating whether the viewing user has starred this starrable
 19  | is_starred | ???
 20  | launched_at | time and date of launch - not the same as creation - launch start is the start of being able to pledge
 21  | location | location of creater - has more info in a dict
 22  | name | name of project
 23  | permissions | ???
 24  | photo | link to photo
 25  | pledged | how much was pledged until now (project still live) or until deadline (project failed/successful)
 26  | profile | link to profile
 27  | slug | info for search engines
 28  | source_url | url-link
 29  | spotlight |  project highlighted, popularity
 30  | staff_pick | was project picked and displayed by KS staff at one point?
 31  | state | status of the project
 32  | state_changed_at | when did the status last change
 33  | static_usd_rate | rate from currency to USD
 34  | urls | weblink and link to rewards
 35  | usd_pledged | pledged amount in USD
 36  | usd_type | ???



