import yfinance as yf
import pandas as pd
import os
from datetime import datetime

def collect_data(config_path='config/us_stock.csv', data_dir='data/'):
    # Ensure data directory exists
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Read stock list
    try:
        with open(config_path, 'r') as f:
            stocks = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: {config_path} not found.")
        return

    start_date = "2025-01-01"
    end_date = datetime.now().strftime('%Y-%m-%d')

    for stock in stocks:
        print(f"Fetching data for {stock}...")
        try:
            ticker = yf.Ticker(stock)
            df = ticker.history(start=start_date, end=end_date)
            
            if df.empty:
                print(f"No data found for {stock}.")
                continue
            
            output_file = os.path.join(data_dir, f"{stock}.csv")
            df.to_csv(output_file)
            print(f"Saved {stock} data to {output_file}")
            
        except Exception as e:
            print(f"Failed to fetch data for {stock}: {e}")

if __name__ == "__main__":
    collect_data()
