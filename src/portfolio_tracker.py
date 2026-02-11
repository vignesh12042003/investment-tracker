import json
import os
import yfinance as yf
import pandas as pd
from datetime import datetime

# ---------- FILE PATHS ----------
PORTFOLIO_FILE = "data/portfolio.json"
TRANSACTION_FILE = "data/transactions.json"


# ---------- HELPERS ----------
def normalize_stock(stock):
    stock = stock.upper().strip()
    if not stock.endswith(".NS"):
        stock += ".NS"
    return stock


# ---------- LOAD PORTFOLIO SAFELY ----------
if os.path.exists(PORTFOLIO_FILE):
    try:
        with open(PORTFOLIO_FILE, "r") as f:
            portfolio_data = json.load(f)
    except:
        portfolio_data = []
else:
    portfolio_data = []


# ---------- SAVE HELPERS ----------
def save_portfolio():
    os.makedirs("data", exist_ok=True)
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(portfolio_data, f, indent=4)


def log_transaction(action, stock, shares):
    os.makedirs("data", exist_ok=True)

    if os.path.exists(TRANSACTION_FILE):
        try:
            with open(TRANSACTION_FILE, "r") as f:
                transactions = json.load(f)
        except:
            transactions = []
    else:
        transactions = []

    transactions.append({
        "Action": action,
        "Stock": stock,
        "Shares": shares,
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    with open(TRANSACTION_FILE, "w") as f:
        json.dump(transactions, f, indent=4)


# ---------- CORE FUNCTIONS ----------
def get_portfolio():
    rows = []
    total_invested = 0
    total_current = 0

    for item in portfolio_data:
        stock = item["Stock"]
        shares = item["Shares"]

        # 🔐 SAFE access (handles old data)
        buy_price = item.get("BuyPrice", 0)

        try:
            ticker = yf.Ticker(stock)
            hist = ticker.history(period="5d")
            price = round(hist["Close"].iloc[-1], 2) if not hist.empty else 0
        except:
            price = 0

        invested = round(shares * buy_price, 2)
        current_value = round(shares * price, 2)
        profit_loss = round(current_value - invested, 2)

        total_invested += invested
        total_current += current_value

        rows.append({
            "Stock": stock,
            "Shares": shares,
            "Buy Price": buy_price,
            "Current Price": price,
            "Invested": invested,
            "Current Value": current_value,
            "Profit / Loss": profit_loss
        })

    df = pd.DataFrame(rows)

    if not df.empty:
        df.loc[len(df)] = [
            "TOTAL", "", "", "",
            round(total_invested, 2),
            round(total_current, 2),
            round(total_current - total_invested, 2)
        ]

    return df



def add_stock(stock, shares, buy_price):
    stock = normalize_stock(stock)
    shares = int(shares)
    buy_price = float(buy_price)

    for item in portfolio_data:
        if item["Stock"] == stock:
            item["Shares"] += shares
            item["BuyPrice"] = buy_price
            save_portfolio()
            log_transaction("BUY", stock, shares)
            return f"Added {shares} more shares of {stock}."

    portfolio_data.append({
        "Stock": stock,
        "Shares": shares,
        "BuyPrice": buy_price
    })

    save_portfolio()
    log_transaction("BUY", stock, shares)
    return f"{stock} added successfully."


def remove_stock(stock):
    stock = normalize_stock(stock)

    for item in portfolio_data:
        if item["Stock"] == stock:
            portfolio_data.remove(item)
            save_portfolio()
            log_transaction("SELL", stock, item["Shares"])
            return f"{stock} removed from portfolio."

    return f"{stock} not found in portfolio."


def get_transactions():
    if os.path.exists(TRANSACTION_FILE):
        with open(TRANSACTION_FILE, "r") as f:
            data = json.load(f)
        return pd.DataFrame(data)

    return pd.DataFrame(columns=["Action", "Stock", "Shares", "Timestamp"])
