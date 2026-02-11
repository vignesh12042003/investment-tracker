import json
import os

DATA_FILE = "data/watchlist.json"

# Load watchlist from JSON if exists, else default
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        watchlist = [stock.upper() for stock in json.load(f)]  # normalize
else:
    watchlist = ["AAPL", "GOOGL", "TSLA"]

# Save normalized watchlist back
def save_watchlist():
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(list(set(watchlist)), f)  # remove duplicates


# Get current watchlist
def get_watchlist():
    return watchlist

# Add a stock to watchlist
def add_stock(stock):
    stock = stock.upper()
    if stock not in watchlist:
        watchlist.append(stock)
        save_watchlist()
        return f"{stock} added to watchlist."
    else:
        return f"{stock} is already in watchlist."

def remove_stock(stock):
    stock = stock.upper()
    if stock in watchlist:
        watchlist.remove(stock)
        save_watchlist()
        return f"{stock} removed from watchlist."
    else:
        return f"{stock} not found in watchlist."


# Test
if __name__ == "__main__":
    print("Current Watchlist:", get_watchlist())
    print(add_stock("sbin.ns"))
    print(remove_stock("lt.ns"))
    print(get_watchlist())
