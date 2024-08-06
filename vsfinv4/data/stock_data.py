import yfinance as yf
import pandas as pd

class StockData:
    def __init__(self, ticker):
        self.ticker = ticker
        self.data = None

    def fetch_data(self):
        self.data = yf.download(self.ticker)
        return self.data

    def preprocess_data(self):
        if self.data is not None:
            self.data['Return'] = self.data['Adj Close'].pct_change()
            self.calculate_indicators()
            self.data.fillna(method='ffill', inplace=True)  # Forward fill NaN values
            self.data.dropna(inplace=True)  # Drop remaining NaN values
            return self.data
        else:
            raise ValueError("Data not fetched. Call fetch_data() first.")

    def calculate_indicators(self):
        self.calculate_sma()
        self.calculate_ema()
        self.calculate_rsi()
        self.calculate_macd()
        self.calculate_bollinger_bands()
        self.calculate_adx()

    def calculate_sma(self, window=20):
        if self.data is not None:
            self.data[f'SMA_{window}'] = self.data['Close'].rolling(window=window).mean()
        else:
            raise ValueError("Data not fetched. Call fetch_data() first.")

    def calculate_ema(self, window=20):
        if self.data is not None:
            self.data[f'EMA_{window}'] = self.data['Close'].ewm(span=window, adjust=False).mean()
        else:
            raise ValueError("Data not fetched. Call fetch_data() first.")

    def calculate_rsi(self, window=14):
        if self.data is not None:
            delta = self.data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
            rs = gain / loss
            self.data['RSI'] = 100 - (100 / (1 + rs))
        else:
            raise ValueError("Data not fetched. Call fetch_data() first.")

    def calculate_macd(self, short_window=12, long_window=26, signal_window=9):
        if self.data is not None:
            self.data['MACD'] = self.data['Close'].ewm(span=short_window, adjust=False).mean() - self.data['Close'].ewm(span=long_window, adjust=False).mean()
            self.data['Signal Line'] = self.data['MACD'].ewm(span=signal_window, adjust=False).mean()
        else:
            raise ValueError("Data not fetched. Call fetch_data() first.")

    def calculate_bollinger_bands(self, window=20, num_std=2):
        if self.data is not None:
            self.data['BB_Middle'] = self.data['Close'].rolling(window=window).mean()
            self.data['BB_Upper'] = self.data['BB_Middle'] + num_std * self.data['Close'].rolling(window=window).std()
            self.data['BB_Lower'] = self.data['BB_Middle'] - num_std * self.data['Close'].rolling(window=window).std()
        else:
            raise ValueError("Data not fetched. Call fetch_data() first.")

    def calculate_adx(self, window=14):
        if self.data is not None:
            high = self.data['High']
            low = self.data['Low']
            close = self.data['Close']
            plus_dm = high.diff().clip(lower=0)
            minus_dm = -low.diff().clip(upper=0)
            tr = pd.concat([high - low, abs(high - close.shift()), abs(low - close.shift())], axis=1).max(axis=1)
            plus_di = 100 * (plus_dm.rolling(window=window).mean() / tr.rolling(window=window).mean())
            minus_di = 100 * (minus_dm.rolling(window=window).mean() / tr.rolling(window=window).mean())
            dx = (abs(plus_di - minus_di) / abs(plus_di + minus_di)) * 100
            self.data['ADX'] = dx.rolling(window=window).mean()
        else:
            raise ValueError("Data not fetched. Call fetch_data() first.")
