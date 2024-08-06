from sklearn.linear_model import Lasso, Ridge

class Regularization:
    def __init__(self, data):
        self.data = data
        self.lasso_model = Lasso(alpha=0.1)
        self.ridge_model = Ridge(alpha=0.1)

    def train_lasso(self, X, y):
        self.lasso_model.fit(X, y)

    def train_ridge(self, X, y):
        self.ridge_model.fit(X, y)
