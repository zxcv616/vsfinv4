import customtkinter as ctk
from tkinter import messagebox
from data.stock_data import StockData
from models.prediction_model import PredictionModel
from models.backtesting import Backtesting
from gui.stock_comparison import StockComparison

class StockApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.root = ctk.CTk()
        self.root.title("Stock Analysis App")
        self.root.geometry("900x700")
        self.root.resizable(False, False)  # Make the size fixed

        self.create_widgets()

    def create_widgets(self):
        print("Creating main widgets")

        # Create main frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Configure the grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        # Create sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self.main_frame, width=200)
        self.sidebar_frame.grid(row=0, column=0, sticky="ns")
        
        # Create buttons in the sidebar
        self.analysis_button = ctk.CTkButton(self.sidebar_frame, text="Stock Analysis", command=lambda: self.show_frame(self.analysis_frame))
        self.analysis_button.grid(row=0, column=0, pady=10, padx=10)
        
        self.backtesting_button = ctk.CTkButton(self.sidebar_frame, text="Backtesting", command=lambda: self.show_frame(self.backtesting_frame))
        self.backtesting_button.grid(row=1, column=0, pady=10, padx=10)
        
        self.comparison_button = ctk.CTkButton(self.sidebar_frame, text="Stock Comparison", command=lambda: self.show_frame(self.comparison_frame))
        self.comparison_button.grid(row=2, column=0, pady=10, padx=10)
        
        self.portfolio_button = ctk.CTkButton(self.sidebar_frame, text="Portfolio", command=lambda: self.show_frame(self.portfolio_frame))
        self.portfolio_button.grid(row=3, column=0, pady=10, padx=10)

        # Create content frames
        self.analysis_frame = ctk.CTkFrame(self.main_frame)
        self.backtesting_frame = ctk.CTkFrame(self.main_frame)
        self.comparison_frame = ctk.CTkFrame(self.main_frame)
        self.portfolio_frame = ctk.CTkFrame(self.main_frame)

        # Place content frames
        for frame in (self.analysis_frame, self.backtesting_frame, self.comparison_frame, self.portfolio_frame):
            frame.grid(row=0, column=1, sticky="nsew")

        # Show the analysis frame by default
        self.show_frame(self.analysis_frame)

        # Create widgets for each frame
        self.create_analysis_widgets()
        self.create_backtesting_widgets()
        self.create_comparison_widgets()
        self.create_portfolio_widgets()

        # Status bar
        self.status_bar = ctk.CTkLabel(self.root, text="Welcome to Stock Analysis App", anchor="w")
        self.status_bar.grid(row=1, column=0, sticky="ew")

    def show_frame(self, frame):
        frame.tkraise()

    def create_analysis_widgets(self):
        print("Creating analysis widgets")
        # Stock ticker input
        ticker_frame = ctk.CTkFrame(self.analysis_frame)
        ticker_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5)
        self.ticker_label = ctk.CTkLabel(ticker_frame, text="Enter Stock Ticker:")
        self.ticker_label.grid(row=0, column=0, sticky="w", padx=5)
        self.ticker_entry = ctk.CTkEntry(ticker_frame, width=200)
        self.ticker_entry.grid(row=0, column=1, sticky="ew", padx=5)

        # Analyze button
        self.analyze_button = ctk.CTkButton(self.analysis_frame, text="Analyze", command=self.analyze_stock)
        self.analyze_button.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")

        # Result and reason display
        result_frame = ctk.CTkFrame(self.analysis_frame)
        result_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)
        self.result_label = ctk.CTkLabel(result_frame, text="", font=("Helvetica", 12, "bold"))
        self.result_label.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5)

        self.reason_label_sma = ctk.CTkLabel(result_frame, text="", wraplength=300)
        self.reason_label_sma.grid(row=1, column=0, sticky="ew", padx=5, pady=2)

        self.reason_label_rsi = ctk.CTkLabel(result_frame, text="", wraplength=300)
        self.reason_label_rsi.grid(row=2, column=0, sticky="ew", padx=5, pady=2)

        self.reason_label_macd = ctk.CTkLabel(result_frame, text="", wraplength=300)
        self.reason_label_macd.grid(row=3, column=0, sticky="ew", padx=5, pady=2)

        self.reason_label_bb = ctk.CTkLabel(result_frame, text="", wraplength=300)
        self.reason_label_bb.grid(row=4, column=0, sticky="ew", padx=5, pady=2)

        self.reason_label_adx = ctk.CTkLabel(result_frame, text="", wraplength=300)
        self.reason_label_adx.grid(row=5, column=0, sticky="ew", padx=5, pady=2)

        self.reason_label_ema = ctk.CTkLabel(result_frame, text="", wraplength=300)
        self.reason_label_ema.grid(row=6, column=0, sticky="ew", padx=5, pady=2)

        self.reason_label_ml = ctk.CTkLabel(result_frame, text="", wraplength=300)
        self.reason_label_ml.grid(row=7, column=0, sticky="ew", padx=5, pady=2)

    def create_backtesting_widgets(self):
        print("Creating backtesting widgets")
        # Backtesting explanation
        explanation_label = ctk.CTkLabel(self.backtesting_frame, text="Backtest your strategies with historical data.", font=("Helvetica", 12))
        explanation_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        # Stock ticker input for backtesting
        ticker_frame = ctk.CTkFrame(self.backtesting_frame)
        ticker_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)
        self.ticker_label_bt = ctk.CTkLabel(ticker_frame, text="Enter Stock Ticker for Backtesting:")
        self.ticker_label_bt.grid(row=0, column=0, sticky="w", padx=5)
        self.ticker_entry_bt = ctk.CTkEntry(ticker_frame, width=200)
        self.ticker_entry_bt.grid(row=0, column=1, sticky="ew", padx=5)

        # Start backtesting button
        self.backtest_button = ctk.CTkButton(self.backtesting_frame, text="Start Backtesting", command=self.start_backtesting)
        self.backtest_button.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        # Backtesting results display
        self.backtest_results_text = ctk.CTkTextbox(self.backtesting_frame, wrap="word", width=70, height=20)
        self.backtest_results_text.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

    def create_comparison_widgets(self):
        print("Creating comparison widgets")
        self.comparison = StockComparison(self.comparison_frame)

    def create_portfolio_widgets(self):
        print("Creating portfolio widgets")
        # Portfolio input fields
        self.portfolio_label = ctk.CTkLabel(self.portfolio_frame, text="Enter Stock Tickers (comma separated):")
        self.portfolio_label.grid(row=0, column=0, padx=5, pady=5)
        self.portfolio_entry = ctk.CTkEntry(self.portfolio_frame, width=400)
        self.portfolio_entry.grid(row=0, column=1, padx=5, pady=5)

        self.analyze_portfolio_button = ctk.CTkButton(self.portfolio_frame, text="Analyze Portfolio", command=self.analyze_portfolio)
        self.analyze_portfolio_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Portfolio result display
        self.portfolio_results_text = ctk.CTkTextbox(self.portfolio_frame, wrap="word", width=80, height=20)
        self.portfolio_results_text.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        # Adjust the row and column weights to make the textbox expand
        self.portfolio_frame.columnconfigure(0, weight=1)
        self.portfolio_frame.rowconfigure(2, weight=1)

    def analyze_stock(self):
        ticker = self.ticker_entry.get()
        self.update_status(f"Fetching data for {ticker}...")
        try:
            stock_data = StockData(ticker)
            stock_data.fetch_data()
            data = stock_data.preprocess_data()
            stock_data.calculate_indicators()

            prediction_model = PredictionModel(data)
            final_recommendation, reasons = prediction_model.combined_strategy()

            self.result_label.configure(text=f"Final Recommendation: {final_recommendation}")
            self.reason_label_sma.configure(text=f"SMA: {reasons['SMA']}")
            self.reason_label_rsi.configure(text=f"RSI: {reasons['RSI']}")
            self.reason_label_macd.configure(text=f"MACD: {reasons['MACD']}")
            self.reason_label_bb.configure(text=f"Bollinger Bands: {reasons['Bollinger Bands']}")
            self.reason_label_adx.configure(text=f"ADX: {reasons['ADX']}")
            self.reason_label_ema.configure(text=f"EMA: {reasons['EMA']}")
            self.reason_label_ml.configure(text=f"Machine Learning: {reasons['Machine Learning']}")

            self.update_status("Analysis complete.")
        except Exception as e:
            self.update_status(f"Error: {e}")
            messagebox.showerror("Error", str(e))

    def analyze_portfolio(self):
        tickers = self.portfolio_entry.get().split(',')
        results = ""
        for ticker in tickers:
            ticker = ticker.strip()
            self.update_status(f"Fetching data for {ticker}...")
            try:
                stock_data = StockData(ticker)
                stock_data.fetch_data()
                data = stock_data.preprocess_data()
                stock_data.calculate_indicators()

                prediction_model = PredictionModel(data)
                final_recommendation, reasons = prediction_model.combined_strategy()

                results += f"Ticker: {ticker}\n"
                results += f"Final Recommendation: {final_recommendation}\n"
                results += f"SMA: {reasons['SMA']}\n"
                results += f"RSI: {reasons['RSI']}\n"
                results += f"MACD: {reasons['MACD']}\n"
                results += f"Bollinger Bands: {reasons['Bollinger Bands']}\n"
                results += f"ADX: {reasons['ADX']}\n"
                results += f"EMA: {reasons['EMA']}\n"
                results += f"Machine Learning: {reasons['Machine Learning']}\n"
                results += "------------------------------------\n"

            except Exception as e:
                results += f"Error fetching data for {ticker}: {e}\n"
                messagebox.showerror("Error", str(e))

        self.portfolio_results_text.delete("1.0", "end")
        self.portfolio_results_text.insert("1.0", results)

    def start_backtesting(self):
        ticker = self.ticker_entry_bt.get()
        self.update_status(f"Starting backtesting for {ticker}...")
        try:
            stock_data = StockData(ticker)
            stock_data.fetch_data()
            data = stock_data.preprocess_data()
            stock_data.calculate_indicators()

            backtesting = Backtesting(data)
            backtest_results = backtesting.backtest_strategy(PredictionModel(data).combined_strategy)
            performance_metrics = backtesting.calculate_performance_metrics(backtest_results)

            # Display backtest results
            self.backtest_results_text.delete("1.0", "end")
            self.backtest_results_text.insert("1.0", f"Backtest Results:\n{backtest_results}\n")
            self.backtest_results_text.insert("1.0", f"\nPerformance Metrics:\n{performance_metrics}\n")

            self.update_status("Backtesting complete.")
        except Exception as e:
            self.update_status(f"Error: {e}")
            messagebox.showerror("Error", str(e))

    def update_status(self, message):
        self.status_bar.configure(text=message)

    def run(self):
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    app = StockApp()
    app.run()
