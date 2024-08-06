from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split

class AdvancedMLModel:
    def __init__(self, data):
        self.data = data
        self.model = XGBClassifier()

    def train_model(self):
        X = self.data.drop(columns=['Close'])
        y = (self.data['Close'].shift(-1) > self.data['Close']).astype(int)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
        self.model.fit(X_train, y_train)
        self.accuracy = self.model.score(X_test, y_test)

    def predict(self, X):
        return self.model.predict(X)
