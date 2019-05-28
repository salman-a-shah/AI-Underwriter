"""
TITLE  : 
AUTHOR : Salman Shah
DATE   : Mon May 27 14:15:26 2019

This script trains and exports the final models as joblib packages
"""
from final_model_trainers import *
from sklearn.externals import joblib

FILENAME = 'data\dataset_cleaned.csv'

approval_model = approval_prediction_trainer(FILENAME)
payment_model = payment_prediction_trainer(FILENAME)
term_model = term_prediction_trainer(FILENAME)

joblib.dump(approval_model, r'saved_models\approval_model.sav')
joblib.dump(payment_model, r'saved_models\payment_model.sav')
joblib.dump(term_model, r'saved_models\term_model.sav')