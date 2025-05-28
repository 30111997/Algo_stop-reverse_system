import time
import datetime
import fyers_api
from fyers_api import fyersModel
from fyers_api import accessToken


# Fyers API credentials
client_id = "VCFZIJXBJX-100"
secret_key = "8CDU7QIBKY"
redirect_uri = "https://www.google.com/"  # Same as registered in Fyers
response_type = "code"
grant_type = "authorization_code"


# Initialize Fyers model
session = accessToken.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri,
    response_type=response_type
)

# Generate auth code URL (run this once to get auth code)
auth_url = session.generate_authcode()
print("Login to this URL and get auth code:", auth_url)

# After getting auth code, use it to get access token
auth_code = "YOUR_AUTH_CODE"
session.set_token(auth_code)
response = session.generate_token()
access_token = response["access_token"]

# Create Fyers model with access token
fyers = fyersModel.FyersModel(
    client_id=client_id,
    token=access_token,
    log_path="/logs"
)

# Trading parameters
symbols = ["NSE:UNIONBANK-EQ", "NSE:HDFCLIFE-EQ"]
capital_per_trade = 10000  # ₹10,000 per trade
ema_period_short = 5
ema_period_long = 10

# Dictionary to track positions
positions = {
    "NSE:UNIONBANK-EQ": {
        "position": None,  # "long", "short", or None
        "entry_price": 0,
        "stop_loss": 0,
        "target": 0
    },
    "NSE:HDFCLIFE-EQ": {
        "position": None,
        "entry_price": 0,
        "stop_loss": 0,
        "target": 0
    }
}

def calculate_ema(data, period):
    """Calculate EMA for given period"""
    if len(data) < period:
        return None
    
    multiplier = 2 / (period + 1)
    ema = data[0]['close']
    
    for i in range(1, len(data)):
        ema = (data[i]['close'] - ema) * multiplier + ema
    
    return ema

def get_historical_data(symbol, timeframe, count):
    """Get historical data from Fyers"""
    data = {
        "symbol": symbol,
        "resolution": timeframe,
        "date_format": "1",
        "range_from": "",
        "range_to": "",
        "cont_flag": "1"
    }
    
    response = fyers.history(data=data)
    
    if response['code'] == 200:
        return response['candles']
    else:
        print(f"Error fetching data for {symbol}: {response['message']}")
        return None

def place_order(symbol, side, quantity):
    """Place order through Fyers"""
    order_data = {
        "symbol": symbol,
        "qty": quantity,
        "type": 2,  # Intraday order
        "side": 1 if side == "buy" else -1,
        "productType": "INTRADAY",
        "limitPrice": 0,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": "False",
        "stopLoss": 0,
        "takeProfit": 0
    }
    
    response = fyers.place_order(data=order_data)
    
    if response['code'] == 200:
        print(f"Order placed: {side} {quantity} {symbol}")
        return True
    else:
        print(f"Order failed: {response['message']}")
        return False

def calculate_quantity(symbol, price):
    """Calculate quantity based on capital per trade"""
    # Get current market price if not provided
    if price == 0:
        ltp_data = fyers.quotes({"symbols": symbol})
        price = ltp_data['d'][0]['v']['lp']
    
    quantity = int(capital_per_trade / price)
    return max(1, quantity)  # Ensure at least 1 share

def check_and_execute_trades():
    """Main trading logic"""
    for symbol in symbols:
        # Get historical data (5-minute candles)
        data = get_historical_data(symbol, "5", 20)  # Get last 20 candles
        
        if not data or len(data) < ema_period_long:
            continue
        
        # Calculate EMAs
        ema_short = calculate_ema(data[-ema_period_short:], ema_period_short)
        ema_long = calculate_ema(data[-ema_period_long:], ema_period_long)
        
        if ema_short is None or ema_long is None:
            continue
        
        current_position = positions[symbol]["position"]
        current_price = data[-1]['close']
        
        # Check for crossover signals
        if ema_short > ema_long and current_position != "long":
            # Golden cross - buy signal
            if current_position == "short":
                # Close short position first (Stop and Reverse)
                quantity = calculate_quantity(symbol, positions[symbol]["entry_price"])
                place_order(symbol, "buy", quantity)
            
            # Open long position
            quantity = calculate_quantity(symbol, current_price)
            if place_order(symbol, "buy", quantity):
                positions[symbol]["position"] = "long"
                positions[symbol]["entry_price"] = current_price
                # Set stop loss and target (adjust as per your risk management)
                positions[symbol]["stop_loss"] = current_price * 0.995  # 0.5% SL
                positions[symbol]["target"] = current_price * 1.01  # 1% target
        
        elif ema_short < ema_long and current_position != "short":
            # Death cross - sell signal
            if current_position == "long":
                # Close long position first (Stop and Reverse)
                quantity = calculate_quantity(symbol, positions[symbol]["entry_price"])
                place_order(symbol, "sell", quantity)
            
            # Open short position
            quantity = calculate_quantity(symbol, current_price)
            if place_order(symbol, "sell", quantity):
                positions[symbol]["position"] = "short"
                positions[symbol]["entry_price"] = current_price
                # Set stop loss and target (adjust as per your risk management)
                positions[symbol]["stop_loss"] = current_price * 1.005  # 0.5% SL for short
                positions[symbol]["target"] = current_price * 0.99  # 1% target for short
        
        # Check for stop loss or target hits
        if current_position == "long":
            if current_price <= positions[symbol]["stop_loss"] or current_price >= positions[symbol]["target"]:
                quantity = calculate_quantity(symbol, positions[symbol]["entry_price"])
                place_order(symbol, "sell", quantity)
                positions[symbol]["position"] = None
        
        elif current_position == "short":
            if current_price >= positions[symbol]["stop_loss"] or current_price <= positions[symbol]["target"]:
                quantity = calculate_quantity(symbol, positions[symbol]["entry_price"])
                place_order(symbol, "buy", quantity)
                positions[symbol]["position"] = None

def main():
    """Main loop"""
    print("Starting algo trading bot...")
    
    while True:
        now = datetime.datetime.now()
        
        # Run only during market hours (9:15 AM to 3:30 PM IST)
        if now.time() >= datetime.time(9, 15) and now.time() <= datetime.time(15, 30):
            # Check trades at the start of each 5-minute candle
            if now.minute % 5 == 0 and now.second == 0:
                check_and_execute_trades()
                time.sleep(1)  # Prevent multiple executions in the same minute
        
        time.sleep(1)  # Check every second

if __name__ == "__main__":
    main()