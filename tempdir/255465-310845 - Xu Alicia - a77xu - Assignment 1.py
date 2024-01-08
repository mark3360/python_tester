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

# In[5]:


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

# In[15]:


def risk_free_rate(data):
    rate = (data['Bond Return']/data['Price']) - 1
    return rate


# b) Write the function ```payoff_A```, which returns security A’s expected payoff in one year.

# In[16]:


def payoff_A(data):
    payoffA = (1 - data['Chance of Poor Economy']) * data['A in Good Economy'] + data['Chance of Poor Economy'] * data['A in Poor Economy']
    return payoffA
    


# c)  Write the function ```Price_A```, which determines what Security A's price is today.

# In[17]:


def price_A(data):
    priceA = payoff_A(data)/(1 + risk_free_rate(data) + dictionary['A Risk Premium'])
    return priceA
    


# In[ ]:


# d) Suppose that you own one share of A, and want a risk free cash flow of 1000 dollars in 1 year. Write the function ```strategy```, which returns the amount of shares of B and C that you must buy/short in order to get the guaranteed payoff which matches that of the risk free bond.

#This function should return a list of size 2, with the first element representing the number of shares of B to buy, and the second element representing the number of shares of C to buy. (Remember that buying a negative number of shares is equivalent to shorting them!).


# In[19]:


def strategy(data):
    x = (data ['Bond Return'] - data['A in Good Economy'])/data['B in Good Economy']
    y = (data ['Bond Return'] - data['A in Poor Economy'])/data['C in Poor Economy']
    lst = [x, y]
    return lst


# In[ ]:


# e) Suppose that the price of Security C is ```c``` dollars. Write the function ```price_B```, which determines the price of security B. 


# In[21]:


def price_B(data, c):
    priceB = price_A - data['Bond Price'] + lst[1]
    return priceB


# f) Write the function ```premium_B```, which determines the risk premium of B. The price of Security C is still ```c``` dollars

# In[22]:


def premium_B(data, c):
    expected = (1 - data['Chance of Poor Economy']) * (data['B in Good Economy'] / price_B(data, c))
    premium = expected - risk_free_rate(data)
    return premium


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
# If you don't know how to use file paths, just put the data csv in the same spot you put this assignment. Then to test the function, call ```locate_prices("Module1_Data.csv")```

# In[2]:


def locate_prices(path):
    df = pd.read_csv(path) # Do not change the first two lines of this function
    
    risk_free_rate = 0.03
    
    current_lst = []
    for index, row in df.iterrows():
        total_cash = [float(row[i]) for i in range(1, 11)]
        risk_prem = float(row[11])
        
        discount_rate = risk_free_rate + risk_prem + 1
        current_price = sum(cash / discount_rate for cash in total_cash) / 10
        current_lst.append((index, current_price))
    
    smallest = min(current_lst, key=lambda x: x[1])[0]
    largest = max(current_lst, key=lambda x: x[1])[0]
    final = [smallest, largest]
    return final


# In[ ]:




