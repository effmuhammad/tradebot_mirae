import yfinance as yf

# Define the ticker for the stock you want to get data for
ticker = "ANTM.JK"

# Download 3 months of historical data using the daily time frame
data = yf.download(ticker, period="1d", interval="1d")

# Print the DataFrame to see the data
print(data['Close'])