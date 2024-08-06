import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  # Add this import
from data.stock_data import StockData
import pandas as pd

class StockComparison:
    def __init__(self, parent):
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        # Frame for stock comparison
        self.frame = ttk.Frame(self.parent, style="TFrame")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Stock ticker inputs
        self.ticker1_label = ttk.Label(self.frame, text="Stock Ticker 1:", style="TLabel")
        self.ticker1_label.grid(row=0, column=0, padx=5, pady=5)
        self.ticker1_entry = ttk.Entry(self.frame, width=20)
        self.ticker1_entry.grid(row=0, column=1, padx=5, pady=5)

        self.ticker2_label = ttk.Label(self.frame, text="Stock Ticker 2:", style="TLabel")
        self.ticker2_label.grid(row=1, column=0, padx=5, pady=5)
        self.ticker2_entry = ttk.Entry(self.frame, width=20)
        self.ticker2_entry.grid(row=1, column=1, padx=5, pady=5)

        self.compare_button = ttk.Button(self.frame, text="Compare", command=self.compare_stocks, style="TButton")
        self.compare_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Comparison result display
        self.result_frame = ttk.Frame(self.frame, style="TFrame")
        self.result_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        self.result_text = tk.Text(self.result_frame, wrap=tk.WORD, width=70, height=20, bg="#333333", fg="#e0e0e0")
        self.result_text.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky=(tk.W, tk.E))

    def compare_stocks(self):
        ticker1 = self.ticker1_entry.get()
        ticker2 = self.ticker2_entry.get()

        if ticker1 and ticker2:
            stock_data1 = StockData(ticker1)
            stock_data2 = StockData(ticker2)

            stock_data1.fetch_data()
            stock_data2.fetch_data()

            data1 = stock_data1.data
            data2 = stock_data2.data

            comparison = pd.DataFrame({
                'Metric': ['Close Price', 'Volume', 'Market Cap'],
                f'{ticker1}': [data1['Close'].iloc[-1], data1['Volume'].iloc[-1], data1['Close'].iloc[-1] * stock_data1.data['Volume'].iloc[-1]],
                f'{ticker2}': [data2['Close'].iloc[-1], data2['Volume'].iloc[-1], data2['Close'].iloc[-1] * stock_data2.data['Volume'].iloc[-1]]
            })

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Stock Comparison:\n{comparison}\n")
        else:
            messagebox.showerror("Input Error", "Please enter both stock tickers")

if __name__ == "__main__":
    root = tk.Tk()
    app = StockComparison(root)
    root.mainloop()
