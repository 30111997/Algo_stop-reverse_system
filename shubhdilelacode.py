import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# 1. Load data
data = yf.download('AAPL', start='2023-01-01', end='2024-01-01', threads=False)


# 2. Calculate EMAs
data['EMA50'] = data['Close'].ewm(span=50, adjust=False).mean()
data['EMA200'] = data['Close'].ewm(span=200, adjust=False).mean()

# 3. Plot
plt.plot(data['Close'], label='Price')
plt.plot(data['EMA50'], label='EMA50')
plt.plot(data['EMA200'], label='EMA200')
plt.legend()
plt.show()

# Create Buy and Sell signals
data['Buy_Signal'] = (data['EMA50'] > data['EMA200']) & (data['EMA50'].shift(1) <= data['EMA200'].shift(1))
data['Sell_Signal'] = (data['EMA50'] < data['EMA200']) & (data['EMA50'].shift(1) >= data['EMA200'].shift(1))

# Plot with signals
plt.figure(figsize=(14,7))
plt.plot(data['Close'], label='Price')
plt.plot(data['EMA50'], label='EMA50')
plt.plot(data['EMA200'], label='EMA200')

# Add Buy markers
plt.scatter(data.index[data['Buy_Signal']], data['Close'][data['Buy_Signal']], marker='^', color='g', label='Buy', s=100)

# Add Sell markers
plt.scatter(data.index[data['Sell_Signal']], data['Close'][data['Sell_Signal']], marker='v', color='r', label='Sell', s=100)

plt.legend()
plt.show()

import requests

# Example to place order (dummy payload)
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzQ2NjkyMDc1LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMjM2MzU4NyJ9.u_aRBAiIJKLn8qDLj_x3Ifa8lzOl-zVuGRbJVNIgujDa5L9o8r_n2fgw8UMywOuNjRTjqS2eUdxfA8kUwAYaEg"

url = "https://api.dhan.co/orders"  # This is just an example endpoint

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

order_payload = {
    "security_id": "XYZ",         # your stock symbol
    "transaction_type": "BUY",    # or "SELL"
    "order_type": "MARKET",        # or "LIMIT"
    "quantity": 1,
    "product_type": "INTRADAY",    # or "DELIVERY"
}

response = requests.post(url, json=order_payload, headers=headers)

print(response.json())