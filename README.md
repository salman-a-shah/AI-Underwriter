# AI Underwriter - Demo
This project serves to demonstrate the possibility of partial automation of the loan approval process for a merchant cash advance (MCA). The ulitmate purpose of this project was to explore the effectiveness of various machine learning models on loan underwriting. The project shows that with a few basic machine learning models, one can generate a machine that can decide whether to approve or deny a loan request with a high level of accuracy and produce reasonable offers for approved requests. Even with a small dataset, one can build a machine that extracts patterns used by a human underwriter and use them to generate offers.

To observe the machine generate offers based on user provided data, run `main.py`.

Coded in python 3.7.2. 

## Model Performance
The approval prediction model uploaded here approves/denies MCA applications with an 88% accuracy. 

The payment prediction model generates a daily payment plan with 21.33% variation.

<p align="center"><img width="800" height="398" src="https://github.com/salman-a-shah/MCA-Underwriter/blob/master/figures/payment-prediction-fig.png"></p>

The term prediction model generates a term length between 60 to 90 business days with 11.28% variation.

<p align="center"><img width="800" height="398" src="https://github.com/salman-a-shah/MCA-Underwriter/blob/master/figures/term-prediction-fig.png"></p>

## Dataset
The dataset used for this project was synthetically generated with random number generators and, therefore, no values in the dataset correspond any real life business. However, the dataset generator was designed based on an underwriter's experience to resemble real life data as closely as possible. The current models were trained with a dataset containing 500 rows. The dataset has the potential to be expanded by running `data_generator.py` and labeling the randomly generated trials by hand. The new dataset can then be processed by running `data_cleaning.py` and the models can be updated by running `final_model_trainers.py` and `model_exporter.py`.

Here is an example produced by the random data generator:

<p align="center"><img width="427" height="400" src="https://github.com/salman-a-shah/MCA-Underwriter/blob/master/figures/data-generator.png"></p>

## Additional info
The full blog post on this model is available here: (TBA).
