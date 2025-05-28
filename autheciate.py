from fyers_api.WebSocket import ws
from fyers_api import fyersModel

# Replace these values
APP_ID = "YOUR_APP_ID"  # Format: XXXXXX-100
SECRET_KEY = "YOUR_SECRET_KEY"
REDIRECT_URI = "https://www.google.com/"  # Must match dashboard

# Create session
fyers = fyersModel.FyersModel(client_id=APP_ID, 
                            token="", 
                            log_path="")

# Generate auth URL
auth_url = fyers.generate_authcode(client_id=APP_ID, 
                                 redirect_uri=REDIRECT_URI)
print("Open this URL in browser:", auth_url)