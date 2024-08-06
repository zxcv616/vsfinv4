class Backtesting:
    def __init__(self, data):
        self.data = data

    def backtest_strategy(self, strategy_function):
        signals = []
        for index, row in self.data.iterrows():
            recommendation, _ = strategy_function()
            signal = 1 if recommendation == "Buy" else -1
            signals.append(signal)

        self.data['Signal'] = signals
        return self.data

    def calculate_performance_metrics(self, backtest_results):
        backtest_results['Return'] = backtest_results['Close'].pct_change()
        backtest_results['Strategy Return'] = backtest_results['Signal'].shift(1) * backtest_results['Return']
        cumulative_return = (1 + backtest_results['Strategy Return']).cumprod() - 1
        total_return = cumulative_return.iloc[-1]
        annual_volatility = backtest_results['Strategy Return'].std() * (252**0.5)
        return {
            'Total Return': total_return,
            'Annual Volatility': annual_volatility
        }
