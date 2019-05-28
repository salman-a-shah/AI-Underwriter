"""
TITLE  : Approval machine
AUTHOR : Salman Shah
DATE   : Sat May 25 16:36:05 2019

This script builds a model that learns to approve or deny different files
"""

import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_csv("data\dataset_cleaned.csv")
X = dataset.iloc[:,0:-4].values
y = dataset.iloc[:, -4].values

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

#from sklearn.preprocessing import StandardScaler
# doesn't seem to make a difference
#sc = StandardScaler()
#X_train = sc.fit_transform(X_train)
#X_test = sc.transform(X_test)

from sklearn.preprocessing import RobustScaler
rbc = RobustScaler()
X_train = rbc.fit_transform(X_train)
X_test = rbc.transform(X_test)

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
classifier = AdaBoostClassifier(RandomForestClassifier(n_estimators=50,
                                                       max_depth=3), n_estimators=50)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
accuracy = sum([cm[i][i] for i in range(cm.shape[0])])/(sum(sum(cm)))

# plotting the confusion matrix
plt.figure(figsize=(5,4))
import seaborn as sn
df_cm = pd.DataFrame(cm, 
                     columns=['Predicted Approved', 'Predicted Denied'], 
                     index=['Approved', 'Denied'])
sn.heatmap(df_cm, annot=True)
plt.title("Confusion Matrix on Test Set")
plt.show()