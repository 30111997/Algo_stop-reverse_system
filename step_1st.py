import os
import requests
import json
import time
import pyotp
from fyers_api import fyersModel
from fyers_api import accessToken


# FYERS क्रेडेंशियल्स
client_id = "FAA37069"  # आपका App ID (XXXXX-XXX format)
secret_key = "CY95JDM8M5"
username = "FAA37069"
password = "Deva@009"
pin = "8484"  # 4-digit pin
totp_key = "ZFBQV5TJK3Y2NYSCCEG23FXAHU4LPIIX"  # TOTP secret key from FYERS

# 1. सेशन मॉड्यूल का उपयोग करके लॉगिन URL प्राप्त करें
def get_auth_code():
    session = accessToken.SessionModel(
        client_id=client_id,
        secret_key=secret_key,
        redirect_uri="https://www.google.com/",  # Redirect URL (must match in FYERS dashboard)
        response_type="code",
        grant_type="authorization_code"
    )
    
    # Generate TOTP
    totp = pyotp.TOTP(totp_key).now()
    
    # Login request
    response = requests.post(
        'https://api-t2.fyers.in/vagator/v2/send_login_otp_v2',
        json={"fy_id": username, "app_id": "2"}
    )
    request_key = response.json()["request_key"]
    
    # Verify TOTP
    response = requests.post(
        'https://api-t2.fyers.in/vagator/v2/verify_otp',
        json={"request_key": request_key, "otp": totp}
    )
    request_key = response.json()["request_key"]
    
    # Verify PIN
    response = requests.post(
        'https://api-t2.fyers.in/vagator/v2/verify_pin_v2',
        json={"request_key": request_key, "identity_type": "pin", "identifier": pin}
    )
    access_token = response.json()["data"]["access_token"]
    
    # Get auth code
    session.set_token(access_token)
    auth_code = session.generate_authcode()
    return auth_code

# 2. एक्सेस टोकन प्राप्त करें
def get_access_token(auth_code):
    session = accessToken.SessionModel(
        client_id=client_id,
        secret_key=secret_key,
        redirect_uri="https://www.google.com/",
        response_type="code",
        grant_type="authorization_code"
    )
    
    session.set_token(auth_code)
    response = session.generate_token()
    access_token = response["access_token"]
    
    # Save token to file for future use
    with open("access_token.txt", "w") as f:
        f.write(access_token)
    
    return access_token

# 3. FYERS मॉडल इनिशियलाइज़ करें
def init_fyers_model(access_token):
    fyers = fyersModel.FyersModel(
        client_id=client_id,
        token=access_token,
        log_path=os.getcwd(),
    )
    return fyers

# मुख्य फंक्शन
def main():
    # Check if access token already exists
    try:
        with open("access_token.txt", "r") as f:
            access_token = f.read()
    except FileNotFoundError:
        auth_code = get_auth_code()
        access_token = get_access_token(auth_code)
    
    fyers = init_fyers_model(access_token)
    
    # Test API connection
    profile = fyers.get_profile()
    print("Profile:", profile)
    
    # यहाँ पर अपना एल्गोरिथम लॉजिक जोड़ें
    # उदाहरण: मार्केट डेटा प्राप्त करना
    # data = {
    #     "symbol": "NSE:SBIN-EQ",
    #     "resolution": "1",
    #     "date_format": "1",
    #     "range_from": "2023-01-01",
    #     "range_to": "2023-01-10",
    #     "cont_flag": "1"
    # }
    # hist_data = fyers.history(data)
    # print("Historical Data:", hist_data)

if __name__ == "__main__":
    main()