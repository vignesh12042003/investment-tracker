import streamlit as st
import pandas as pd
import requests
from src import watchlist, portfolio_tracker, stock_analysis, new_insights, profile

BACKEND_URL =  "http://127.0.0.1:8000/api"

# ---------------- JWT TOKEN INIT ----------------
if "access_token" not in st.session_state:
    st.session_state.access_token = None

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ---------------- USER HELPERS ----------------
def get_headers():
    token = st.session_state.get("access_token")

    if not token:
        return {}

    return {
        "Authorization": f"Bearer {token}"
    }


def fetch_current_user():
    r = requests.get(f"{BACKEND_URL}/me/", headers=get_headers())
    if r.status_code == 200:
        return r.json().get("username")
    return None


# ---------------- LOGIN / SIGNUP ----------------
def login_ui():
    if "show_signup" not in st.session_state:
        st.session_state.show_signup = False

    if not st.session_state.show_signup:
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            r = requests.post(  # 🔥 CHANGED
                f"{BACKEND_URL}/token/",
                json={"username": username, "password": password}
            )
            if r.status_code == 200:
                data = r.json()
                st.session_state.access_token = data["access"]  # 🔥 CHANGED
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid credentials")

        if st.button("Create an account"):
            st.session_state.show_signup = True
            st.rerun()

    else:
        st.title("Create Account")
        u = st.text_input("Username")
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")

        if st.button("Sign Up"):
            r = requests.post(
                f"{BACKEND_URL}/register/",
                json={"username": u, "email": e, "password": p}
            )
            if r.status_code == 201:
                st.success("Account created. Please login.")
                st.session_state.show_signup = False
                st.rerun()
            else:
                st.error("Signup failed")


# ---------------- LOGIN GATE ----------------
if not st.session_state.logged_in:
    login_ui()
    st.stop()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Investment Tracker", layout="wide")


# ---------------- BACKEND HELPERS ----------------
def fetch_portfolio_from_backend():
    r = requests.get(f"{BACKEND_URL}/portfolio/", headers=get_headers())  # 🔥 CHANGED
    return r.json() if r.status_code == 200 else []

def fetch_watchlist_from_backend():
    r = requests.get(f"{BACKEND_URL}/watchlist/", headers=get_headers())  # 🔥 CHANGED
    return r.json() if r.status_code == 200 else []

def fetch_transactions():
    r = requests.get(f"{BACKEND_URL}/transactions/", headers=get_headers())  # 🔥 CHANGED
    return r.json() if r.status_code == 200 else []

def submit_transaction(symbol, ttype, qty):
    headers = get_headers()

    st.write("HEADERS:", headers)   # 🔥 DEBUG

    return requests.post(
        f"{BACKEND_URL}/transaction/",
        json={
            "stock_symbol": symbol,
            "transaction_type": ttype,
            "quantity": qty
        },
        headers=headers
    )

def add_watchlist_backend(stock):
    return requests.post(  # 🔥 CHANGED
        f"{BACKEND_URL}/watchlist/",
        json={"stock_symbol": stock},
        headers=get_headers()
    )

def remove_watchlist_backend(stock):
    return requests.delete(  # 🔥 CHANGED
        f"{BACKEND_URL}/watchlist/",
        json={"stock_symbol": stock},
        headers=get_headers()
    )

def calculate_portfolio_summary(data):
    invested = value = 0
    for r in data:
        q = r.get("total_quantity", 0)
        avg = r.get("avg_buy_price", 0)
        cur = r.get("current_price", avg)
        invested += q * avg
        value += q * cur
    return {
        "total_invested": invested,
        "market_value": value,
        "pnl": value - invested,
        "holdings": len(data)
    }

# ---------------- SIDEBAR ----------------
st.sidebar.title("📊 Investment Tracker")

page = st.sidebar.radio(
    "Navigate",
    ["📊 Watchlist", "📂 Portfolio", "📈 Stock Analysis", "📰 News", "📨 Contact Us"]
)

# Visual separator
st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

