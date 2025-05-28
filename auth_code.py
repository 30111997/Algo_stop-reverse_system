# Import the required module from the fyers_apiv3 package
from fyers_apiv3 import fyersModel

# Define your Fyers API credentials
client_id = "VCFZIJXBJX-100"  # Replace with your client ID
secret_key = "8CDU7QIBKY"  # Replace with your secret key
redirect_uri = "https://www.google.com/"  # Replace with your redirect URI
response_type = "code" 
grant_type = "authorization_code"  

# The authorization code received from Fyers after the user grants access
auth_code = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBfaWQiOiJWQ0ZaSUpYQkpYIiwidXVpZCI6IjYxN2E5YTZhOGMzOTQ4YjRhMzc4N2I5NTExZTgwYWViIiwiaXBBZGRyIjoiIiwibm9uY2UiOiIiLCJzY29wZSI6IiIsImRpc3BsYXlfbmFtZSI6IkZBQTM3MDY5Iiwib21zIjoiSzEiLCJoc21fa2V5IjoiMGEzMTg3ZGJlMzM3NjFiMDk1ZDFmZDQ2YjFlYjNiODcyY2Y4ZjRlZDE1MjVhNTJhOWYyYzk4MTYiLCJpc0RkcGlFbmFibGVkIjoiTiIsImlzTXRmRW5hYmxlZCI6Ik4iLCJhdWQiOiJbXCJkOjFcIixcIng6MFwiLFwieDoxXCIsXCJ4OjJcIl0iLCJleHAiOjE3NDg0MzU2NTgsImlhdCI6MTc0ODQwNTY1OCwiaXNzIjoiYXBpLmxvZ2luLmZ5ZXJzLmluIiwibmJmIjoxNzQ4NDA1NjU4LCJzdWIiOiJhdXRoX2NvZGUifQ.Blm6i009nxo8FcbCow565MWq40aC59eCCjNR3mYt-WQ"

# Create a session object to handle the Fyers API authentication and token generation
session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_key, 
    redirect_uri=redirect_uri, 
    response_type=response_type, 
    grant_type=grant_type
)

# Set the authorization code in the session object
session.set_token(auth_code)

# Generate the access token using the authorization code
response = session.generate_token()

# Print the response, which should contain the access token and other details
print(response)
