# AI Underwriter - Demo
This project serves to demonstrate the possibility of partial automation of the loan approval process for a merchant cash advance (MCA). The ulitmate purpose of this project was to explore the effectiveness of various machine learning models on loan underwriting. The project shows that with a few basic machine learning models, one can generate a machine that can decide whether to approve or deny a loan request with a high level of accuracy and produce reasonable offers for approved requests. Even with a small dataset, one can build a machine that extracts patterns used by a human underwriter and use them to generate offers.

To observe the machine generate offers based on user provided data, run main.py.

Coded in python 3.7.2. 

## Model Performance
The approval prediction model uploaded here approves/denies MCA applications with an 88% accuracy. 

The payment prediction model generates a daily payment plan with 21.33% variation.

The term prediction model generates a term length between 60 to 90 business days with 11.28% variation.

## Dataset
The dataset used for this project was synthetically generated with random number generators and, therefore, no values in the dataset correspond any real life business. However, the dataset generator was designed based on an underwriter's experience to resemble real life data as closely as possible. 
