#!/usr/bin/env python
# coding: utf-8

#  # Assignment 5

# In[2]:


import pandas as pd # Do not change these imports
import numpy as np
import math


# ### Part A

# In[4]:


data = {"Number of Shares" : 250000,
        "Price Per Share" : 60,
        "Debt" : 310000,
        "Excess Cash" : 1000000,
        "FCF" : 500000,
        "High Growth Rate" : 0.1,
        "rwacc": 0.09,
        "re" : 0.11}

data


# IDX is a privately held firm. You are considering making an offer to acquire the equity
# of IDX. You have been informed that the founder of IDX is willing to sell all of the firm’s
# shares (`Number of Shares`) for a price of `Price Per Share` per share. You are evaluating whether this is a fair price.
# 
# IDX currently has debt of `Debt` and excess cash of `Excess Cash`. You have estimated that
# the firm will have free cash flows of `FCF` one year from today, and that this amount will
# grow by `High Growth Rate` per year over the following three years (i.e. during years 2-4). You have also
# calculated that IDX has a weighted average cost of capital of `rwacc` and a cost of equity capital
# of `re`. In addition, you expect the future free cash flows for IDX beyond year 4 to grow at
# a constant long run annual growth rate. What long run annual growth rate in free cash flows
# would be consistent with a share price of `Price Per Share` today?
# 
# Write the function ```growth_rate```, which calculates the long run annual growth rate in the situation described above. This function takes in a dictionary `data`, formatted as above.

# In[12]:


def growth_rate(data):
    market_cap = data["Price Per Share"]*data["Number of Shares"]
    ent_val = market_cap + data["Debt"] - data["Excess Cash"]
    pvfcf = (data["FCF"]/(data["rwacc"]-data["High Growth Rate"]))*(1-((1+data["High Growth Rate"])/(1+data["rwacc"]))**3)
    pvcont = ent_val - pvfcf
    remn_cont = pvcont * ((1+data["rwacc"])**3)
    fcf_final = data["FCF"]*((1+ data["High Growth Rate"])**3)
    ann_gr = data["rwacc"] - (fcf_final/remn_cont)
    
    return ann_gr


# ### Part B

# We first need to clean up the data. For the sake of this assignment, you are provided the function ```aggregate```. However, data cleaning is the first step of any financial data analytics and thus you need to conceptually understand what is written in the function below. 
# 
# The function aggregates the supplied data to annual frequency. This function will take a  string that represents a file path to a csv file formatted like the one supplied. ```aggregate``` will output a DataFrame formatted like the one supplied. 
# 
# First, it removes all rows where ```PRC``` is 0, and where ```DIVAMT``` is 0. It is fine if after removing these rows, your aggregated DataFrame "skips" certain years.
# 
# Then, for each unique year in each CUSIP, the function adds a row to the ```output``` DataFrame. The ```CUSIP``` entry represents the CUSIP of the security, the ```Year``` entry represents which year was aggregated, the ```Dividends``` entry represents the total amount of dividends paid during the year, and the ```Price``` column represents the price of the security at the last available month of the year.
# 
# Note that the ```Dividends``` column only contains dividends paid during that year. For example, if the first available month of a certain security happens to be November 1990, then the 1990 row will only contain dividends paid in November and December of 1990.
#     
# Finally, the function removes all securities where there is only one year's data for dividends paid. 
# 
# 

# In[6]:


def aggregate(path):
    df = pd.read_csv(path) # Do not change this line of code
    
    # Drop Unneccesary columns
    df.drop(['PERMNO', 'COMNAM'], axis=1, inplace = True)
    
    # Replace all NaN values with 0
    df = df.fillna(0)
    
    # Negative is used to represent something else in the data, so abs will remove the negative
    df['PRC'] = abs(df['PRC'])
    
    # Filter out rows where price is zero or DIVAMT is zero
    df = df.loc[df["PRC"] != 0]
    df = df.loc[df["DIVAMT"] != 0]
    
    # Replace date
    df["date"] = df["date"].str.slice(stop = 4)
    
    groups = df.groupby(["CUSIP", "date"], group_keys = False)
    

    price =  groups["PRC"].agg("last")
    divs = list(groups["DIVAMT"].sum())
    cusips = list(price.index.get_level_values(0))
    year = list(price.index.get_level_values(1))
    price = list(price)
    
    
    output = pd.DataFrame(data = {
        "CUSIP" : cusips,
        "Year" : year,
        "Dividends" : divs,
        "Price" : price
    })
    
    
    # filter singletons
    groups = output.groupby(["CUSIP"], group_keys = False)
    filtered = groups.filter(lambda x: len(x) != 1).reset_index().drop(['index'], axis = 1)
    
    return filtered


# In[8]:


print(aggregate("monthlycrsp.csv"))


# Now that we have aggregated the data to annual frequency, we consider which percentage of securities are overvalued by the Dividend Discount Model. Write the function ```overvalued```, which takes in a DataFrame ```annual_data``` (this is the output of ```aggregate```). With this annual data:
# 
# 1)	Using annual dividends, for each security (identified by CUSIP), calculate the annual dividend growth. Even though some years may be "skipped" in the above data due to 0 dividends, **treat them as if they were consecutive years** in your calculations. For example, if you found that the security returned a dividend of 1 dollar in 1990, and 1.2 dollars in 1992, you should calculate the dividend growth in 1992 to be 20\%.
# 
# 2) You can calculate the average dividend growth of each security by taking the average of each security's annual dividend growth.
# 
# 3)	You can similarly calculate the equity cost of capital by calculating the annual equity cost of capital (including the dividend), and taking the average. Note that in this step and the previous, these calculations will never fail to produce a number, since we have filtered out all cases where the Dividends/Stock Price are 0, and all securities contain at least 2 entries.
# 
# 4)	Use “Dividend discount model (constant growth model)” to calculate the price on that security’s last available date.
# 
# 5)	Compare model-implied price with actual price.
# 
# You may find the ```groupby``` method for DataFrames helpful in this question.

# In[9]:


def overvalued(annual_data):
    return 0

