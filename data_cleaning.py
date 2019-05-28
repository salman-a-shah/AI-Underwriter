"""
TITLE  : Dataset Cleaning
AUTHOR : Salman Shah
DATE   : Wed May 15 18:32:57 2019
"""

# this script cleans the raw_dataset file and prepares it for training
import pandas as pd

# load up the raw dataset
df = pd.read_csv("data\dataset_raw.csv")

# replace the NaNs with 0s
df = df.fillna(0)

# This portion takes the strings from the individual lender withdrawals column
# (which represent payments to current lenders) and puts them into 
# their own column
templist = df.loc[:,'individual lender withdrawals'].tolist()
templist = [str(s).replace(";"," ") for s in templist]
templist = [s.split() for s in templist]

new_list = []
for l in templist: 
  while (len(l) < 7): # since there's a max of 7 lenders in the dataset
    l.append('0')
  new_list.append(l)
templist = new_list

new_list = []
for l in templist:
  new_list.append([float(s) for s in l])
templist = new_list

labels = ['lender 1', 'lender 2', 'lender 3', 'lender 4', 'lender 5',
         'lender 6', 'lender 7']
df2 = pd.DataFrame.from_records(templist, columns=labels)
df = pd.concat([df.iloc[:,0:14], df2, df.iloc[:,15:]], axis=1, sort=False)

# changing approval and denial to binary numberical values
templist = df.loc[:, 'approval'].tolist()
templist = [(0 if s == 'Denied' else 1) for s in templist]
df['approval'] = pd.DataFrame(templist, columns=['approval'])

# changing past default column to binary nemerical values
templist = df.loc[:, 'past default'].tolist()
templist = [(0 if b == False else 1) for b in templist]
df['past default'] = pd.DataFrame(templist, columns=['past default'])

# applying one hot encoding to business type
business_type_df = pd.get_dummies(df.iloc[:,0],drop_first=True)
df = pd.concat([business_type_df, df.iloc[:,1:]], axis=1, sort=False)

# the dataframe is now ready to be used for training
# Save the dataframe into a new csv file

df.to_csv('data\dataset_cleaned.csv', index=False)