import pandas as pd
from .machine_learning_model import MachineLearningModel

class PredictionModel:
    def __init__(self, data):
        self.data = data
        self.ml_model = MachineLearningModel(data)
        self.ml_model.train_model()
        self.weights = {
            "SMA": 1.0,
            "RSI": 1.2,
            "MACD": 1.5,
            "Bollinger Bands": 1.1,
            "ADX": 1.3,
            "Machine Learning": 2.0,
            "EMA": 1.0  # Adding weight for EMA
        }
        self.thresholds = {
            "SMA": {"middle": 0, "high": 1, "low": -1},
            "RSI": {"middle": 50, "high": 70, "low": 30},
            "MACD": {"middle": 0, "high": 1, "low": -1},
            "Bollinger Bands": {"middle": 0, "high": 1, "low": -1},
            "ADX": {"middle": 25, "high": 50, "low": 20},
            "EMA": {"middle": 0, "high": 1, "low": -1}  # Adding threshold for EMA
        }

    def calculate_weight(self, value, variable):
        threshold = self.thresholds[variable]
        if value > threshold["high"]:
            weight = 2.0  # Extreme high
        elif value > threshold["middle"]:
            weight = 1.5  # High
        elif value < threshold["low"]:
            weight = 2.0  # Extreme low
        elif value < threshold["middle"]:
            weight = 1.5  # Low
        else:
            weight = 1.0  # Middle
        return weight

    def simple_moving_average_strategy(self):
        sma_signal = self.data['Close'] > self.data['SMA_20']
        value = (self.data['Close'] - self.data['SMA_20']).iloc[-1]
        weight = self.calculate_weight(value, "SMA")
        if sma_signal.iloc[-1]:
            recommendation = 1  # Buy
        elif not sma_signal.iloc[-1] and abs(value) < self.thresholds["SMA"]["middle"]:
            recommendation = 0  # Hold
        else:
            recommendation = -1  # Sell
        reason = f"SMA Strategy: {'Buy' if recommendation == 1 else 'Sell' if recommendation == -1 else 'Hold'} based on SMA_20."
        return recommendation * weight, reason

    def rsi_strategy(self):
        rsi_signal = self.data['RSI'] < 30
        value = self.data['RSI'].iloc[-1]
        weight = self.calculate_weight(value, "RSI")
        if rsi_signal.iloc[-1]:
            recommendation = 1  # Buy
        elif not rsi_signal.iloc[-1] and abs(value - self.thresholds["RSI"]["middle"]) < 5:
            recommendation = 0  # Hold
        else:
            recommendation = -1  # Sell
        reason = f"RSI Strategy: {'Buy' if recommendation == 1 else 'Sell' if recommendation == -1 else 'Hold'} based on RSI."
        return recommendation * weight, reason

    def macd_strategy(self):
        macd_signal = self.data['MACD'] > self.data['Signal Line']
        value = (self.data['MACD'] - self.data['Signal Line']).iloc[-1]
        weight = self.calculate_weight(value, "MACD")
        if macd_signal.iloc[-1]:
            recommendation = 1  # Buy
        elif not macd_signal.iloc[-1] and abs(value) < self.thresholds["MACD"]["middle"]:
            recommendation = 0  # Hold
        else:
            recommendation = -1  # Sell
        reason = f"MACD Strategy: {'Buy' if recommendation == 1 else 'Sell' if recommendation == -1 else 'Hold'} based on MACD."
        return recommendation * weight, reason

    def bollinger_bands_strategy(self):
        bb_signal = self.data['Close'] < self.data['BB_Lower']
        value = (self.data['Close'] - self.data['BB_Lower']).iloc[-1]
        weight = self.calculate_weight(value, "Bollinger Bands")
        if bb_signal.iloc[-1]:
            recommendation = 1  # Buy
        elif not bb_signal.iloc[-1] and abs(value) < self.thresholds["Bollinger Bands"]["middle"]:
            recommendation = 0  # Hold
        else:
            recommendation = -1  # Sell
        reason = f"Bollinger Bands Strategy: {'Buy' if recommendation == 1 else 'Sell' if recommendation == -1 else 'Hold'} based on Bollinger Bands."
        return recommendation * weight, reason

    def adx_strategy(self):
        adx_signal = self.data['ADX'] > 25
        value = self.data['ADX'].iloc[-1]
        weight = self.calculate_weight(value, "ADX")
        if adx_signal.iloc[-1]:
            recommendation = 1  # Buy
        elif not adx_signal.iloc[-1] and abs(value - self.thresholds["ADX"]["middle"]) < 5:
            recommendation = 0  # Hold
        else:
            recommendation = -1  # Sell
        reason = f"ADX Strategy: {'Buy' if recommendation == 1 else 'Sell' if recommendation == -1 else 'Hold'} based on ADX."
        return recommendation * weight, reason

    def exponential_moving_average_strategy(self):
        ema_signal = self.data['Close'] > self.data['EMA_20']
        value = (self.data['Close'] - self.data['EMA_20']).iloc[-1]
        weight = self.calculate_weight(value, "EMA")
        if ema_signal.iloc[-1]:
            recommendation = 1  # Buy
        elif not ema_signal.iloc[-1] and abs(value) < self.thresholds["EMA"]["middle"]:
            recommendation = 0  # Hold
        else:
            recommendation = -1  # Sell
        reason = f"EMA Strategy: {'Buy' if ema_signal.iloc[-1] else 'Sell' if recommendation == -1 else 'Hold'} based on EMA_20."
        return recommendation * weight, reason

    def combined_strategy(self):
        sma_recommendation, sma_reason = self.simple_moving_average_strategy()
        rsi_recommendation, rsi_reason = self.rsi_strategy()
        macd_recommendation, macd_reason = self.macd_strategy()
        bb_recommendation, bb_reason = self.bollinger_bands_strategy()
        adx_recommendation, adx_reason = self.adx_strategy()
        ema_recommendation, ema_reason = self.exponential_moving_average_strategy()
        
        # Prepare the input data for the ML model
        X = self.data.drop(columns=['Close']).iloc[-1].values.reshape(1, -1)
        ml_recommendation = self.ml_model.predict(X)
        ml_recommendation = 1 if ml_recommendation == 1 else -1
        ml_recommendation *= self.weights["Machine Learning"]

        weighted_sum = (
            sma_recommendation +
            rsi_recommendation +
            macd_recommendation +
            bb_recommendation +
            adx_recommendation +
            ema_recommendation +
            ml_recommendation
        )

        final_recommendation = "Buy" if weighted_sum > 0 else "Sell" if weighted_sum < 0 else "Hold"

        reasons = {
            "SMA": sma_reason,
            "RSI": rsi_reason,
            "MACD": macd_reason,
            "Bollinger Bands": bb_reason,
            "ADX": adx_reason,
            "EMA": ema_reason,
            "Machine Learning": f"ML Model: {'Buy' if ml_recommendation > 0 else 'Sell' if ml_recommendation < 0 else 'Hold'} based on trained model."
        }

        return final_recommendation, reasons
