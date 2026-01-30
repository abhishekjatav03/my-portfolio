import streamlit as st
import pandas as pd
import plotly.express as px
import time
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import google.generativeai as genai

# ==========================================
# 1. GOOGLE SHEETS CONNECTION
# ==========================================
def connect_db():
    try:
        # Define Scope
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        # Load Credentials from Streamlit Secrets
        # Setup: Streamlit Cloud Dashboard > App > Settings > Secrets
        creds_dict = dict(st.secrets["gcp_service_account"])
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        
        # Open the Sheet
        sheet = client.open("Luxora_DB") # Sheet ka naam EXACT same hona chahiye
        return sheet
    except Exception as e:
        st.error("⚠️ Database Connection Failed! Please check Streamlit Secrets.")
        st.stop()

# --- HELPER FUNCTIONS ---

def get_data(sheet_name):
    """Sheet se data padhkar DataFrame banata hai"""
    try:
        sh = connect_db()
        worksheet = sh.worksheet(sheet_name)
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        # Empty rows handle karna
        return df if not df.empty else pd.DataFrame()
    except:
        return pd.DataFrame()

def add_row(sheet_name, row_data):
    """Nayi line add karta hai"""
    sh = connect_db()
    worksheet = sh.worksheet(sheet_name)
    worksheet.append_row(row_data)

def delete_row_by_id(sheet_name, col_name, id_val):
    """ID dhundh kar row delete karta hai (Cloud operation)"""
    sh = connect_db()
    worksheet = sh.worksheet(sheet_name)
    try:
        cell = worksheet.find(str(id_val))
        worksheet.delete_rows(cell.row)
        return True
    except:
        return False

def update_row_by_id(sheet_name, id_val, new_amount, new_note):
    """ID dhundh kar update karta hai"""
    sh = connect_db()
    worksheet = sh.worksheet(sheet_name)
    try:
        cell = worksheet.find(str(id_val))
        # Amount aur Note update (Assuming columns layout: id, date, category, amount, user, note)
        # Amount is Col 4, Note is Col 6 (A=1, B=2...)
        worksheet.update_cell(cell.row, 4, new_amount) 
        worksheet.update_cell(cell.row, 6, new_note)
        return True
    except:
        return False

# ==========================================
# 2. APP CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="ABHI Luxora Cloud",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# WHITE & GOLD THEME
st.markdown("""
<style>
    .stApp { background-color: #ffffff; background-image: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%); color: #333333; }
    .glass-card { background: rgba(255, 255, 255, 0.9); border: 1px solid rgba(212, 175, 55, 0.3); border-radius: 16px; padding: 25px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); }
    h1, h2, h3 { background: linear-gradient(45deg, #b8860b, #d4af37, #daa520); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800 !important; }
    .stTextInput>div>div>input, .stNumberInput>div>div>input { border: 1px solid #d4af37 !important; border-radius: 8px; }
    .stButton>button { background: linear-gradient(90deg, #d4af37, #f1c40f); color: white; border: none; padding: 10px 20px; font-weight: bold; border-radius: 8px; }
    .bill-box { border: 2px dashed #d4af37; padding: 20px; background: #fff; text-align: center; border-radius: 10px; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SESSION STATE
# ==========================================
if 'user' not in st.session_state:
    st.session_state.user = None

# ==========================================
# 4. LOGIN SYSTEM
# ==========================================
def login_page():
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""<div class="glass-card" style="text-align:center;"><h1 style="font-size: 35px;">ABHI LUXORA CLOUD</h1><p style="color: #666;">GOOGLE SHEETS EDITION</p></div>""", unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["LOGIN", "REGISTER"])
        
        with tab1:
            username = st.text_input("Username", key="l_user")
            password = st.text_input("Password", type="password", key="l_pass")
            if st.button("ENTER CLASSROOM", use_container_width=True):
                with st.spinner("Connecting to Google Cloud..."):
                    df = get_data("Users")
                    if not df.empty:
                        # Convert to string for safe comparison
                        df['username'] = df['username'].astype(str)
                        df['password'] = df['password'].astype(str)
                        
                        user = df[(df['username'] == username) & (df['password'] == password)]
                        
                        if not user.empty:
                            u_data = user.iloc[0]
                            st.session_state.user = {"username": u_data['username'], "name": u_data['name'], "role": u_data['role']}
                            st.success(f"Welcome, {u_data['name']}")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Invalid ID or Password.")
                    else:
                        st.error("Database Empty or Connection Failed.")

        with tab2:
            new_name = st.text_input("Student Name")
            new_user = st.text_input("Create User ID")
            new_pass = st.text_input("Create Password", type="password")
            if st.button("JOIN LUXORA", use_container_width=True):
                with st.spinner("Saving to Cloud..."):
                    df = get_data("Users")
                    if not df.empty and str(new_user) in df['username'].astype(str).values:
                        st.error("Username Taken!")
                    else:
                        add_row("Users", [new_user, new_pass, new_name, "User"])
                        st.success("Account Created! Login Now.")

