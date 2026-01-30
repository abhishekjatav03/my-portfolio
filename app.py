import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time
import random

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Luxora By ABHISHEK",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. GLOBAL STYLES (Luxury 3D)
# ==========================================
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); font-family: 'Helvetica Neue', sans-serif; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid rgba(0,0,0,0.1); }
    
    /* 3D Sidebar Avatar */
    .avatar-3d {
        display: block; margin-left: auto; margin-right: auto; width: 130px; height: 130px;
        border-radius: 50%; object-fit: cover; box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        border: 4px solid #00d2ff; transition: transform 0.3s;
    }
    .avatar-3d:hover { transform: scale(1.05); }

    /* Pulsing Green Dot */
    .online-indicator {
        height: 15px; width: 15px; background-color: #00ff88; border-radius: 50%;
        display: inline-block; animation: pulse-green 2s infinite;
    }
    @keyframes pulse-green {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(0, 255, 136, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 136, 0); }
    }

    /* Highlight Box */
    .highlight-box { padding: 15px; border-radius: 10px; margin-bottom: 20px; font-weight: bold; text-align: center; }
    .deleted { background-color: #ffebee; color: #c62828; border: 1px solid #ef9a9a; }
    .updated { background-color: #e8f5e9; color: #2e7d32; border: 1px solid #a5d6a7; }

    h1 {
        background: -webkit-linear-gradient(45deg, #007bff, #00d2ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800 !important;
    }
    
    /* Bill Layout */
    .bill-container {
        background: white; padding: 30px; border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); border: 1px solid #eee;
    }
    .bill-header { text-align: center; border-bottom: 2px dashed #ddd; padding-bottom: 20px; margin-bottom: 20px; }
    .bill-total { text-align: right; margin-top: 20px; padding-top: 10px; border-top: 2px solid #333; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. DATABASE
# ==========================================
if 'users' not in st.session_state:
    st.session_state.users = {"admin": {"password": "123", "name": "Abhishek Jatav", "role": "Admin"}}
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame([
        {"ID": "TXN-1001", "Date": "2026-01-20", "Category": "Food", "Amount": 450, "User": "Abhishek Jatav", "Note": "Lunch"},
        {"ID": "TXN-1002", "Date": "2026-01-22", "Category": "Bills", "Amount": 1200, "User": "Papa", "Note": "Electricity"}
    ])
if 'messages' not in st.session_state: st.session_state.messages = []
if 'last_action' not in st.session_state: st.session_state.last_action = None

# ==========================================
# 4. LOGIN PAGE
# ==========================================
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div style='text-align: center; margin-top: 50px;'>", unsafe_allow_html=True)
        # --- BIG 3D LOGO ---
        st.image("https://cdn-icons-png.flaticon.com/512/9376/9376757.png", width=140) # 3D Gem Icon
        st.markdown("<h1>Luxora By ABHISHEK</h1>", unsafe_allow_html=True)
        st.caption("Secure Personal Management Suite v9.0")
        
        tab1, tab2 = st.tabs(["🔒 Login", "📝 Sign Up"])
        with tab1:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login", use_container_width=True):
                users_db = st.session_state.users
                if username in users_db and users_db[username]["password"] == password:
                    st.session_state.logged_in_user = users_db[username]
                    st.session_state.username_id = username
                    st.success("Access Granted!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Incorrect Credentials")
        with tab2:
            new_name = st.text_input("Full Name")
            new_user = st.text_input("Create User ID")
            new_pass = st.text_input("Create Password", type="password")
            if st.button("Create Account", use_container_width=True):
                if new_user in st.session_state.users: st.warning("User Exists!")
                elif new_name and new_user and new_pass:
                    st.session_state.users[new_user] = {"password": new_pass, "name": new_name, "role": "User"}
                    st.success("Account Created! Login Now.")
                else: st.error("Fill all fields.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 5. MAIN APP
# ==========================================
def main_app():
    user_info = st.session_state.logged_in_user
    current_name = user_info['name']
    
    with st.sidebar:
        st.markdown(f"""
            <img src="https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg" class="avatar-3d">
            <div style="text-align: center; margin-top: 15px;">
                <h2 style="margin:0; color:#333;">{current_name}</h2>
                <p style="color:gray; font-size:14px;">ID: @{st.session_state.username_id}</p>
                <div style="background: #e0f2f1; padding: 5px; border-radius: 10px; display: inline-block;">
                    <span class="online-indicator"></span> 
                    <span style="color: #00695c; font-weight: bold; margin-left: 5px;">Online</span>
                </div>
            </div>
            <hr>
        """, unsafe_allow_html=True)
        menu = st.radio("Menu", ["Dashboard", "Finance Pro", "AI Brain", "Logout"], label_visibility="collapsed")
        if menu == "Logout":
            st.session_state.logged_in_user = None
            st.rerun()

    # --- DASHBOARD ---
    if menu == "Dashboard":
        c_head1, c_head2 = st.columns([4, 1])
        with c_head1:
            st.title(f"👋 Welcome Back, {current_name}")
            st.caption("Daily Smart Briefing")
        with c_head2:
            # 3D AI ROBOT (Online Status)
            st.markdown("""<div style="text-align: center;"><img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" width="90"><br><span class="online-indicator"></span> <b>System Live</b></div>""", unsafe_allow_html=True)
        
        df = st.session_state.expenses
        total = df["Amount"].sum()
        k1, k2, k3 = st.columns(3)
        k1.metric("Wallet Balance", f"₹{total}", "Live Update")
        k2.metric("Total Items", len(df))
        k3.metric("AI Status", "Active", "v9.0")
        
        if not df.empty:
            st.subheader("📊 Live Activity")
            fig = px.bar(df, x="Category", y="Amount", color="User")
            st.plotly_chart(fig, use_container_width=True)

    # --- FINANCE PRO ---
    elif menu == "Finance Pro":
        # HEADER WITH 3D LOGO
        c_logo, c_title = st.columns([1, 6])
        with c_logo: 
            st.image("https://cdn-icons-png.flaticon.com/512/1077/1077366.png", width=90) # 3D Wallet
        with c_title: 
            st.title("Finance Command Center")
        
        if st.session_state.last_action:
            act = st.session_state.last_action
            css = "deleted" if act['type'] == "delete" else "updated"
            st.markdown(f"<div class='highlight-box {css}'>{act['msg']}</div>", unsafe_allow_html=True)

        tab1, tab2, tab3, tab4 = st.tabs(["➕ Add Item", "🔍 Modify (Highlight)", "📑 Report", "🧾 Bill Generator"])
        
        with tab1:
            with st.form("new_entry"):
                c1, c2 = st.columns(2)
                dt = c1.date_input("Date")
                ct = c2.selectbox("Category", ["Food", "Travel", "Bills", "Shopping", "Other"])
                amt = c1.number_input("Amount", min_value=0)
                nt = c2.text_input("Note")
                if st.form_submit_button("Add Record"):
                    nid = f"TXN-{random.randint(1000,9999)}"
                    row = pd.DataFrame([{"ID": nid, "Date": str(dt), "Category": ct, "Amount": amt, "User": current_name, "Note": nt}])
                    st.session_state.expenses = pd.concat([st.session_state.expenses, row], ignore_index=True)
                    st.session_state.last_action = {"type": "update", "msg": f"✅ Added: {ct} (₹{amt})"}
                    st.rerun()

        with tab2:
            st.subheader("Update or Delete")
            search_id = st.text_input("Enter Transaction ID")
            if search_id:
                df = st.session_state.expenses
                record = df[df["ID"] == search_id]
                if not record.empty:
                    st.dataframe(record, hide_index=True)
                    c_up, c_del = st.columns(2)
                    with c_up:
                        with st.expander("✏️ Update"):
                            new_amt = st.number_input("New Amount", value=int(record.iloc[0]["Amount"]))
                            if st.button("Update"):
                                idx = record.index[0]
                                st.session_state.expenses.at[idx, "Amount"] = new_amt
                                st.session_state.last_action = {"type": "update", "msg": f"✏️ Updated ID {search_id} to ₹{new_amt}"}
                                st.rerun()
                    with c_del:
                        with st.expander("🗑️ Delete"):
                            if st.button("Confirm Delete"):
                                st.session_state.expenses = df[df["ID"] != search_id]
                                st.session_state.last_action = {"type": "delete", "msg": f"🗑️ DELETED ID {search_id}"}
                                st.rerun()
                else: st.warning("ID Not Found")

        with tab3:
            st.dataframe(st.session_state.expenses, use_container_width=True)

        with tab4:
            c_bill_logo, c_bill_title = st.columns([1, 6])
            with c_bill_logo: st.image("https://cdn-icons-png.flaticon.com/512/2920/2920323.png", width=60) # 3D Document
            with c_bill_title: st.subheader("Automatic Monthly Bill")
            
            df = st.session_state.expenses
            if not df.empty:
                df['Date_Obj'] = pd.to_datetime(df['Date'])
                df['Month_Year'] = df['Date_Obj'].dt.strftime('%B %Y')
                months = df['Month_Year'].unique()
                sel_month = st.selectbox("Select Month to Generate Bill", months)
                
                bill_data = df[df['Month_Year'] == sel_month]
                total_bill = bill_data['Amount'].sum()
                
                st.markdown(f"""
                <div class="bill-container">
                    <div class="bill-header">
                        <h2 style="color: #333; margin:0;">LUXORA MONTHLY STATEMENT</h2>
                        <p style="color: #777;">Client: {current_name} | Period: {sel_month}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.table(bill_data[['Date', 'Category', 'Note', 'Amount']])
                
                st.markdown(f"""
                    <div class="bill-total">
                        <h1 style="color: #007bff; margin:0;">TOTAL PAYABLE: ₹{total_bill}</h1>
                        <p style="font-size: 12px; color: gray;">Generated by Luxora AI System</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                csv = bill_data.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Bill (CSV)", csv, f"Bill_{sel_month}.csv", "text/csv")
            else:
                st.info("No data available.")

    # --- AI BRAIN ---
    elif menu == "AI Brain":
        # HEADER WITH 3D LOGO
        c_ai_logo, c_ai_title = st.columns([1, 6])
        with c_ai_logo: st.image("https://cdn-icons-png.flaticon.com/512/4712/4712027.png", width=80) # 3D Robot Head
        with c_ai_title: st.title("Gemini AI Brain")
        
        st.markdown("""<div style="background-color: #f0f9ff; padding: 15px; border-radius: 10px; border-left: 5px solid #00d2ff;"><strong>💡 Need Key?</strong> <a href="https://aistudio.google.com/app/apikey" target="_blank">👉 Click Here</a></div>""", unsafe_allow_html=True)
        key = st.text_input("Paste API Key", type="password")
        if key:
            prompt = st.chat_input("Ask...")
            if prompt:
                st.session_state.messages.append({"role": "user", "content": prompt})
                for m in st.session_state.messages:
                    with st.chat_message(m["role"]):
                        st.write(m["content"])
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=key)
                    model = genai.GenerativeModel('gemini-pro')
                    res = model.generate_content(prompt)
                    st.session_state.messages.append({"role": "assistant", "content": res.text})
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

if __name__ == "__main__":
    if st.session_state.logged_in_user is None: login_page()
    else: main_app()