"""
TITLE  : Payment prediction
AUTHOR : Salman Shah
DATE   : Sat May 25 18:29:18 2019

Given that a file has been approved, this machine generates the daily payment
associated with the offer
"""
import pandas as pd

# load up all the approved data points from the dataset
dataset = pd.read_csv("data\dataset_cleaned.csv")
df = dataset.loc[dataset['approval'] == 1]

# build up a payment column 
offer = df['offer'].values
rate = df['rate'].values
term = df['term (days)'].values
payment = pd.DataFrame(offer * rate / term, columns=['payment'], index=df.index)

# Obtain some training data
X = df.iloc[:,0:-4].values
y = payment.values.ravel()

# splitting into training and test sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

## feature scaling
#from sklearn.preprocessing import StandardScaler
#sc = StandardScaler()
#X_train = sc.fit_transform(X_train)
#X_test = sc.transform(X_test)

from sklearn.preprocessing import RobustScaler
rbc = RobustScaler()
X_train = rbc.fit_transform(X_train)
X_test = rbc.transform(X_test)

# build, fit and predict the model
#from sklearn.ensemble import RandomForestRegressor
#from sklearn.svm import LinearSVR
from sklearn.linear_model import LinearRegression
#regressor = RandomForestRegressor(n_estimators=100,
#                                  max_depth=None,
#                                  random_state=0)
#regressor = LinearSVR(epsilon=0.1)
regressor = LinearRegression()
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)
y_train_pred = regressor.predict(X_train)

## reshaping y vectors 
#y_test = y_test.reshape((y_test.shape[0],))
#y_train = y_train.reshape((y_train.shape[0],))
#y_pred = y_pred.reshape((y_pred.shape[0],))
#y_train_pred = y_train_pred.reshape((y_train_pred.shape[0],))

# error values
error = abs(y_test - y_pred)
error_percentage = sum(error)/sum(y_test) * 100
error_train = abs(y_train - y_train_pred)
error_percentage_train = sum(error_train)/sum(y_train) * 100

''' plotting '''
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({'font.size': 9})
fig = plt.figure(figsize=(8,4))
fig.suptitle("Daily Payment Prediction Performance", fontsize=12, fontweight='bold')

ax = plt.subplot(122)

# plotting test performance
sorted_y = pd.DataFrame({
           'y_test' : y_test.tolist(),
           'y_pred' : y_pred.tolist()
           }, index=None)
sorted_y = sorted_y.sort_values(by=['y_pred'])

ax.scatter(range(y_test.shape[0]), sorted_y['y_test'].values, marker='x')
ax.plot(sorted_y['y_pred'].values, color='red')
plt.xlabel('Loans')
plt.xticks([])
ax.grid(axis='y')
plt.ylim(0, 600)
ax.text(x=0, y=-50, s="Error: %.2f" % error_percentage + "%")
#ax.legend(['Prediction', 'Datapoint'])
plt.title('test data', fontsize=9)

# plotting training performance
sorted_y_train = pd.DataFrame({
        'y_train' : y_train.tolist(),
        'y_train_pred' : y_train_pred.tolist()
        }, index=None)
sorted_y_train = sorted_y_train.sort_values(by=['y_train_pred'])

ax2 = plt.subplot(121)
ax2.scatter(range(y_train.shape[0]), sorted_y_train['y_train'].values, marker='x')
ax2.plot(sorted_y_train['y_train_pred'].values, color='red')
plt.xlabel('Loans')
plt.ylabel('Daily payment offer ($/day)')
plt.xticks([])
ax2.grid(axis='y')
plt.ylim(0, 600)
ax2.text(x=0, y=-50, s="Error: %.2f" % error_percentage_train + "%")
ax2.legend(['Prediction', 'Datapoint'])
plt.title('training data', fontsize=9)
plt.show()