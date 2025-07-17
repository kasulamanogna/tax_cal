import streamlit as st

# --- Simulated backend logic (replace with API calls later) ---
if 'users' not in st.session_state:
    st.session_state['users'] = {}
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = {"username": None}
if 'tax_histories' not in st.session_state:
    st.session_state['tax_histories'] = {}

users = st.session_state['users']
current_user = st.session_state['current_user']
tax_histories = st.session_state['tax_histories']

def register_user(username, password):
    if username in users:
        return False, "User already exists"
    users[username] = password
    return True, "Registered successfully"

def login_user(username, password):
    if users.get(username) == password:
        current_user["username"] = username
        return True, "Login successful"
    return False, "Invalid credentials"

def calculate_tax(income, regime="old"):
    if regime == "old":
        if income <= 250000:
            return 0
        elif income <= 500000:
            return (income - 250000) * 0.05
        elif income <= 1000000:
            return 12500 + (income - 500000) * 0.20
        else:
            return 112500 + (income - 1000000) * 0.30
    elif regime == "new":
        if income <= 250000:
            return 0
        elif income <= 500000:
            return (income - 250000) * 0.05
        elif income <= 750000:
            return 12500 + (income - 500000) * 0.10
        elif income <= 1000000:
            return 37500 + (income - 750000) * 0.15
        elif income <= 1250000:
            return 75000 + (income - 1000000) * 0.20
        elif income <= 1500000:
            return 125000 + (income - 1250000) * 0.25
        else:
            return 187500 + (income - 1500000) * 0.30
    return 0

# --- UI Flow ---
st.title("India Income Tax Calculator")

menu = ["Register", "Login"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Register":
    st.subheader("Create New Account")
    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type='password')
    if st.button("Register"):
        success, msg = register_user(new_user, new_password)
        st.success(msg) if success else st.error(msg)

elif choice == "Login":
    st.subheader("Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        success, msg = login_user(username, password)
        st.success(msg) if success else st.error(msg)

    if current_user["username"]:
        st.success(f"Welcome, {current_user['username']}!")

        st.header("Calculate Your Tax")

        income = st.number_input("Enter your Gross Income (per year)", min_value=0, step=1000)
        regime = st.selectbox("Choose Tax Regime", ["old", "new"])

        if st.button("Calculate Tax"):
            tax = calculate_tax(income, regime)
            st.success(f"Total Tax Payable: ₹{tax:,.2f}")
            # Store tax history
            user = current_user["username"]
            if user not in tax_histories:
                tax_histories[user] = []
            tax_histories[user].append({
                "year": 2024,  # You can make this dynamic
                "total_income": income,
                "tax_paid": tax,
                "regime": regime
            })

        