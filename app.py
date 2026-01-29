import streamlit as st
import hashlib
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# --- 1. CONFIGURATION & REBRANDING ---
st.set_page_config(page_title="ABHI_NEW_MART-1.0 | Enterprise System", page_icon="🏢", layout="wide")

# --- 2. DATA & SESSION STATE SETUP ---
# Inventory
if 'inventory' not in st.session_state:
    st.session_state.inventory = [
        {"ID": 101, "Product": "Nike Air Jordan", "Category": "Footwear", "Price": 12000, "Stock": 10},
        {"ID": 102, "Product": "Adidas Ultraboost", "Category": "Footwear", "Price": 15000, "Stock": 15},
        {"ID": 103, "Product": "Apple iPhone 15", "Category": "Electronics", "Price": 80000, "Stock": 5},
        {"ID": 104, "Product": "Samsung S24 Ultra", "Category": "Electronics", "Price": 110000, "Stock": 8},
        {"ID": 105, "Product": "Levi's Denim Jacket", "Category": "Apparel", "Price": 4500, "Stock": 25},
    ]

# Customer CRM
if 'customers' not in st.session_state:
    st.session_state.customers = {
        "9876543210": {"Name": "Amit Kumar", "Points": 150, "Total Spent": 12000},
        "9988776655": {"Name": "Priya Singh", "Points": 40, "Total Spent": 3500}
    }

# Coupons
coupons = {
    "WELCOME10": 0.10,  "VIP20": 0.20, "FLAT500": 500
}

# Session Variables
if 'cart' not in st.session_state: st.session_state.cart = []
if 'sales_history' not in st.session_state: st.session_state.sales_history = []
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'current_customer' not in st.session_state: st.session_state.current_customer = None

# --- 3. HELPER FUNCTIONS & 3D VISUALS ---
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

users_db = {
    "manager": {"name": "Abhishek Jatav", "role": "abhishek", "password": make_hashes("abhi123")},
    "cashier1": {"name": "Rahul Sharma", "role": "krishna", "password": make_hashes("Rsoft123")}
}

def get_product_details(name):
    for item in st.session_state.inventory:
        if item["Product"] == name: return item
    return None

# --- 3D AI Visual Generator ---
def get_3d_ai_visual():
    df_3d = pd.DataFrame(np.random.randn(200, 3), columns=['X', 'Y', 'Z'])
    fig = px.scatter_3d(df_3d, x='X', y='Y', z='Z', color='Z', opacity=0.6, 
                        color_continuous_scale='Viridis')
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), 
                      scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False)),
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300)
    return fig

# --- TRANSACTION PROCESSING ---
def process_transaction(discount_amt, subtotal_amt, tax_amt, grand_total_amt):
    bill_id = f"INV-{int(time.time())}"
    current_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for cart_item in st.session_state.cart:
        for inventory_item in st.session_state.inventory:
            if inventory_item["Product"] == cart_item["Item"]:
                inventory_item["Stock"] -= cart_item["Qty"]
    
    cust_name = "Guest"
    phone = "N/A"
    if st.session_state.current_customer:
        phone = st.session_state.current_customer
        points_earned = int((grand_total_amt) / 100)
        st.session_state.customers[phone]["Points"] += points_earned
        st.session_state.customers[phone]["Total Spent"] += grand_total_amt
        cust_name = st.session_state.customers[phone]["Name"]

    sale_record = {
        "Bill ID": bill_id,
        "Date Time": current_dt,
        "Customer": cust_name,
        "Phone": phone,
        "Subtotal": subtotal_amt,
        "Discount": discount_amt,
        "Tax": tax_amt,
        "Grand Total": grand_total_amt,
        "Cashier": st.session_state.get('user_name', 'Unknown'),
        "Items Detail": st.session_state.cart.copy()
    }
    st.session_state.sales_history.append(sale_record)
    return bill_id

