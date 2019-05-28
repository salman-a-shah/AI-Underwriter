"""
TITLE  : The main underwriter
AUTHOR : Salman Shah
DATE   : Mon May 27 14:48:22 2019
"""

def new_user_input():
    """
    Prompts the user to type in a datapoint through a series of questions
    Returns the data as a (1,39) array
    """
    import pandas as pd
    import statistics as stats
    
    #initialize a dataframe to collect information into
    dataset = pd.read_csv("data\dataset_cleaned.csv", nrows=1)
    industries = pd.read_csv("data\industry list.csv")
    df = pd.DataFrame([], columns=dataset.columns[:-4])
    zeroes = [0]*df.shape[1]
    df = pd.concat([df, pd.DataFrame([zeroes], columns=df.columns)], axis=0)
    
    # collect inputs from user
    for i in range(industries.shape[0]):
        print(i+1, ":", industries['industry type'][i])
    print("---")
    index = int(input("Choose a number for industry: "))-1
    business_type = industries['industry type'][index]
    print("----------------")
    print("Bank information")
    print("----------------")
    deposits = []
    deposits.append(float(input("Deposit 1 month ago:  ")))
    deposits.append(float(input("Deposit 2 months ago: ")))
    deposits.append(float(input("Deposit 3 months ago: ")))
    deposits_avg = stats.mean(deposits)
    avg_num_of_deposits = input("Average number of deposits per month: ")
    num_neg_bal_days = input("Average number of days with negative balance: ")
    print("------------------")
    print("Credit information")
    print("------------------")
    credit_score = input("Credit score: ")
    credit_satisfactory = input("Number of satisfactory credit accounts: ")
    credit_delinquent = input("Number of delinquent credit accounts: ")
    num_of_credit_inquiries = input("Total number of credit inquiries: ")
    past_default = input("Has this merchant defaulted before? (y/n): ")
    past_default = True if past_default.lower() == 'y' else False
    past_default_age = -1
    if (past_default):
        past_default_age = input("Time since last default (yrs): ")
    print("------------------")
    print("Lender information")
    print("------------------")
    num_of_lenders = int(input("Number of current lenders: "))
    lender_payments = []
    for i in range(min(num_of_lenders,7)):
        lender_payments.append(float(input("Daily payment for lender " + str(i+1) + ": ")))
    monthly_lender_payment = sum(lender_payments) * 21.74
    leftover_cashflow = max(deposits_avg - monthly_lender_payment, 0)
    
    while (len(lender_payments) < 7):
        lender_payments.append(0.0)
    
    # place user inputs in dataframe 
    c = dataset.columns
    if (business_type != "AUTO REPAIR SHOP"):
        df[business_type] = 1
    df[c[17]] = deposits[0]
    df[c[18]] = deposits[1]
    df[c[19]] = deposits[2]
    df[c[20]] = deposits_avg
    df[c[21]] = avg_num_of_deposits
    df[c[22]] = num_neg_bal_days
    df[c[23]] = credit_score
    df[c[24]] = credit_satisfactory
    df[c[25]] = credit_delinquent
    df[c[26]] = num_of_credit_inquiries
    df[c[27]] = 1 if past_default else 0
    df[c[28]] = past_default_age
    df[c[29]] = num_of_lenders
    for i in range(7):
        df[c[30+i]] = lender_payments[i]
    df[c[37]] = monthly_lender_payment
    df[c[38]] = leftover_cashflow
    
    return df.values
    
def make_offer(data):
    """
    Use trained models to make an offer
    Returns a list containing
    {
       status:  approved or denied
       offer:   dollar amount offered
       rate:    interest rate
       term:    payback term in # of days
       payment: the daily payment
    }
    """
    from sklearn.externals import joblib
    import numpy as np
    
    approval_clf = joblib.load(r"saved_models\approval_model.sav")
    payment_reg = joblib.load(r"saved_models\payment_model.sav")
    term_reg = joblib.load(r"saved_models\term_model.sav")
    
    status = "Denied"
    offer, rate, term, payment = 0, 0.0, 0, 0.0
    approval = int(approval_clf.predict(data))
    if (approval == 1):
        payment = float(payment_reg.predict(data).round(2))
        term = int(np.around(term_reg.predict(data)/5)*5)
        rate = 1.45

        offer = int(round((payment * term) / rate, -2))
        payment = round(offer * rate / term, 2)
        status = "Approved"

    return [status, offer, rate, term, payment]

def offer_tostring(offerlist):
    """
    Returns a predicted offer in string format
    """    
    width = 20
    s = str(offerlist[0])
    if (offerlist[0] == 'Approved'):
        s = s + "\n"
        s = s + "Offer:   " + ("$ {:,.2f}".format(offerlist[1])).rjust(width) + "\n"
        s = s + "Rate:    " + ("{:.2f}".format(offerlist[2])).rjust(width) + "\n"
        s = s + "Term:    " + (str(offerlist[3]) + " days").rjust(width) + "\n"
        s = s + "Payment: " + ("$ {:,.2f}".format(offerlist[4])).rjust(width)
        
    return s

""" example input for testing """
#import pandas as pd
#test_input = pd.read_csv("test_input.txt", header=None).values