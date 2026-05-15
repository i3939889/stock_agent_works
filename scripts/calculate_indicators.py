import pandas as pd
import os
import glob

def calculate_indicators(data_dir='data/', output_dir='data/processed/'):
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # Find all CSV files in the data directory
    csv_files = glob.glob(os.path.join(data_dir, '*.csv'))
    
    if not csv_files:
        print(f"No CSV files found in {data_dir}")
        return

    for file_path in csv_files:
        file_name = os.path.basename(file_path)
        print(f"Processing {file_name}...")
        
        # Load data
        df = pd.read_csv(file_path)
        
        # Ensure 'Date' is datetime and sort
        df['Date'] = pd.to_datetime(df['Date'], utc=True)
        df = df.sort_values('Date')
        
        # 1. Moving Averages
        df['MA10'] = df['Close'].rolling(window=10).mean()
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['MA55'] = df['Close'].rolling(window=55).mean()
        
        # 2. MACD (12, 26, 9)
        ema12 = df['Close'].ewm(span=12, adjust=False).mean()
        ema26 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = ema12 - ema26
        df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']
        
        # 3. ATR (14) using SMA
        # True Range calculation
        df['prev_close'] = df['Close'].shift(1)
        df['tr1'] = df['High'] - df['Low']
        df['tr2'] = abs(df['High'] - df['prev_close'])
        df['tr3'] = abs(df['Low'] - df['prev_close'])
        df['TR'] = df[['tr1', 'tr2', 'tr3']].max(axis=1)
        
        # ATR using SMA as requested
        df['ATR'] = df['TR'].rolling(window=14).mean()
        
        # Cleanup temporary columns
        df.drop(columns=['prev_close', 'tr1', 'tr2', 'tr3', 'TR'], inplace=True)
        
        # Save to processed directory
        output_path = os.path.join(output_dir, file_name)
        df.to_csv(output_path, index=False)
        print(f"Saved processed data to {output_path}")

if __name__ == "__main__":
    calculate_indicators()
