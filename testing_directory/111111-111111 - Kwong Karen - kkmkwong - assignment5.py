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

import os
import re
import pandas as pd
import numpy as np
import time
from IPython.display import display
from timeout_decorator import timeout


class Test:
    def __init__(self, name, time, full_marks, test, student_function):
        self.name = name    # Name of test
        self.time = time    # Time allotted to run test in seconds 
        self.full_marks = full_marks   # Maximum marks on the test
        self.the_test = test 
        self.funct = student_function

# the_test is Function that takes in a function and tests that function, returns list containing
# marks awarded and feedback
                             
    
    
    
    
class Tester:
    feedback = ""
    marks_earned = 0
    total_marks = 0
    
    #expected is "correct" result, close is a list for awarding part marks.
    def run_test(self, test):
        student_function = test.funct
        self.total_marks += test.full_marks
        marks_awarded = 0
        self.feedback += f"{test.name}: " 
        
        if student_function == None:
            self.feedback += "Function Undefined!\n"
        else:
            try:
                @timeout(test.time)
                def f():
                    return test.the_test(student_function)
                result = f()
                marks_awarded = result[0]
                test_feedback = result[1]
                self.feedback += test_feedback
            
            except TimeoutError as e:
                self.feedback +=  f"Function {student_function.__name__} timed out with time limit {test.time}"
            except:
                self.feedback += f"Function {student_function.__name__} encountered error while running"
            
        self.marks_earned += marks_awarded
        self.feedback += "\n"
        self.feedback += f"{marks_awarded} / {test.full_marks}"
        self.feedback += "\n"
        self.feedback += "\n"


# Consumes a list of student functions (as strings), and returns the list containing the actual student functions.
def load_functions(lst):
    ans = []
    for f in lst:
        try:
            exec(f"ans.append({f})",globals(), locals())
        except:
            ans.append(None)
    return ans

##########################################################################################################
##########################################################################################################
# Define tests here.


equal_frame = pd.DataFrame(data = {
    "CUSIP" : ["1234","1234"],
    "Year" : [1988,1992],
    "Dividends" : [0.0625,0.625],
    "Price" : [0.3125,2.5]
})

inf_val_frame = pd.DataFrame(data = {
        "CUSIP" : ["1234","1234","1234"],
        "Year" : [1991,1992,1993],
        "Dividends" : [0.4,0.44,0.24],
        "Price" : [39,31.875,24.5]
    })


three_frame = pd.DataFrame(data = {
        "CUSIP" : ["1234","1234","1234","12345","12345","12346","12346"],
        "Year" : [1991,1992,1993,2000,2001,2000,2001],
        "Dividends" : [0.4,0.44,0.24,0.5,0.6,0.5,0.6],
        "Price" : [39,31.875,24.5,0.2,0.3,0.2,0.3]
})

not_overvalued_frame = pd.DataFrame(data = {
        "CUSIP" : ['00036020',
 '00036020',
 '00036020',
 '00036020',
 '00036020',
 '00036020',
 '00036020',
 '00036020',
 '00036020',
 '00036020',
 '00036020',
 '00036020',
 '00036020',
 '00036020',
 '00036020',
 '00036020',
 '00036020'],
        "Year" : ['2006',
 '2007',
 '2008',
 '2009',
 '2010',
 '2011',
 '2012',
 '2013',
 '2014',
 '2015',
 '2016',
 '2017',
 '2018',
 '2019',
 '2020',
 '2021',
 '2022'],
        "Dividends" : [0.4,
 0.36,
 0.32,
 0.36,
 0.36,
 0.3,
 0.36,
 0.2,
 0.22,
 0.22,
 0.24,
 0.26,
 0.32,
 0.32,
 0.38,
 0.38,
 0.43],
        "Price" : [26.28,
 19.82,
 20.88,
 19.49,
 25.65,
 21.91,
 21.05,
 30.77,
 20.72,
 24.71,
 32.9,
 36.45,
 37.95,
 49.37,
 65.13,
 78.0,
 79.26]
    })

