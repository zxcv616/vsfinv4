from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np

class MachineLearningModel:
    def __init__(self, data):
        self.data = data
        self.model = LogisticRegression()

    def preprocess_data(self):
        # Assuming 'Close' is the target variable and others are features
        X = self.data.drop(columns=['Close'])
        y = (self.data['Close'].shift(-1) > self.data['Close']).astype(int)  # Binary classification target

        # Fill NaNs with the mean of the column
        X = X.fillna(X.mean())
        
        return X, y

    def train_model(self):
        X, y = self.preprocess_data()
        self.model.fit(X[:-1], y[:-1])  # Train on all but the last sample

    def predict(self, X):
        # Convert to DataFrame to handle NaNs
        X_df = pd.DataFrame(X)
        # Fill NaNs with the mean of the column
        X_df = X_df.fillna(X_df.mean())
        return self.model.predict(X_df.values)
