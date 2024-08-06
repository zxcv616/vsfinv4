class ExternalData:
    @staticmethod
    def get_economic_indicators():
        # Placeholder for economic indicators (mock data or skip integration)
        indicators = None
        return indicators

    @staticmethod
    def merge_with_stock_data(stock_data):
        indicators = ExternalData.get_economic_indicators()
        if indicators is not None:
            merged_data = stock_data.merge(indicators, on='Date', how='left')
            return merged_data
        return stock_data  # Return the stock data as is if no indicators
