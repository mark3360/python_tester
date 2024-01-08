#!/usr/bin/env python
# coding: utf-8

# # Assignment 1

# In[1]:


import numpy as np
import pandas as pd
import math


# ## IMPORTANT INFORMATION
# 
# The Python assignments that you will write in this course will be autotested. In order to ensure that your code can be tested, it is **extremely important** that your entire file should be able to be executed without error. That is, if you navigate to ```Kernel -> Restart & Run All```, Python does not encounter an error anywhere throughout your file.
# 
# Additionally, you may not add any imports other than the ones that are at the top of the file.
# 
# Side note: You may notice that some of the functions you write on this or any subsequent assignments may take a (very) long time to run. This is okay, and you will not be penalized for this.

# ### Part A

# Consider the following dictionary, which gives information about a risk free bond, and 3 securities A B and C (It is known that security B will return nothing in a poor economy, and security C will return nothing in a good economy).

# In[2]:


info = {'Bond Return' : 1000,
     'Bond Price' : 960,
     'Chance of Poor Economy' : 0.4,
     'A in Poor Economy' : 700,
     'A in Good Economy' : 1200,
     'B in Good Economy' : 200,
     'C in Poor Economy' : 300,
     'A Risk Premium' : 0.1}


# In the rest of this part, you will write multiple functions. Each function you write will take in an argument ```data```. This argument will be a dictionary like the one formatted above. 
# 
# Additionally, for all functions you write in this class, return percentage values as decimals. For example, if your function determines that the answer is 5%, then it should return the number ```0.05```.

# a) What is the one year risk-free interest rate? Write the function ```risk_free_rate``` which returns the risk free interest rate. 

# In[3]:


def risk_free_rate(data):
    breturn = data['Bond Return']
    bprice = data['Bond Price']
    risk_free_rate = (breturn - bprice) / bprice
    return risk_free_rate


# b) Write the function ```payoff_A```, which returns security A’s expected payoff in one year.

# In[4]:


def payoff_A(data):
    chance_poor = data['Chance of Poor Economy']
    poorA_economy = data['A in Poor Economy']
    goodA_economy = data['A in Good Economy']
    payoff_A = (goodA_economy * (1 - chance_poor)) + (poorA_economy * chance_poor)
    return payoff_A


# c)  Write the function ```Price_A```, which determines what Security A's price is today.

# In[5]:


def Price_A(data):
    risk_premium = data['A Risk Premium']
    Price_A = payoff_A(data)/(risk_free_rate(data) + 1 + risk_premium)
    return Price_A


# d) Suppose that you own one share of A, and want a risk free cash flow of 1000 dollars in 1 year. Write the function ```strategy```, which returns the amount of shares of B and C that you must buy/short in order to get the guaranteed payoff which matches that of the risk free bond.
# 
# This function should return a list of size 2, with the first element representing the number of shares of B to buy, and the second element representing the number of shares of C to buy. (Remember that buying a negative number of shares is equivalent to shorting them!).

# In[6]:


def strategy(info):
    bond_return = info['Bond Return']
    bond_price = info['Bond Price']
    chance_poor_economy = info['Chance of Poor Economy']
    a_poor_economy = info['A in Poor Economy']
    a_good_economy = info['A in Good Economy']
    b_good_economy = info['B in Good Economy']
    c_poor_economy = info['C in Poor Economy']
    a_risk_premium = info['A Risk Premium']
    
    b = (bond_return - a_good_economy) / b_good_economy
    c = (bond_return - a_poor_economy) / c_poor_economy
    
    portfolio_good_economy = a_good_economy + b_good_economy * b
    portfolio_poor_economy = a_poor_economy + c_poor_economy * c
    
    expected_portfolio_value = (chance_poor_economy * portfolio_poor_economy
                                 + (1 - chance_poor_economy) * portfolio_good_economy)
    
    if expected_portfolio_value == bond_return:
        return [b, c]
    else:
        return False


# e) Suppose that the price of Security C is ```c``` dollars. Write the function ```price_B```, which determines the price of security B. 

# In[7]:


def price_B(data, c):
    price_A = data['A in Good Economy']
    bond_price = data['Bond Price']
    bond_return = data['Bond Return']
    
    # Calculate the price of security B using the Law of One Price
    price_B = price_A + c - bond_price
    
    return round(price_B, 2) 


# f) Write the function ```premium_B```, which determines the risk premium of B. The price of Security C is still ```c``` dollars

# In[8]:


def premium_B(data, c):
    chance_poor_economy = data['Chance of Poor Economy']
    chance_good_economy = 1 - chance_poor_economy
    B_with_good_economy = data['B in Good Economy']
    
    expect_return = B_with_good_economy * chance_good_economy / price_B(data, c)
    
    premium_B  = expect_return - (1 + risk_free_rate(data))
    return premium_B


# ### Part 2

# There are 100,001 securities. 
# In year 1, there are 10 equally probable states. 
# For each state, security will generate different cashflows. 
# 
# Each row corresponds to a different security.
# Col A: security number
# Col B-Col K: different cashflows for different state
# Col L: risk premium in decimal
# 
# Assume that risk free rate is 3%. 
# Which security has the smallest current price?
# Which security has the largest current price?
# 
# Write the function ```locate_prices```, which consumes a string ```path``` that represents a file path to a csv file formatted like the one supplied. This function will return list containing 2 elements: the number of the security with the smallest current price, and the number of the security with the largest current price.
# 

# In[10]:


import pandas as pd

def locate_prices(path):
    df = pd.read_csv(path) 
    current_prices = []  
    
    for i in range(0, 100001):
        row = df.iloc[i]

        cashflows_average = (row[1] + row[2] + row[3] + row[4] + row[5] +
                             row[6] + row[7] + row[8] + row[9] + row[10]) / 10
        
        risk_free_rate = 0.03 
        current_price = cashflows_average / (1 + risk_free_rate + row[11])
        current_prices.append(current_price)
    
    smallest_price = min(current_prices)
    largest_price = max(current_prices)
    
    smallest_index = current_prices.index(smallest_price)
    largest_index = current_prices.index(largest_price)
    
    return [smallest_index, largest_index]


