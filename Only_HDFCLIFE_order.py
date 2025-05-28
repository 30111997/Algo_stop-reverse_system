from fyers_apiv3 import fyersModel
import pandas as pd
import time
from datetime import datetime, time as dt_time, timedelta

# Fyers API credentials
client_id = "VCFZIJXBJX-100"
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCb05vNE9zaTNTVTIyOWctMUwxQ1hyM0d5NWtjWFpnMWVvNmxVWDdRVXpST3BqZkhjZkttTGhqblBldXNYdnVONzNva2xmQlZtQmlMdWc2eTFxeDd4V1BXTjBic2hCQlRpV2Iwd0ozUjZBY1BaRFVfZz0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiIwYTMxODdkYmUzMzc2MWIwOTVkMWZkNDZiMWViM2I4NzJjZjhmNGVkMTUyNWE1MmE5ZjJjOTgxNiIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiRkFBMzcwNjkiLCJhcHBUeXBlIjoxMDAsImV4cCI6MTc0ODQ3ODYwMCwiaWF0IjoxNzQ4NDA1Nzc0LCJpc3MiOiJhcGkuZnllcnMuaW4iLCJuYmYiOjE3NDg0MDU3NzQsInN1YiI6ImFjY2Vzc190b2tlbiJ9.u33z5TKyvVnC5t2wi-no5eI2yReecDcB0zT1C-EoNTU"

# Initialize FyersModel
fyers = fyersModel.FyersModel(
    client_id=client_id,
    token=access_token,
    is_async=False,
    log_path=""
)

# Configuration
SYMBOL = "NSE:HDFCLIFE-EQ"
TIMEFRAME = "1"  # 5 minutes
POSITION_SIZE = 10000  # ₹10,000 position size
EMA_PERIOD_FAST = 5
EMA_PERIOD_SLOW = 10
MIN_CANDLES_NEEDED = EMA_PERIOD_SLOW + 10  # Extra buffer

def get_historical_data(symbol, timeframe, days_back=1):
    """
    Fetch historical data from Fyers API with date range
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    data = {
        "symbol": symbol,
        "resolution": timeframe,
        "date_format": "1",
        "range_from": start_date.strftime('%Y-%m-%d'),
        "range_to": end_date.strftime('%Y-%m-%d'),
        "cont_flag": "1"
    }
    
    
    try:
        response = fyers.history(data=data)
        if response['code'] == 200 and len(response['candles']) >= MIN_CANDLES_NEEDED:
            df = pd.DataFrame(response['candles'])
            df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            df.set_index('timestamp', inplace=True)
            return df
        else:
            print(f"Insufficient data received: {len(response['candles'])} candles")
            return None
    except Exception as e:
        print(f"Error fetching historical data: {e}")
        return None

def calculate_ema(df):
    """
    Calculate EMA indicators
    """
    df['ema_fast'] = df['close'].ewm(span=EMA_PERIOD_FAST, adjust=False).mean()
    df['ema_slow'] = df['close'].ewm(span=EMA_PERIOD_SLOW, adjust=False).mean()
    return df

def check_crossover(df):
    """
    Check for EMA crossover
    Returns: 1 for buy (fast EMA crosses above slow EMA), 
             -1 for sell (fast EMA crosses below slow EMA),
             0 for no signal
    """
    if len(df) < 2:
        return 0
    
    prev_fast = df['ema_fast'].iloc[-2]
    prev_slow = df['ema_slow'].iloc[-2]
    curr_fast = df['ema_fast'].iloc[-1]
    curr_slow = df['ema_slow'].iloc[-1]
    
    # Buy signal: fast EMA crosses above slow EMA
    if prev_fast <= prev_slow and curr_fast > curr_slow:
        return 1
    # Sell signal: fast EMA crosses below slow EMA
    elif prev_fast >= prev_slow and curr_fast < curr_slow:
        return -1
    else:
        return 0

def get_current_price(symbol):
    """
    Get current market price
    """
    data = {"symbols": symbol}
    try:
        response = fyers.quotes(data=data)
        if response['code'] == 200:
            return response['d'][0]['v']['lp']
    except Exception as e:
        print(f"Error getting current price: {e}")
        return None

def calculate_quantity(position_size, price):
    """
    Calculate quantity based on position size
    """
    return max(1, int(position_size / price))  # Ensure at least 1 quantity

def place_order(signal, symbol, price):
    """
    Place buy/sell order based on signal
    """
    qty = calculate_quantity(POSITION_SIZE, price)
    
    data = {
        "symbol": symbol,
        "qty": qty,
        "type": 2,  # 2 = limit order, 1 = market order
        "side": 1 if signal == 1 else -1,  # 1 = buy, -1 = sell
        "productType": "INTRADAY",
        "limitPrice": price,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": False,
        "orderTag": "EMA_CROSS"
    }
    
    try:
        response = fyers.place_order(data=data)
        return response
    except Exception as e:
        print(f"Error placing order: {e}")
        return None

def is_market_open():
    """
    Check if Indian stock market is open (9:15 AM to 3:30 PM)
    """
    now = datetime.now().time()
    market_open = dt_time(9, 15)
    market_close = dt_time(15, 30)
    return market_open <= now <= market_close

def main():
    print("Starting EMA Crossover Trading System")
    
    while True:
        if not is_market_open():
            print("Market is closed. Waiting...")
            time.sleep(300)  # Check every 5 minutes
            continue
        
        # Get historical data with 1 day lookback
        df = get_historical_data(SYMBOL, TIMEFRAME, days_back=1)
        
        if df is None:
            print("Failed to get historical data. Retrying...") 
            time.sleep(60)


            continue
        
        # Calculate indicators
        df = calculate_ema(df)
        
        # Check for crossover signal
        signal = check_crossover(df)
        
        if signal != 0:
            current_price = get_current_price(SYMBOL)
            if current_price:
                action = "BUY" if signal == 1 else "SELL"
                print(f"{action} signal detected at price: {current_price}")
                
                # Place order
                order_response = place_order(signal, SYMBOL, current_price)
                if order_response and order_response.get('code') == 200:
                    print(f"Order placed successfully: {order_response}")
                    # Wait for some time after placing order to avoid duplicate orders
                    time.sleep(300)
                else:
                    print("Failed to place order")
            else:
                print("Couldn't get current price")
        
        # Wait for next candle (1 minutes)
        time.sleep(300)

if __name__ == "__main__":
    main()