reg_overvalued_frame = pd.DataFrame(data = {
        "CUSIP" : ['00037520',
 '00037520',
 '00037520',
 '00037520',
 '00037520',
 '00037520',
 '00037520',
 '00037520',
 '00037520',
 '00037520',
 '00037520',
 '00037520',
 '00037520',
 '00037520',
 '00037520',
 '00037520',
 '00037520',
 '00037520'],
        "Year" : ['2003',
 '2006',
 '2007',
 '2008',
 '2009',
 '2010',
 '2011',
 '2012',
 '2013',
 '2014',
 '2015',
 '2016',
 '2017',
 '2018',
 '2019',
 '2020',
 '2021',
 '2022'],
        "Dividends" : [1.23019,
 0.09396,
 0.19815,
 0.45252,
 0.44498,
 0.48392,
 0.67267,
 0.70285,
 0.73776,
 0.78865,
 0.7669199999999999,
 0.75058,
 0.75457,
 0.82606,
 0.79721,
 0.77407,
 0.87432,
 1.81466],
        "Price" : [5.08,
 12.62,
 21.47,
 26.22,
 18.28,
 20.18,
 26.9,
 15.81,
 22.57,
 23.74,
 20.28,
 21.25,
 24.6,
 23.27,
 18.18,
 17.26,
 30.47,
 27.84]
    })

data_partA = {"Number of Shares" : 250000,
        "Price Per Share" : 60,
        "Debt" : 310000,
        "Excess Cash" : 1000000,
        "FCF" : 500000,
        "High Growth Rate" : 0.1,
        "rwacc": 0.09,
        "rd" : 0.10}

def g_rate(f):
    pts = 0
    res = f(data_partA)
    ans = 0.0502
    
    if round(res, 4) == ans:
        feedback = "Test passed!"
        pts = 2
    else:
        feedback = f"Test failed, saw {res}, but expected {ans}"
    return [pts, feedback]

def ov_1(f):
    pts = 0
    res = f(reg_overvalued_frame)
    ans = 1
    
    if round(res, 4) == ans:
        feedback = "Test passed!"
        pts = 1
    else:
        feedback = f"Test checking an overvalued security with re > g failed."
    return [pts, feedback]

def ov_2(f):
    pts = 0
    res = f(not_overvalued_frame)
    ans = 0
    
    if round(res, 4) == ans:
        feedback = "Test passed!"
        pts = 1
    else:
        feedback = f"Test checking an non-overvalued security with re > g failed."
    return [pts, feedback]

def ov_3(f):
    pts = 0
    res = f(inf_val_frame)
    ans = 1
    
    if round(res, 4) == ans:
        feedback = "Test passed!"
        pts = 1
    else:
        feedback = f"Test checking a security with re < g failed."
    return [pts, feedback]

def ov_4(f):
    pts = 0
    res = f(equal_frame)
    ans = 1
    
    if round(res, 4) == ans:
        feedback = "Test passed!"
        pts = 1
    else:
        feedback = f"Test checking a security with re = g failed."
    return [pts, feedback]


def ov_5(f):
    pts = 0
    res = f(three_frame)
    ans = 0.3333
    
    if round(res, 4) == ans:
        feedback = "Test passed!"
        pts = 2
    else:
        feedback = f"Test checking multiple different securities failed."
    return [pts, feedback]



# Load student functions
sf = load_functions(["growth_rate", "overvalued"])

# Order is name, time, full_marks, test

test_1 = Test("growth_rate_test",10, 2, g_rate, sf[0])

ovt_1 = Test("overvalued_test1",10, 1, ov_1, sf[1])
ovt_2 = Test("overvalued_test2",10, 1, ov_2, sf[1])
ovt_3 = Test("overvalued_test3",10, 1, ov_3, sf[1])
ovt_4 = Test("overvalued_test4",10, 1, ov_4, sf[1])
ovt_5 = Test("overvalued_test5",10, 2, ov_5, sf[1])

# Place all tests in list below
the_tests = [test_1, ovt_1, ovt_2, ovt_3, ovt_4, ovt_5]


##########################################################################################################
##########################################################################################################
## The actual testing

filename = os.path.basename(__file__)
lst = filename.split(" - ")
del lst[4:]

(file_id, name, watiam, fileid) = lst


print(f"Testing {watiam}") 

feedback = f"Feedback for {watiam}:\n\n"

the_tester = Tester()
    
    
        
for test in the_tests:
    the_tester.run_test(test)

feedback += the_tester.feedback
total = the_tester.total_marks
score = the_tester.marks_earned
x = round(100*score/total, 4)


feedback += f"Total: {score}/{total}:         {x}% \n"

filename = "../feedback/" + file_id + " - " +  name + " - " +  watiam + " - " +  "feedback.txt"

with open(filename, 'w') as fp:
	fp.write(feedback)

grades_df = pd.read_csv("../grades.csv").set_index("Username")
grades_df.at["#" + watiam, "Module 5 Python Points Grade <Numeric MaxPoints:100 Weight:6.25 Category:Python exercises CategoryWeight:20>"] = x

grades_df.to_csv("../grades.csv")
