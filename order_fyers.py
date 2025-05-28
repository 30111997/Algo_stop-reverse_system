from fyers_apiv3 import fyersModel

client_id = "VCFZIJXBJX-100"
access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCb05vNE9zaTNTVTIyOWctMUwxQ1hyM0d5NWtjWFpnMWVvNmxVWDdRVXpST3BqZkhjZkttTGhqblBldXNYdnVONzNva2xmQlZtQmlMdWc2eTFxeDd4V1BXTjBic2hCQlRpV2Iwd0ozUjZBY1BaRFVfZz0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiIwYTMxODdkYmUzMzc2MWIwOTVkMWZkNDZiMWViM2I4NzJjZjhmNGVkMTUyNWE1MmE5ZjJjOTgxNiIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiRkFBMzcwNjkiLCJhcHBUeXBlIjoxMDAsImV4cCI6MTc0ODQ3ODYwMCwiaWF0IjoxNzQ4NDA1Nzc0LCJpc3MiOiJhcGkuZnllcnMuaW4iLCJuYmYiOjE3NDg0MDU3NzQsInN1YiI6ImFjY2Vzc190b2tlbiJ9.u33z5TKyvVnC5t2wi-no5eI2yReecDcB0zT1C-EoNTU'

# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, token=access_token,is_async=False, log_path="")

data = {
    "symbol":"NSE:HDFCLIFE-EQ",
    "qty":1,
    "type":2,
    "side":1,
    "productType":"INTRADAY",
    "limitPrice":0,
    "stopPrice":0,
    "validity":"DAY",
    "disclosedQty":0,
    "offlineOrder":False,
    "orderTag":"tag1"
}
response = fyers.place_order(data=data)
print(response)
