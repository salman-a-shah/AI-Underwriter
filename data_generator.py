"""
TITLE  : Data Generator
AUTHOR : Salman Shah
DATE   : Mon May 13 17:30:14 2019
"""

"""
This script adds datapoints to dataset.csv interactively through user input
"""

import math
import statistics as stats
import random
import pandas as pd
import platform
import os

CLR = 'cls' if (platform.system().lower()=='windows') else 'clear'
EXIT = 'exit'

industry_list = pd.read_csv("data\industry list.csv")

done = False
iteration = 0
message = ""

while(not done):
    """
    A single iteration of this loop generates a theoretical datapoint
    and appends it to dataset.csv
    """
    # business type
    # randomly choose one from the list of industries
    business_type = random.choices(industry_list.values[:,0].tolist())[0]
    
    # Deposits
    # a mean is chosen uniformly between 1k and 40k
    # then 3 random numbers are chosen to represent the deposit for each of the
    # last 3 months with 10-90% as standard deviation
    deposit_mean = random.uniform(1000, 40000)
    deposit_std = deposit_mean * random.uniform(0.1, 0.9)
    deposits = []
    deposits.append(max(random.gauss(deposit_mean, deposit_std),0))
    deposits.append(max(random.gauss(deposit_mean, deposit_std),0))
    deposits.append(max(random.gauss(deposit_mean, deposit_std),0))
    deposits_avg = stats.mean(deposits)
    
    # Average number of negative days with negative balance
    # gaussian: N(0,7)
    # ignore negative numbers (same as ignoring negative numbers since mean=0)
    num_neg_bal_days = math.ceil(max(random.gauss(0,7),0))
    
    # Average number of deposits each month
    # use N(mu,sigma) for mu and sigma in industry_list
    # x extracts from the dataframe the row corresponding to the selected business type
    x = industry_list.loc[industry_list['industry type']==business_type].values[0].tolist()
    mu = x[1]
    sigma = x[2]
    avg_num_of_deposits = math.ceil(random.gauss(mu,sigma))
    
    # Credit score
    # I initially defined the probability distribution based on the percentages found on experian:
    # https://www.experian.com/blogs/ask-experian/credit-education/score-basics/what-is-a-good-credit-score/
    # However, to acheive realistic numbers, I had to modify the 
    # percentages because people who seek out merchant cash advances
    # typically don't have good credit
    credit_divs = [[850,800], [799, 700], [699,550],[549,450],[449,300]]
    credit_probabilities = [0.02, 0.05, 0.41, 0.42, 0.10]
    credit_range = random.choices(population=credit_divs, weights=credit_probabilities)[0]
    credit_score = math.ceil(random.uniform(credit_range[0], credit_range[1]))
    
    # satisfactory and delinquent credit accounts
    credit_satisfactory = math.floor(random.uniform(0,35))
    credit_delinquent = math.floor(random.uniform(0,35))
    
    # Number of credit inquiries
    num_of_credit_inquiries = max(math.ceil(random.gauss(30,10)),0)
    
    # Past defaults
    # true or false
    past_default = random.choices([True,False])[0]
    
    # how long ago was the last default
    # -1 implies no known past defaults
    # age measured in number of years
    # using poisson distribution
    past_default_age = -1
    if (past_default==True):
      past_default_age = max(math.floor(random.gauss(1.5,1.5)),0)
      
    # number of current lenders
    # Past default makes it less likely that new lenders have funded 
    if (past_default==False and deposits_avg >= 5000):
        num_of_lenders = max(math.floor(random.gauss(3,1.7)), 0)
    else:
        num_of_lenders = max(math.floor(random.gauss(0.5,1)),0)
    
    # lender daily payments
    # 21.74 avg business days in a month
    # assuming the first lender typically tries to collect
    # a third of the total monthly deposit. Then the others follow
    lender_payments = []
    for i in range(num_of_lenders):
      x = (deposits_avg/(3+(i*2)))/21.74
      lender_payments.append(round(x + random.gauss(0,x*0.2),2))
      
    # Remaining calculations
    # monthly lender payment: Amount of money paid to lenders every month
    # leftover cashflow: Amount of money left over after lenders are paid off
    monthly_lender_payment = sum(lender_payments) * 21.74
    leftover_cashflow = max(deposits_avg - monthly_lender_payment, 0)
    
    # Present the business to user as a summary
    os.system(CLR)
    print("----------------------------------------------------")
    print("Synthetic Data Generator for the Machine Underwriter")
    print("----------------------------------------------------")
    print(message)
    print("\n")
    print("File #", str(iteration+1))
    print("----------------------------------------------------")
    print("Business type:", business_type)
    print("")
    print("--Deposit History--")
    print("1 month ago:", "${:,.2f}".format(round(deposits[0],2)))
    print("2 months ago:", "${:,.2f}".format(round(deposits[1],2)))
    print("3 months ago:", "${:,.2f}".format(round(deposits[2],2)))
    print("Avearge monthly deposit:", "${:,.2f}".format(round(deposits_avg,2)))
    print("Average deposit count:", avg_num_of_deposits)
    print("Number of negative balance days:", num_neg_bal_days)
    print("")
    print("--Credit--")
    print("Credit score:", credit_score)
    print("Credit accounts statisfactory / delinquent:", credit_satisfactory, "/", credit_delinquent)
    print("Credit inquiries: ", num_of_credit_inquiries)
    print("Past default:", "Yes" if past_default else "No")
    past_default_age_text = ""
    if (past_default_age == 0):
        past_default_age_text = "Less than 1 year ago"
    elif (past_default_age == 1):
        past_default_age_text = "1 year ago"
    elif (past_default_age < 0):
        past_default_age_text = "N/A"
    else:
        past_default_age_text = str(past_default_age) + " years ago"
    print("Time since last default:", past_default_age_text)
    print("")
    print("--Lenders--")
    print("Number of current lenders:", num_of_lenders)
    if (len(lender_payments) > 0): 
      print("Lender withdrawals")
    for i in range(len(lender_payments)):
      print("Lender", str(i+1), ":", "${:,.2f}".format(lender_payments[i]))
    print("Monthly lender withdrawal:", "${:,.2f}".format(monthly_lender_payment))
    print("Leftover cashflow:", "${:,.2f}".format(leftover_cashflow))
    print("----------------------------------------------------")
    print("")

    # Prompt the user to make a decision
    print("--Offer Generation--")
    print("Commands: a: approve, d: deny, s: skip, q: quit")
    print("----------------------------------------------------")
    offer, rate, days = 0.0, 0.0, 0
    approval = "Denied"
    verdict = input("Type a command: ")
    if (verdict.lower() == 'q'):
        os.system(CLR)
        print("Exiting...")
        done = True
        break
    elif (verdict.lower() == 's'):
        message = "File skipped\nDatapoint was not saved"
        continue
    elif (verdict.lower() == 'a'):
        approval = "Approved"
        offer = input("Offer: ")
        rate = input("Rate: ")
        days = input("Days: ")
        message = "Approved for " + "${:,.2f}".format(float(offer)) + " " + str(rate) + " " + str(days) + " days\nDatapoint saved"
    else:
        message = "Denied\nDatapoint saved"
    
    # Package the data into a list to append to dataset.csv
    lender_payments_str = ""
    if (len(lender_payments) == 0):
        lender_payments_str = "N/A"
    else: 
        for s in lender_payments:
            lender_payments_str = lender_payments_str + "{:.2f}".format(s) + ";"
        lender_payments_str = lender_payments_str[:-1]
    data = [business_type, 
            round(deposits[0],2), round(deposits[1],2), round(deposits[2],2), 
            round(deposits_avg,2), avg_num_of_deposits, num_neg_bal_days, 
            credit_score, credit_satisfactory, credit_delinquent, num_of_credit_inquiries, 
            past_default, past_default_age, 
            num_of_lenders, lender_payments_str, 
            round(monthly_lender_payment, 2), round(leftover_cashflow,2), 
            approval, offer, rate, days]
    datastr = ','.join([str(s) for s in data])
    
    # Save file to datset.csv
    with open("data\dataset.csv", 'a') as file:
        file.write("\n" + datastr)
    
    iteration += 1

os.system(CLR)
os.system(EXIT)