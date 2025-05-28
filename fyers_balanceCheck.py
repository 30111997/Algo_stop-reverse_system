from fyers_api import fyersModel

# Replace these with your actual credentials
CLIENT_ID = "VCFZIJXBJX-100"  # From Fyers API dashboard (format: XXXXXX-100)
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"  # Generated via auth process

def get_fyers_balance():
    """
    Fetches and displays account balance from Fyers API
    """
    try:
        # Initialize Fyers model
        fyers = fyersModel.FyersModel(
            client_id=CLIENT_ID,
            token=ACCESS_TOKEN,
            log_path="/logs"  # Optional: for storing logs
        )
        
        # Get account funds
        response = fyers.funds()
        
        # Display balance information
        print("\nAccount Balance Summary")
        print("="*40)
        print(f"{'Fund Type':<20} | {'Amount (₹)':>15}")
        print("-"*40)
        
        for fund in response.get("fund_limit", []):
            print(f"{fund['title']:<20} | {float(fund['equityAmount']):>15.2f}")
        
        print("="*40)
        
    except Exception as e:
        print(f"\nError fetching balance: {e}")

if __name__ == "__main__":
    get_fyers_balance()