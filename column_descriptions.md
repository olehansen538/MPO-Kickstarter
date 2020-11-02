**Description of raw data columns:**

Index | Name | Nulls (out of 209222) | Type | Interpretation
-|-|-|-|-
0 | backers_count | none | int64 | how many people backed the campaign
1   | blurb | 8 | object | a brief description of the project, probably limited in terms of number of words
2   | category | none | object | category of project, including subcategories
3   | converted_pledged_amount | none | int64 | amount pledged (index #25) converted into ???
 4   | country | none | object | country of project (???) not necessarily the same as the country in location (index #21)
 5   | created_at | none | int64 | time of project creation
 6   | creator | none | object | account that created the project with lots of additional info in a dict
 7   | currency | none | object | currency (but of what???)
 8   | currency_symbol | none | object | corresponding currency symbol
 9   | currency_trailing_code | none | bool | is the currency symbol displayed after the amount?
 10  | current_currency | none | object | another currency
 11  | deadline | none | int64 | time and date until which the project can get pledges - evaluation of whether goal was reached will happen at this point
 12  | disable_communication | none | bool | whether or not to allow for communication with backers
 13  | friends | 206222 | object | tbd
 14  | fx_rate | none | float64 | another rate ???
 15  | goal | none | float64 | amount of money to be collected if the project is successful
 16  | id | none | int64 | ID of project
 17  | is_backing | 206222 | object | ???
 18  | is_starrable | none | bool | ???
 19  | is_starred | 206222 | object | ???
 20  | launched_at | none | int64 | time and date of launch - not the same as creation - launch start is the start of being able to pledge
 21  | location | 226 | object | location of creater (???) - has more info in a dict
 22  | name | none | object | name of project
 23  | permissions | 206222 | object | ???
 24  | photo | none | object | ???
 25  | pledged | none | float64 | how much was pledged until now (project still live) or until deadline (project failed/successful)
 26  | profile | none | object | ???
 27  | slug | none | object | info for search engines
 28  | source_url | none | object | ???
 29  | spotlight | none | bool | ???
 30  | staff_pick | none | bool | was project picked and displayed by KS staff at one point?
 31  | state | none | object | status of the project
 32  | state_changed_at | none | int64 | when did the status last change
 33  | static_usd_rate | none | float64 | ???
 34  | urls | none | object | ???
 35  | usd_pledged | none | float64 | ???
 36  | usd_type | 480 | object | ???


**New columns**
name | purpose
-|-
len_blurb | How many words were used in the blurb description
category_in_blurb | Is the category or subcategory mentioned in the blurb
category_id | Subcategory of project
category_parent | Category of project
catgeroy_name | Name of either category or subcategory
duration | How long the project could be pledged in days
preparation | How many days between creation and launch of project site
ind_pledge | Average pledge per contributor