# Logout (BOTTOM OF SIDEBAR – NOT FLOATING)
st.sidebar.markdown('<div class="logout-btn">', unsafe_allow_html=True)
if st.sidebar.button("🚪 Logout"):
    st.session_state.session.post(f"{BACKEND_URL}/logout/")
    st.session_state.logged_in = False
    st.session_state.username = None
    st.rerun()
st.sidebar.markdown('</div>', unsafe_allow_html=True)


# ---------------- HEADER ----------------
username = st.session_state.get("username", "USER")
st.markdown(f"""
<h2>👋 WELCOME, <span style="color:#2563eb;">{username.upper()}</span></h2>
<p>Investment & Stock Tracker Dashboard</p>
<hr>
""", unsafe_allow_html=True)

# ---------------- WATCHLIST ----------------
if page == "📊 Watchlist":
    st.header("📊 Watchlist")
    data = fetch_watchlist_from_backend()

    if not data:
        st.info("No stocks in watchlist")
    else:
        for i in data:
            c1, c2 = st.columns([9,1])
            c1.write(i["stock_symbol"])
            if c2.button("❌", key=i["stock_symbol"]):
                remove_watchlist_backend(i["stock_symbol"])
                st.rerun()

    stock = st.text_input("Add Stock Symbol")
    if st.button("➕ Add Stock"):
        add_watchlist_backend(stock)
        st.rerun()

# ---------------- PORTFOLIO ----------------
elif page == "📂 Portfolio":
    st.header("📂 Portfolio Tracker")
    pdata = fetch_portfolio_from_backend()

    if pdata:
        s = calculate_portfolio_summary(pdata)
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("💰 Total Invested", f"₹ {s['total_invested']:,.2f}")
        c2.metric("📈 Market Value", f"₹ {s['market_value']:,.2f}")
        c3.metric("📊 P&L", f"₹ {s['pnl']:,.2f}")
        c4.metric("🧾 Holdings", s["holdings"])
        st.divider()

    sym = st.text_input("Stock Symbol")
    qty = st.number_input("Quantity", min_value=1, step=1)

    # ✅ MUST BE INSIDE THIS BLOCK
    b1, b2 = st.columns(2)

    # ---------------- BUY ----------------
    if b1.button("🟢 BUY"):
        response = submit_transaction(sym, "BUY", qty)

        st.write("Status:", response.status_code)
        st.write("Response:", response.text)

        if response.status_code == 200:
            st.success("Stock added successfully")
            st.rerun()
        else:
            st.error("Failed to add stock")

    # ---------------- SELL ----------------
    if b2.button("🔴 SELL"):
        response = submit_transaction(sym, "SELL", qty)

        st.write("Status:", response.status_code)
        st.write("Response:", response.text)

        if response.status_code == 200:
            st.success("Stock sold successfully")
            st.rerun()
        else:
            st.error("Failed to sell stock")

    st.subheader("📊 Current Portfolio")
    st.dataframe(pd.DataFrame(pdata), hide_index=True)

    st.subheader("📜 Transaction History")
    tx = fetch_transactions()
    if tx:
        st.dataframe(pd.DataFrame(tx), hide_index=True)
    else:
        st.info("No transactions yet")

# ---------------- STOCK ANALYSIS ----------------
elif page == "📈 Stock Analysis":
    st.header("📈 Stock Analysis")
    sym = st.text_input("Stock Symbol")
    if st.button("Analyze"):
        d = stock_analysis.get_stock_data(sym)
        if not d.empty:
            st.dataframe(d.tail())
            st.image(stock_analysis.plot_stock_chart(d, sym))
        else:
            st.warning("No data found")

# ---------------- NEWS ----------------
elif page == "📰 News":
    st.header("📰 Market News")
    for n in new_insights.get_news():
        st.markdown(f"- {n}")

# ---------------- CONTACT ----------------
elif page == "📨 Contact Us":
    st.header("📨 Contact Us")
    n = st.text_input("Name")
    e = st.text_input("Email")
    m = st.text_area("Message")
    if st.button("Send"):
        if not n or not e or not m:
            st.warning("Fill all fields")
        else:
            st.success("Message sent")

st.markdown("""
<div class="main-footer">
    © 2026 Investment Tracker · Built with Django & Streamlit
</div>
""", unsafe_allow_html=True)