# --- 4. LOGIN PAGE (FIXED CODE HERE) ---
def login_page():
    st.markdown("<h1 style='text-align:center; color:#0071ce;'>🏢 ABHI_NEW_MART-1.0</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'>System Time: {datetime.now().strftime('%d-%b-%Y | %I:%M %p')}</p>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([1.5, 1])
    with c1:
        st.plotly_chart(get_3d_ai_visual(), use_container_width=True)
        st.caption("Secure AI-Powered Retail Environment")
        
    with c2:
        # --- FIX: Added st.form() wrapper here ---
        with st.container(border=True):
            with st.form("login_form"): 
                st.subheader("System Login")
                user = st.text_input("Username")
                pwd = st.text_input("Password", type="password")
                
                # Now st.form_submit_button is inside st.form, so NO ERROR
                submitted = st.form_submit_button("🔒 Authenticate")
                
                if submitted:
                    if user in users_db and check_hashes(pwd, users_db[user]['password']):
                        st.session_state.logged_in = True
                        st.session_state.user_role = users_db[user]['role']
                        st.session_state.user_name = users_db[user]['name']
                        st.rerun()
                    else:
                        st.error("Invalid Access Credentials.")

# --- 5. MAIN APPLICATION ---
def main_app():
    with st.sidebar:
        st.markdown(f"## 🕒 {datetime.now().strftime('%I:%M %p')}")
        st.caption(f"📅 {datetime.now().strftime('%d-%B-%Y')}")
        st.divider()
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=60)
        st.write(f"User: **{st.session_state.user_name}**")
        st.caption(f"Role: {st.session_state.user_role}")
        
        menu = ["POS Terminal", "CRM (Customers)", "Inventory", "Analytics & Search"]
        if st.session_state.user_role == "Staff":
            menu = ["POS Terminal", "CRM (Customers)", "Inventory"]
            
        choice = st.radio("Navigation", menu)
        st.divider()
        if st.button("🔴 Log Out"):
            st.session_state.logged_in = False
            st.rerun()

    if choice == "POS Terminal":
        c_head_1, c_head_2 = st.columns([3, 1])
        c_head_1.title("🛒 POS Billing")
        c_head_2.markdown(f"**Date:** {datetime.now().strftime('%d-%m-%Y')}")
        
        with st.container(border=True):
            c1, c2, c3 = st.columns([2, 1, 1])
            phone_input = c1.text_input("📞 Customer Phone (Optional)", placeholder="Enter 10-digit number")
            if c2.button("Find Customer"):
                if phone_input in st.session_state.customers:
                    cust = st.session_state.customers[phone_input]
                    st.session_state.current_customer = phone_input
                    c3.success(f"Verified: {cust['Name']}")
                    c3.caption(f"Points: {cust['Points']}")
                else:
                    st.session_state.current_customer = None
                    c3.warning("New Customer")
                    if c2.button("Register New"):
                        st.session_state.customers[phone_input] = {"Name": "New User", "Points": 0, "Total Spent": 0}
                        st.success("Registered!")

        col_left, col_right = st.columns([1, 1.2])

        with col_left:
            st.subheader("Scan Items")
            product_list = [p["Product"] for p in st.session_state.inventory]
            selected_product = st.selectbox("Select Product", product_list)
            details = get_product_details(selected_product)
            st.info(f"Price: ₹{details['Price']} | Stock: {details['Stock']}")
            qty = st.number_input("Qty", min_value=1, value=1)
            if st.button("➕ Add to Cart", type="primary", use_container_width=True):
                if qty <= details['Stock']:
                    total = qty * details['Price']
                    st.session_state.cart.append({"Item": selected_product, "Qty": qty, "Price": details['Price'], "Total": total})
                    st.toast("Item Added!")
                else: st.error("❌ Out of Stock!")

        with col_right:
            st.subheader("🧾 Receipt Preview")
            st.caption(f"Invoice Time: {datetime.now().strftime('%I:%M %p')}")
            if st.session_state.cart:
                df_cart = pd.DataFrame(st.session_state.cart)
                st.dataframe(df_cart, hide_index=True, use_container_width=True)
                
                subtotal = df_cart['Total'].sum()
                coupon_code = st.text_input("🎟️ Apply Coupon")
                discount = 0
                if coupon_code and coupon_code in coupons:
                    val = coupons[coupon_code]
                    discount = subtotal * val if val < 1 else val
                    st.caption(f"Coupon Applied: -₹{discount}")

                use_points = st.checkbox("Redeem Points?")
                points_discount = 0
                if use_points and st.session_state.current_customer:
                    avail = st.session_state.customers[st.session_state.current_customer]["Points"]
                    points_discount = min(avail, subtotal - discount)
                    st.caption(f"Points Redeemed: -₹{points_discount}")

                total_discount = discount + points_discount
                tax = (subtotal - total_discount) * 0.18
                grand_total = (subtotal - total_discount) + tax

                st.divider()
                r1, r2 = st.columns(2)
                r1.markdown(f"Subtotal: ₹{subtotal}")
                r1.markdown(f"Discount: -₹{total_discount}")
                r1.markdown(f"GST (18%): ₹{tax:.2f}")
                r2.markdown(f"### Total: ₹{grand_total:.2f}")
                
                if r2.button("✅ CHECKOUT & PRINT", type="primary"):
                    with st.spinner("Processing Transaction..."):
                        time.sleep(1)
                        if use_points and st.session_state.current_customer:
                            st.session_state.customers[st.session_state.current_customer]["Points"] -= int(points_discount)
                        
                        new_bill_id = process_transaction(total_discount, subtotal, tax, grand_total)
                        st.session_state.cart = []
                        st.session_state.current_customer = None
                        st.balloons()
                        st.success(f"Transaction Successful! Bill No: {new_bill_id}")
                        time.sleep(3)
                        st.rerun()

    elif choice == "CRM (Customers)":
        st.title("👥 Customer Database")
        st.write(f"As on: {datetime.now().strftime('%d-%b-%Y %I:%M %p')}")
        crm_data = []
        for phone, data in st.session_state.customers.items():
            row = data.copy()
            row['Phone'] = phone
            crm_data.append(row)
        st.dataframe(pd.DataFrame(crm_data), use_container_width=True)

    elif choice == "Inventory":
        st.title("📦 Warehouse Stock")
        st.caption(f"Last Updated: {datetime.now().strftime('%I:%M %p')}")
        df_inv = pd.DataFrame(st.session_state.inventory)
        c1, c2 = st.columns(2)
        c1.metric("Total SKU Count", len(df_inv))
        c2.metric("⚠️ Low Stock Alerts", len(df_inv[df_inv['Stock'] < 5]), delta_color="inverse")
        st.dataframe(df_inv.style.map(lambda x: 'background-color: #ffcccc' if x < 5 else '', subset=['Stock']), use_container_width=True)

    elif choice == "Analytics & Search":
        st.title("📈 Analytics & Records")
        st.caption(f"Report Time: {datetime.now().strftime('%d-%b-%Y %I:%M %p')}")
        
        tab1, tab2 = st.tabs(["📊 Sales Report", "🔍 Search Old Bill"])
        
        with tab1:
            if not st.session_state.sales_history:
                st.info("No sales data available.")
            else:
                df_sales = pd.DataFrame(st.session_state.sales_history)
                k1, k2, k3 = st.columns(3)
                k1.metric("Total Revenue", f"₹{df_sales['Grand Total'].sum():,.2f}")
                k2.metric("Total Discounts", f"₹{df_sales['Discount'].sum():,.2f}")
                k3.metric("Total Bills", len(df_sales))
                st.subheader("Transaction Log")
                st.dataframe(df_sales[['Bill ID', 'Date Time', 'Customer', 'Grand Total']], use_container_width=True)
                
                c1, c2 = st.columns(2)
                c1.plotly_chart(get_3d_ai_visual(), use_container_width=True)
                c2.caption("AI Sales Trend Analysis (Visual Placeholder)")

        with tab2:
            st.subheader("Find Past Invoice")
            search_bill_no = st.text_input("Enter Bill No. (e.g., INV-169...)")
            if st.button("🔍 Search Bill"):
                found_bill = None
                for bill in st.session_state.sales_history:
                    if bill['Bill ID'] == search_bill_no:
                        found_bill = bill
                        break
                
                if found_bill:
                    st.success(f"Bill Found: {found_bill['Bill ID']}")
                    with st.container(border=True):
                        st.markdown(f"### 🧾 INVOICE REPRINT")
                        st.write(f"**Date:** {found_bill['Date Time']}")
                        st.write(f"**Customer:** {found_bill['Customer']} ({found_bill['Phone']})")
                        st.write(f"**Cashier:** {found_bill['Cashier']}")
                        st.divider()
                        st.write("**Items Purchased:**")
                        st.dataframe(pd.DataFrame(found_bill['Items Detail']), hide_index=True)
                        st.divider()
                        b1, b2 = st.columns(2)
                        b1.write(f"Subtotal: ₹{found_bill['Subtotal']}")
                        b1.write(f"Discount: -₹{found_bill['Discount']}")
                        b1.write(f"Tax: ₹{found_bill['Tax']:.2f}")
                        b2.markdown(f"### Grand Total: ₹{found_bill['Grand Total']:.2f}")
                else:
                    st.error("Bill not found in records.")

# Run Logic
if st.session_state.logged_in:
    main_app()
else:
    login_page()