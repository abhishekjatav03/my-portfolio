import streamlit as st
import pandas as pd
import plotly.express as px
import time
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import google.generativeai as genai
import streamlit.components.v1 as components
from datetime import datetime

# ==========================================
# 1. AMERICAN INDUSTRY LEVEL SETUP
# ==========================================
st.set_page_config(page_title="ABHISHEK LUXORA PRO 20.0", page_icon="💎", layout="wide", initial_sidebar_state="expanded")

# --- ENTERPRISE THEME CSS ---
st.markdown("""
<style>
    /* 3D Background Animation */
    @keyframes move {
        0% { background-position: 0 0; }
        100% { background-position: 40px 40px; }
    }
    .stApp {
        background-color: #f8f9fa;
        background-image: radial-gradient(#e5e7eb 1px, transparent 1px);
        background-size: 20px 20px;
        animation: move 4s linear infinite;
    }
    
    /* Typography */
    h1, h2, h3 { font-family: 'Segoe UI', sans-serif; color: #0f172a; font-weight: 700; }
    
    /* Metrics Cards */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        border-left: 5px solid #2563eb;
        text-align: center;
        transition: transform 0.2s;
    }
    .metric-card:hover { transform: translateY(-5px); }
    .metric-card h3 { margin: 0; color: #64748b; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; }
    .metric-card h2 { margin: 5px 0 0 0; color: #1e293b; font-size: 2rem; }

    /* Filmy Dashboard Specifics */
    .movie-card {
        background: #1e1e1e; /* Dark Cinema Background */
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        border: 1px solid #333;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: transform 0.2s;
    }
    .movie-card:hover { transform: scale(1.02); }
    .movie-rating {
        color: #f5c518; /* IMDb Yellow */
        font-weight: bold;
    }

    /* Buttons */
    .stButton>button {
        background: #1e293b;
        color: white;
        border-radius: 8px;
        padding: 0.6rem;
        border: none;
        font-weight: 600;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover { background: #334155; box-shadow: 0 8px 15px rgba(0,0,0,0.1); }

    /* Tables & Inputs */
    .stDataFrame { border-radius: 10px; overflow: hidden; border: 1px solid #e2e8f0; }
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. ROBUST DATABASE FUNCTIONS
# ==========================================
@st.cache_resource
def connect_db():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        if "gcp_service_account" not in st.secrets:
            st.error("⚠️ System Error: Credentials Missing.")
            st.stop()
        creds_dict = dict(st.secrets["gcp_service_account"])
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        return client.open("Luxora_DB")
    except Exception as e:
        st.error(f"⚠️ Database Connection Failed: {e}"); st.stop()

def ensure_headers(worksheet, headers):
    try:
        if not worksheet.row_values(1): worksheet.append_row(headers)
        elif worksheet.row_values(1)[0] != headers[0]: worksheet.insert_row(headers, index=1)
    except: pass

def get_data(sheet_name):
    try:
        sh = connect_db()
        ws = sh.worksheet(sheet_name)
        if sheet_name == "Expenses": ensure_headers(ws, ["id", "date", "category", "amount", "user", "note"])
        elif sheet_name == "Loans": ensure_headers(ws, ["id", "date", "app_name", "amount", "interest_rate", "note"])
        elif sheet_name == "Jobs": ensure_headers(ws, ["id", "date", "name", "company", "shift", "salary"])
        elif sheet_name == "Users": ensure_headers(ws, ["username", "password", "name", "role"])
        return pd.DataFrame(ws.get_all_records())
    except: return pd.DataFrame()

def add_row(sheet_name, row_data):
    try: connect_db().worksheet(sheet_name).append_row(row_data); return True
    except: return False

def delete_row_by_id(sheet_name, col_name, id_val):
    try:
        ws = connect_db().worksheet(sheet_name)
        cell = ws.find(str(id_val))
        ws.delete_rows(cell.row)
        return True
    except: return False

def update_cell_value(sheet_name, id_val, col_index, new_value):
    try:
        ws = connect_db().worksheet(sheet_name)
        cell = ws.find(str(id_val))
        ws.update_cell(cell.row, col_index, new_value)
        return True
    except: return False

# ==========================================
# 3. AI ENGINE
# ==========================================
class EnterpriseAI:
    def __init__(self, api_key):
        self.active = False
        if api_key:
            try:
                genai.configure(api_key=api_key.strip())
                self.active = True
            except: self.active = False

    def get_insight(self, prompt):
        if not self.active: return "⚠️ AI Services Unavailable."
        models = ['gemini-1.5-flash', 'gemini-pro']
        for m in models:
            try:
                model = genai.GenerativeModel(m)
                return model.generate_content(prompt).text
            except: continue
        return "⚠️ Service Error: AI models are currently unreachable."

# ==========================================
# 4. AUTHENTICATION
# ==========================================
if 'user' not in st.session_state: st.session_state.user = None
if 'xp' not in st.session_state: st.session_state.xp = 0

def login_system():
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: center; padding: 40px; background: white; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1);'>
            <h1 style='color: #0f172a;'>💎 ABHISHEK LUXORA PRO 20.0</h1>
            <p style='color: #64748b; margin-bottom: 30px;'>AMERICAN INDUSTRY EDITION</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔐 LOGIN", "📝 REGISTER"])
        
        with tab1:
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.button("SECURE LOGIN", use_container_width=True):
                df = get_data("Users")
                if not df.empty:
                    df[['username', 'password']] = df[['username', 'password']].astype(str)
                    user = df[(df['username'] == u) & (df['password'] == p)]
                    if not user.empty:
                        st.session_state.user = user.iloc[0].to_dict()
                        st.success("Access Granted."); st.rerun()
                    else: st.error("Invalid Credentials.")
        
        with tab2:
            nm = st.text_input("Full Name")
            nu = st.text_input("New Username")
            np = st.text_input("New Password", type="password")
            if st.button("CREATE ACCOUNT", use_container_width=True):
                if add_row("Users", [nu, np, nm, "User"]):
                    st.success("Account Created. Please Login."); st.rerun()

# ==========================================
# 5. CORE APPLICATION
# ==========================================
def main_app():
    user = st.session_state.user
    
    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align:center; padding: 20px 0;'>
            <div style='width: 70px; height: 70px; background: #2563eb; border-radius: 50%; margin: 0 auto 10px; display: flex; align-items: center; justify-content: center; color: white; font-size: 30px;'>💎</div>
            <h3 style='margin:0;'>{user['name']}</h3>
            <p style='color: #64748b; font-size: 0.9rem;'>{user['role']} Account</p>
        </div>
        """, unsafe_allow_html=True)
        
        api_key = st.secrets.get("GEMINI_API_KEY")
        if not api_key: api_key = st.text_input("🔑 API Key", type="password")
        
        st.markdown("---")
        options = ["DASHBOARD", "🎬 LIVE FILMY DASHBOARD", "🧠 3D AI LAB", "💰 WALLET PRO 20.0", "✅ TASKS", "📓 NOTEBOOK", "📊 ATTENDANCE"]
        if user['role'] == "Admin":
            options.extend(["💸 LOAN MANAGER (BOSS)", "🏢 STAFF JOBS PRO+5", "👥 USER MANAGER"])
        options.append("🚪 LOGOUT")
        
        menu = st.radio("NAVIGATION", options, label_visibility="collapsed")
        if menu == "🚪 LOGOUT": st.session_state.user = None; st.rerun()

    # --- DASHBOARD ---
    if menu == "DASHBOARD":
        st.title("🚀 Executive Dashboard")
        df_exp = get_data("Expenses")
        my_exp = df_exp[df_exp['user'] == user['username']] if not df_exp.empty else pd.DataFrame()
        total_spend = my_exp['amount'].sum() if not my_exp.empty else 0
        
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"<div class='metric-card'><h3>Total Spend</h3><h2>₹{total_spend:,.0f}</h2></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='metric-card'><h3>XP Earned</h3><h2>{st.session_state.xp}</h2></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='metric-card'><h3>Status</h3><h2>Active</h2></div>", unsafe_allow_html=True)
        
        st.markdown("### 📊 Financial Overview")
        if not my_exp.empty:
            st.plotly_chart(px.area(my_exp, x='date', y='amount', color='category'), use_container_width=True)

    # --- 🎬 LIVE FILMY DASHBOARD (SMART PRO++) ---
    elif menu == "🎬 LIVE FILMY DASHBOARD":
        st.title("🎬 Live Filmy Dashboard (Smart Pro++)")
        
        # Simulated Live Data
        st.markdown("""
        <div style='background-color: #000; color: #0f0; padding: 10px; font-family: monospace; white-space: nowrap; overflow: hidden;'>
            BREAKING NEWS: "Superstar's New Movie Breaks Records!" | "Upcoming Sci-Fi Thriller Trailer Released" | "Film Festival 2026 Dates Announced"
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("🔥 Trending Now")
            # Example Data - In a real app, this would come from an API
            movies = [
                {"title": "Galactic Wars: The Beginning", "rating": "9.2", "gross": "$1.2B"},
                {"title": "The Last Detective", "rating": "8.8", "gross": "$850M"},
                {"title": "Comedy of Errors 2", "rating": "7.5", "gross": "$400M"},
            ]
            
            for m in movies:
                st.markdown(f"""
                <div class='movie-card'>
                    <h3>{m['title']}</h3>
                    <p>Rating: <span class='movie-rating'>⭐ {m['rating']}</span> | Gross: {m['gross']}</p>
                </div>
                """, unsafe_allow_html=True)
                
            st.subheader("📽️ Box Office Analytics")
            box_office_data = pd.DataFrame({
                "Movie": ["Movie A", "Movie B", "Movie C", "Movie D"],
                "Collection (Cr)": [500, 350, 200, 150]
            })
            st.plotly_chart(px.bar(box_office_data, x='Movie', y='Collection (Cr)', title="Weekly Collections", color='Collection (Cr)'), use_container_width=True)

        with col2:
            st.subheader("🍿 Quick Search")
            m_search = st.text_input("Find Movie Details")
            if st.button("Search Movie"):
                if m_search:
                    st.info(f"Searching database for: {m_search}...")
                    time.sleep(1)
                    st.success("Movie Found! (Data would appear here)")
                else:
                    st.warning("Please enter a movie name.")
            
            st.subheader("📅 Upcoming Releases")
            st.write("- Action Hero (Feb 15)")
            st.write("- Love Story 2026 (Feb 22)")
            st.write("- Mystery House (Mar 01)")

    # --- 🧠 3D AI LAB ---
    elif menu == "🧠 3D AI LAB":
        st.title("🧠 3D Learning Engine")
        topic = st.text_input("Search Topic", placeholder="e.g. Heart, Engine...")
        if st.button("🚀 Launch Simulation"):
            if not topic: st.warning("Enter a topic.")
            else:
                with st.spinner("Initializing AI..."):
                    ai = EnterpriseAI(api_key)
                    insight = ai.get_insight(f"Explain '{topic}' simply. Definition, Mechanism, Fact.")
                    c1, c2 = st.columns([1, 1.5])
                    with c1: st.markdown(f"<div class='metric-card' style='text-align:left;'><h3>Insight</h3><p>{insight}</p></div>", unsafe_allow_html=True)
                    with c2:
                        st.markdown(f"<div class='metric-card'><h3>3D Visualization</h3></div>", unsafe_allow_html=True)
                        components.iframe(f"https://sketchfab.com/search?q={topic}&type=models", height=500, scrolling=True)

    # --- 💰 WALLET PRO 20.0 ---
    elif menu == "💰 WALLET PRO 20.0":
        st.title("💰 Wallet Pro 20.0 (Smart Excel Edition)")
        tab1, tab2, tab3, tab4 = st.tabs(["➕ SMART ADD", "🔍 UPDATE/DELETE", "📊 REPORT", "🧾 AUTO BILL"])
        
        with tab1:
            with st.form("w_add"):
                c1, c2 = st.columns(2)
                d = c1.date_input("Date")
                c = c2.text_input("Category", placeholder="e.g. Food")
                a = c1.number_input("Amount (₹)", min_value=0)
                n = c2.text_input("Note")
                if st.form_submit_button("SAVE"):
                    tid = f"TXN-{random.randint(10000,99999)}"
                    add_row("Expenses", [tid, str(d), c, a, user['username'], n])
                    st.success(f"Saved! ID: {tid}"); st.rerun()
        
        with tab2:
            df = get_data("Expenses")
            if not df.empty:
                if user['role'] != 'Admin': df = df[df['user'] == user['username']]
                st.dataframe(df, use_container_width=True)
                c1, c2 = st.columns(2)
                with c1:
                    did = st.text_input("Enter ID to Delete", key="w_del")
                    if st.button("DELETE ITEM", key="w_del_btn"): 
                        delete_row_by_id("Expenses", "id", did); st.rerun()
                with c2:
                    uid = st.text_input("Enter ID to Update", key="w_upd")
                    namt = st.number_input("New Amount", 0, key="w_amt")
                    if st.button("UPDATE AMOUNT", key="w_upd_btn"): 
                        update_cell_value("Expenses", uid, 4, namt); st.rerun()

        with tab3:
            df = get_data("Expenses")
            if not df.empty:
                c1, c2 = st.columns(2)
                with c1: st.plotly_chart(px.pie(df, values='amount', names='category', title="Breakdown"), use_container_width=True)
                with c2: st.plotly_chart(px.bar(df, x='category', y='amount', title="Trends"), use_container_width=True)

        with tab4:
            df = get_data("Expenses")
            if not df.empty:
                df['date'] = pd.to_datetime(df['date']); df['MY'] = df['date'].dt.strftime('%B %Y')
                sel = st.selectbox("Select Month", df['MY'].unique())
                bill = df[df['MY']==sel]
                st.markdown(f"<div class='metric-card'><h3>Total Bill</h3><h1>₹{bill['amount'].sum():,.0f}</h1></div>", unsafe_allow_html=True)
                st.table(bill[['date','category','amount','note']])

    # --- 💸 LOAN MANAGER ---
    elif menu == "💸 LOAN MANAGER (BOSS)":
        if user['role'] == "Admin":
            st.title("💸 Loan Manager (BOSS)")
            t1, t2, t3, t4 = st.tabs(["➕ SMART ADD", "🔍 UPDATE/DELETE", "📊 REPORT", "📉 AUTO LOAN"])
            
            with t1:
                with st.form("ln"):
                    c1, c2 = st.columns(2)
                    ld = c1.date_input("Date"); la = c2.text_input("App Name")
                    lam = c1.number_input("Amount", min_value=0); lr = c2.number_input("Rate %", min_value=0.0)
                    ln = st.text_input("Note")
                    if st.form_submit_button("RECORD LOAN"):
                        add_row("Loans", [f"LN-{random.randint(1000,9999)}", str(ld), la, lam, lr, ln])
                        st.success("Saved!")
            
            with t2:
                df = get_data("Loans")
                if not df.empty:
                    st.dataframe(df, use_container_width=True)
                    c1, c2 = st.columns(2)
                    with c1:
                        did = st.text_input("Loan ID to Delete", key="l_del")
                        if st.button("DELETE LOAN", key="l_del_btn"): 
                            delete_row_by_id("Loans", "id", did); st.rerun()
                    with c2:
                        uid = st.text_input("Loan ID to Update", key="l_upd")
                        namt = st.number_input("New Amount", 0, key="l_amt")
                        if st.button("UPDATE LOAN", key="l_upd_btn"):
                            update_cell_value("Loans", uid, 4, namt); st.rerun()

            with t3:
                df = get_data("Loans")
                if not df.empty:
                    df['amount'] = pd.to_numeric(df['amount'])
                    st.plotly_chart(px.bar(df, x='app_name', y='amount', title="Loan Portfolio"), use_container_width=True)

            with t4:
                st.subheader("📉 Auto Loan Analysis")
                df = get_data("Loans")
                if not df.empty:
                    df['amount'] = pd.to_numeric(df['amount'])
                    df['interest_rate'] = pd.to_numeric(df['interest_rate'])
                    df['Total Interest'] = df['amount'] * (df['interest_rate'] / 100)
                    df['Total Payable'] = df['amount'] + df['Total Interest']
                    
                    c1, c2 = st.columns(2)
                    c1.markdown(f"<div class='metric-card'><h3>Total Principal</h3><h2>₹{df['amount'].sum():,.0f}</h2></div>", unsafe_allow_html=True)
                    c2.markdown(f"<div class='metric-card'><h3>Total Payable (inc. Interest)</h3><h2 style='color:#dc2626'>₹{df['Total Payable'].sum():,.0f}</h2></div>", unsafe_allow_html=True)
                    st.dataframe(df[['app_name', 'amount', 'interest_rate', 'Total Interest', 'Total Payable']], use_container_width=True)

        else: st.error("Access Denied")

    # --- 🏢 STAFF JOBS PRO+5 ---
    elif menu == "🏢 STAFF JOBS PRO+5":
        if user['role'] == "Admin":
            st.title("🏢 Staff Jobs Pro+5")
            t1, t2, t3, t4 = st.tabs(["➕ SMART ADD", "🔍 UPDATE/DELETE", "📊 REPORT", "💵 AUTO SALARY"])
            
            with t1:
                with st.form("stf"):
                    c1, c2 = st.columns(2)
                    jd = c1.date_input("Join Date"); jn = c2.text_input("Name")
                    jc = c1.text_input("Company"); js = c2.selectbox("Shift", ["Full Day", "Half Day", "Night Shift"])
                    jam = st.number_input("Salary", min_value=0)
                    if st.form_submit_button("ADD RECORD"):
                        add_row("Jobs", [f"JB-{random.randint(1000,9999)}", str(jd), jn, jc, js, jam])
                        st.success("Added!")
            
            with t2:
                df = get_data("Jobs")
                if not df.empty:
                    st.dataframe(df, use_container_width=True)
                    c1, c2 = st.columns(2)
                    with c1:
                        did = st.text_input("Job ID to Delete", key="j_del")
                        if st.button("DELETE JOB", key="j_del_btn"): 
                            delete_row_by_id("Jobs", "id", did); st.rerun()
                    with c2:
                        uid = st.text_input("Job ID to Update Salary", key="j_upd")
                        nsal = st.number_input("New Salary", 0, key="j_sal")
                        if st.button("UPDATE SALARY", key="j_upd_btn"):
                            update_cell_value("Jobs", uid, 6, nsal); st.rerun() # Salary is col 6

            with t3:
                df = get_data("Jobs")
                if not df.empty:
                    if 'name' in df.columns and 'salary' in df.columns:
                        st.plotly_chart(px.bar(df, x='name', y='salary', color='shift', title="Salary Distribution"), use_container_width=True)

            with t4:
                st.subheader("💵 Auto Salary & Payroll")
                df = get_data("Jobs")
                if not df.empty:
                    df['salary'] = pd.to_numeric(df['salary'])
                    total_payroll = df['salary'].sum()
                    st.markdown(f"<div class='metric-card'><h3>Total Monthly Payroll</h3><h1 style='color:#16a34a'>₹{total_payroll:,.0f}</h1></div>", unsafe_allow_html=True)
                    st.table(df[['name', 'company', 'shift', 'salary']])

        else: st.error("Access Denied")

    # --- 👥 USER MANAGER ---
    elif menu == "👥 USER MANAGER":
        if user['role'] == "Admin":
            st.title("👥 User Management")
            df = get_data("Users")
            if not df.empty:
                st.metric("Total Users", len(df))
                st.dataframe(df, use_container_width=True)
                st.download_button("📥 Export CSV", df.to_csv(index=False).encode('utf-8'), "users.csv")
            else: st.info("No users.")
        else: st.error("Access Denied")

    # --- TASKS ---
    elif menu == "✅ TASKS":
        st.title("✅ Tasks")
        with st.form("tsk"):
            tn = st.text_input("Task"); td = st.date_input("Due")
            if st.form_submit_button("Add"): add_row("Tasks", [str(td), tn, "Pending", user['username']]); st.success("Added")
        df = get_data("Tasks")
        if not df.empty:
            for _, r in df[df['user']==user['username']].iterrows():
                st.markdown(f"<div class='metric-card' style='padding:10px; text-align:left;'>⬜ {r['task']}</div>", unsafe_allow_html=True)

    # --- NOTEBOOK ---
    elif menu == "📓 NOTEBOOK":
        st.title("📓 Notebook")
        with st.form("nb"):
            ns = st.text_input("Subject"); nc = st.text_area("Note")
            if st.form_submit_button("Save"): add_row("Notebook", [str(datetime.now().date()), ns, nc, user['username']]); st.success("Saved")
        df = get_data("Notebook")
        if not df.empty:
            for _, r in df[df['user']==user['username']].iterrows():
                with st.expander(r['subject']): st.write(r['note'])

    # --- ATTENDANCE ---
    elif menu == "📊 ATTENDANCE":
        st.title("📊 Attendance")
        with st.form("att"):
            asub = st.text_input("Subject/Event"); ast = st.radio("Status", ["Present","Absent"])
            if st.form_submit_button("Mark"): add_row("Attendance", [str(datetime.now().date()), asub, ast, user['username']]); st.success("Marked")
        df = get_data("Attendance")
        if not df.empty: st.dataframe(df[df['user']==user['username']])

if __name__ == "__main__":
    if st.session_state.user: main_app()
    else: login_system()