"""
TITLE  : final model compilation
AUTHOR : Salman Shah
DATE   : Mon May 27 12:23:37 2019
"""

# a function for training approval predictions
def approval_prediction_trainer(filename):
    """
    Builds a classifer that makes approval predictions
    Using a boosted random forest for classification
    Returns the fitted model
    """
    import pandas as pd
    
    # load data
    dataset = pd.read_csv(filename)
    X = dataset.iloc[:,0:-4].values
    y = dataset.iloc[:, -4].values
    
    # build and fit model
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.ensemble import AdaBoostClassifier
    classifier = AdaBoostClassifier(RandomForestClassifier(n_estimators=50,
                                                           max_depth=3), n_estimators=50)
    classifier.fit(X, y)
    
    return classifier

# a function for training paypment predictions
def payment_prediction_trainer(filename):
    """
    Builds a linear regression model that makes daily payment predictions
    Returns the fitted model
    """
    import pandas as pd
    
    # load up all the approved data points from the dataset
    dataset = pd.read_csv(filename)
    df = dataset.loc[dataset['approval'] == 1]
    
    # build up a payment column 
    offer = df['offer'].values
    rate = df['rate'].values
    term = df['term (days)'].values
    payment = pd.DataFrame(offer * rate / term, columns=['payment'], index=df.index)
    
    # Obtain some training data
    X = df.iloc[:,0:-4].values
    y = payment.values.ravel()
    
    # build and fit the model
    from sklearn.linear_model import LinearRegression
    regressor = LinearRegression()
    regressor.fit(X, y)
    
    return regressor

# a function for training term predictions
def term_prediction_trainer(filename):
    """
    Builds a random forest regression model that predicts the loan term
    Returns the fitted model
    """
    import pandas as pd
    
    # load up all the approved data points from the dataset
    dataset = pd.read_csv(filename)
    df = dataset.loc[dataset['approval'] == 1]
    
    # Define the data and target values
    X = df.iloc[:,0:-4].values
    y = df['term (days)'].values
    
    # build, fit and predict the model
    # round predictions to the nearest 5
    from sklearn.ensemble import RandomForestRegressor
    regressor = RandomForestRegressor(n_estimators=100,
                                      max_depth=None,
                                      random_state=0)
    regressor.fit(X, y)
    
    return regressor