from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class EnsembleModel:
    def __init__(self, data):
        self.data = data
        self.models = {
            'RandomForest': RandomForestClassifier(n_estimators=100),
            'GradientBoosting': GradientBoostingClassifier(n_estimators=100)
        }
        self.X_train, self.X_test, self.y_train, self.y_test = self.prepare_data()

    def prepare_data(self):
        X = self.data.drop(columns=['Close'])
        y = (self.data['Close'].shift(-1) > self.data['Close']).astype(int)  # 1 if next day is up, else 0
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
        return X_train, X_test, y_train, y_test

    def train_models(self):
        for name, model in self.models.items():
            model.fit(self.X_train, self.y_train)

    def evaluate_models(self):
        results = {}
        for name, model in self.models.items():
            y_pred = model.predict(self.X_test)
            accuracy = accuracy_score(self.y_test, y_pred)
            results[name] = accuracy
        return results

    def predict(self, X):
        predictions = {}
        for name, model in self.models.items():
            predictions[name] = model.predict(X)
        return predictions