# ==========================================
# 5. MAIN APP
# ==========================================
def main_app():
    user = st.session_state.user
    
    with st.sidebar:
        badge = "👑 BOSS" if user['role'] == "Admin" else "🎓 STUDENT"
        st.markdown(f"""
        <div style="text-align: center; padding: 20px;">
            <h3 style="margin-top: 10px; color: #333;">{user['name']}</h3>
            <p style="color: #666;">ID: {user['username']}</p>
            <div style="background: #333; color: white; padding: 5px 15px; border-radius: 20px; display: inline-block;">{badge}</div>
        </div>
        """, unsafe_allow_html=True)
        
        options = ["DASHBOARD", "WALLET", "AI HELP"]
        if user['role'] == "Admin": options.append("🏢 STAFF JOBS")
        options.append("LOGOUT")
        
        menu = st.radio("MENU", options, label_visibility="collapsed")
        if menu == "LOGOUT":
            st.session_state.user = None
            st.rerun()

    # --- DASHBOARD ---
    if menu == "DASHBOARD":
        st.title("DASHBOARD (LIVE CLOUD DATA)")
        
        # Load Data
        df = get_data("Expenses")
        
        # Filter Logic
        if user['role'] != "Admin" and not df.empty:
            df = df[df['user'] == user['name']]
            
        total_spent = df['amount'].sum() if not df.empty else 0
        
        if user['role'] == "Admin":
            users_df = get_data("Users")
            # Count only Users (not Admin)
            if not users_df.empty:
                total_students = len(users_df[users_df['role'] == 'User'])
            else:
                total_students = 0
                
            c1, c2, c3 = st.columns(3)
            c1.metric("TOTAL STUDENTS", total_students)
            c2.metric("TOTAL SPEND", f"₹{total_spent:,.0f}")
            c3.metric("BOSS MODE", "ON")
            
            st.markdown("### 📋 REGISTERED STUDENTS")
            if not users_df.empty:
                st.dataframe(users_df[users_df['role'] == 'User'], use_container_width=True)
                
        else:
            c1, c2 = st.columns(2)
            c1.metric("TOTAL SPENT", f"₹{total_spent:,.0f}")
            c2.metric("TRANSACTIONS", len(df))
            
            if not df.empty:
                fig = px.bar(df, x='category', y='amount', color='category')
                st.plotly_chart(fig, use_container_width=True)

    # --- WALLET ---
    elif menu == "WALLET":
        st.title("STUDENT WALLET 💳")
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["➕ DAILY ENTRY", "🔍 MANAGE", "📊 SMART REPORT", "🧾 BILL", "📈 ANALYSIS"])
        
        with tab1:
            st.subheader("Add Expense to Sheet")
            with st.form("add_exp"):
                c1, c2 = st.columns(2)
                dt = c1.date_input("Date")
                cat = c2.selectbox("Category", ["Canteen/Food", "Books", "Recharge", "Travel", "Fees", "Other"])
                amt = c1.number_input("Amount (₹)", min_value=0)
                nt = c2.text_input("Item Name / Note")
                
                if st.form_submit_button("SAVE TO CLOUD"):
                    eid = f"TXN-{random.randint(1000,9999)}"
                    with st.spinner("Syncing..."):
                        add_row("Expenses", [eid, str(dt), cat, amt, user['name'], nt])
                        st.success(f"Saved! ID: {eid}")
                        time.sleep(1); st.rerun()

        with tab2:
            st.subheader("Update/Delete (Cloud)")
            search = st.text_input("Transaction ID (e.g. TXN-1234)")
            if search:
                # Direct deletion requires logic, simplified here
                c1, c2 = st.columns(2)
                with c1:
                    u_amt = st.number_input("New Amount")
                    u_note = st.text_input("New Note")
                    if st.button("UPDATE CLOUD"):
                        if update_row_by_id("Expenses", search, u_amt, u_note):
                            st.success("Updated!")
                        else:
                            st.error("ID Not Found")
                with c2:
                    st.write("")
                    st.write("")
                    if st.button("DELETE FROM SHEET"):
                        if delete_row_by_id("Expenses", "id", search):
                            st.warning("Deleted!")
                        else:
                            st.error("ID Not Found")

        with tab3:
            st.subheader("Live Google Sheet View")
            df = get_data("Expenses")
            if user['role'] != "Admin" and not df.empty:
                df = df[df['user'] == user['name']]
            st.dataframe(df, use_container_width=True)

        with tab4:
            st.subheader("Monthly Bill")
            df = get_data("Expenses")
            if user['role'] != "Admin" and not df.empty: df = df[df['user'] == user['name']]
            
            if not df.empty:
                df['date'] = pd.to_datetime(df['date'])
                df['Month'] = df['date'].dt.strftime('%B %Y')
                sel_month = st.selectbox("Select Month", df['Month'].unique())
                bill_df = df[df['Month'] == sel_month]
                st.markdown(f"<div class='bill-box'><h2>TOTAL: ₹{bill_df['amount'].sum():,.2f}</h2></div>", unsafe_allow_html=True)
                st.table(bill_df[['date', 'category', 'amount']])

        with tab5:
            df = get_data("Expenses")
            if user['role'] != "Admin" and not df.empty: df = df[df['user'] == user['name']]
            if not df.empty:
                fig = px.pie(df, values='amount', names='category')
                st.plotly_chart(fig, use_container_width=True)

    # --- STAFF JOBS (BOSS ONLY) ---
    elif menu == "🏢 STAFF JOBS":
        st.title("🏢 STAFF JOB MANAGEMENT")
        tab1, tab2 = st.tabs(["➕ ADD JOB", "📑 VIEW REPORT"])
        
        with tab1:
            with st.form("job_form"):
                c1, c2 = st.columns(2)
                j_date = c1.date_input("Job Date")
                j_staff = c2.text_input("Staff Name")
                j_comp = c1.text_input("Company Name")
                j_type = c2.selectbox("Work Type", ["Full Day", "Half Day", "Overtime"])
                j_salary = st.number_input("Salary (₹)", min_value=0)
                
                if st.form_submit_button("SAVE RECORD"):
                    with st.spinner("Saving..."):
                        add_row("Jobs", [str(j_date), j_staff, j_comp, j_type, j_salary])
                        st.success("Saved to Google Sheet!")
        
        with tab2:
            df_jobs = get_data("Jobs")
            st.dataframe(df_jobs, use_container_width=True)
            if not df_jobs.empty:
                csv = df_jobs.to_csv(index=False).encode('utf-8')
                st.download_button("DOWNLOAD REPORT", csv, "jobs.csv", "text/csv")

    # --- AI HELP ---
    elif menu == "AI HELP":
        st.title("AI STUDY PARTNER 🤖")
        # Google Sheets version mein hum API Key input mangenge
        key = st.text_input("Enter Gemini API Key", type="password")
        if key:
            genai.configure(api_key=key)
            model = genai.GenerativeModel('gemini-pro')
            if "messages" not in st.session_state: st.session_state.messages = []
            for m in st.session_state.messages:
                with st.chat_message(m["role"]): st.write(m["content"])
            prompt = st.chat_input("Ask me...")
            if prompt:
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.chat_message("user").write(prompt)
                res = model.generate_content(prompt)
                st.session_state.messages.append({"role": "assistant", "content": res.text})
                st.chat_message("assistant").write(res.text)

if __name__ == "__main__":
    if st.session_state.user:
        main_app()
    else:
        login_page()