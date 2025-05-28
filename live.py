from fyers_apiv3.FyersWebsocket import data_ws


def onmessage(message):
    """
    Callback function to handle incoming messages from the FyersDataSocket WebSocket.

    Parameters:
        message (dict): The received message from the WebSocket.

    """
    print("Response:", message)


def onerror(message):
    """
    Callback function to handle WebSocket errors.

    Parameters:
        message (dict): The error message received from the WebSocket.


    """
    print("Error:", message)


def onclose(message):
    """
    Callback function to handle WebSocket connection close events.
    """
    print("Connection closed:", message)


def onopen():
    """
    Callback function to subscribe to data type and symbols upon WebSocket connection.

    """
    # Specify the data type and symbols you want to subscribe to
    data_type = "SymbolUpdate"

    # Subscribe to the specified symbols and data type
    symbols = ['NSE:HDFCLIFE-EQ', 'NSE:UNIONBANK-EQ']
    fyers.subscribe(symbols=symbols, data_type=data_type)

    # Keep the socket running to receive real-time data
    fyers.keep_running()


# Replace the sample access token with your actual access token obtained from Fyers
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCb05vNE9zaTNTVTIyOWctMUwxQ1hyM0d5NWtjWFpnMWVvNmxVWDdRVXpST3BqZkhjZkttTGhqblBldXNYdnVONzNva2xmQlZtQmlMdWc2eTFxeDd4V1BXTjBic2hCQlRpV2Iwd0ozUjZBY1BaRFVfZz0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiIwYTMxODdkYmUzMzc2MWIwOTVkMWZkNDZiMWViM2I4NzJjZjhmNGVkMTUyNWE1MmE5ZjJjOTgxNiIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiRkFBMzcwNjkiLCJhcHBUeXBlIjoxMDAsImV4cCI6MTc0ODQ3ODYwMCwiaWF0IjoxNzQ4NDA1Nzc0LCJpc3MiOiJhcGkuZnllcnMuaW4iLCJuYmYiOjE3NDg0MDU3NzQsInN1YiI6ImFjY2Vzc190b2tlbiJ9.u33z5TKyvVnC5t2wi-no5eI2yReecDcB0zT1C-EoNTU"

# Create a FyersDataSocket instance with the provided parameters
fyers = data_ws.FyersDataSocket(
    access_token=access_token,       # Access token in the format "appid:accesstoken"
    log_path="",                     # Path to save logs. Leave empty to auto-create logs in the current directory.
    litemode=False,                  # Lite mode disabled. Set to True if you want a lite response.
    write_to_file=False,              # Save response in a log file instead of printing it.
    reconnect=True,                  # Enable auto-reconnection to WebSocket on disconnection.
    on_connect=onopen,               # Callback function to subscribe to data upon connection.
    on_close=onclose,                # Callback function to handle WebSocket connection close events.
    on_error=onerror,                # Callback function to handle WebSocket errors.
    on_message=onmessage             # Callback function to handle incoming messages from the WebSocket.
)

# Establish a connection to the Fyers WebSocket
fyers.connect()
