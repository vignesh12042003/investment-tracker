# alerts_notifications.py

alerts = []

def add_alert(stock, target_price):
    alerts.append({"stock": stock, "target_price": target_price})
    print(f"Alert added: {stock} at ${target_price}")

def view_alerts():
    print("Your Alerts:")
    for alert in alerts:
        print(f"{alert['stock']} → ${alert['target_price']}")

# Test
if __name__ == "__main__":
    add_alert("AAPL", 200)
    view_alerts()

alerts = ["AAPL +5% today", "TSLA -3% today"]

def get_alerts():
    return alerts
