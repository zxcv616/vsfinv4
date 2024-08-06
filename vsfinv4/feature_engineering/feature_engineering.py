class FeatureEngineering:
    @staticmethod
    def add_features(data):
        data['SMA_50'] = data['Close'].rolling(window=50).mean()
        data['EMA_20'] = data['Close'].ewm(span=20, adjust=False).mean()
        data['Volatility'] = data['Close'].rolling(window=20).std()
        data['Momentum'] = data['Close'] - data['Close'].shift(10)
        return data

    @staticmethod
    def handle_missing_values(data):
        # Fill NaNs with the mean of the column
        data = data.fillna(data.mean())
        return data

#dogshit i still need to work on