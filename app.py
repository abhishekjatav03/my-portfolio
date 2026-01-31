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
# 1. LUXURY PRO SETUP & ANIMATION THEME
# ==========================================
st.set_page_config(page_title="💎 ABHISHEK LUXORA PRO 10.0 INDORE EDITION", page_icon="💎", layout="wide", initial_sidebar_state="expanded")

# --- 🌟 LIVE INDORE PRO THEME (CSS) ---
st.markdown("""
<style>
    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    .stApp {
        background: linear-gradient(-45deg, #f3f4f6, #e0e7ff, #ffe4e6, #f0fdf4);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    .glass-card:hover { transform: translateY(-5px); }
    
    h1, h2, h3 { color: #1f2937; font-weight: 800; font-family: 'Arial', sans-serif; }
    
    .xp-card {
        background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #111827, #374151);
        color: white;
        border-radius: 10px;
        font-weight: bold;
        border: none;
        padding: 10px 20px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .best-deal { background: #dcfce7; border-left: 5px solid #22c55e; padding: 15px; border-radius: 10px; color: #14532d; margin-bottom: 10px; }
    .high-risk { background: #fee2e2; border-left: 5px solid #ef4444; padding: 15px; border-radius: 10px; color: #7f1d1d; margin-bottom: 10px; }
    
    /* Input Fields Styling */
    .stTextInput>div>div>input { border-radius: 10px; border: 1px solid #ddd; }
    .stNumberInput>div>div>input { border-radius: 10px; }
    .stSelectbox>div>div>div { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATABASE FUNCTIONS
# ==========================================
@st.cache_resource
def connect_db():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        if "gcp_service_account" not in st.secrets:
            st.error("⚠️ Secrets missing!")
            st.stop()
        creds_dict = dict(st.secrets["gcp_service_account"])
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        return client.open("Luxora_DB")
    except Exception as e:
        st.error(f"⚠️ DB Error: {e}"); st.stop()

def ensure_headers(worksheet, headers):
    try:
        existing = worksheet.row_values(1)
        if not existing: 
            worksheet.append_row(headers)
    except: pass

def get_data(sheet_name):
    try:
        sh = connect_db()
        ws = sh.worksheet(sheet_name)
        # Defining Headers
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
class ProLearningAI:
    def __init__(self, api_key):
        self.active = False
        if api_key:
            try:
                self.api_key = api_key.strip()
                genai.configure(api_key=self.api_key)
                self.active = True
            except:
                self.active = False

    def get_lesson(self, topic):
        if not self.active: return "⚠️ Key Missing! Enter API Key in Sidebar."
        
        prompt = f"Explain '{topic}' simply for a student. Definition, How it works, Fun Fact."
        
        # Try Models in order: Newest -> Oldest
        models_to_try = ['gemini-1.5-flash', 'gemini-pro']
        
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                return response.text
            except Exception:
                continue 
        
        return "⚠️ AI Error: Could not connect to Google. Check API Key."

# ==========================================
# 4. LOGIN SYSTEM
# ==========================================
if 'user' not in st.session_state: st.session_state.user = None
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'level' not in st.session_state: st.session_state.level = "🌱 Beginner"

def login_page():
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("<br><div class='glass-card' style='text-align:center;'><h1>💎 ABHISHEK LUXORA PRO 10.0</h1><p>INDORE EDITION</p></div>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🔐 LOGIN", "📝 REGISTER"])
        with tab1:
            u = st.text_input("Username"); p = st.text_input("Password", type="password")
            if st.button("ENTER CLASSROOM", use_container_width=True):
                df = get_data("Users")
                if not df.empty:
                    df['username'] = df['username'].astype(str); df['password'] = df['password'].astype(str)
                    user = df[(df['username'] == u) & (df['password'] == p)]
                    if not user.empty:
                        st.session_state.user = user.iloc[0].to_dict()
                        st.success("Welcome!"); st.rerun()
                    else: st.error("Wrong Password")
        with tab2:
            nm = st.text_input("Name"); nu = st.text_input("New User ID"); np = st.text_input("New Password", type="password")
            if st.button("CREATE ACCOUNT", use_container_width=True):
                add_row("Users", [nu, np, nm, "User"]); st.success("Created! Login Now.")

# ==========================================
# 5. MAIN APP
# ==========================================
def main_app():
    user = st.session_state.user
    
    with st.sidebar:
        st.markdown(f"""
        <div class="xp-card">
            <h3>{st.session_state.level}</h3>
            <h1>⭐ {st.session_state.xp} XP</h1>
        </div>
        """, unsafe_allow_html=True)
        st.write(f"👤 **{user['name']}**")
        
        # Auto-Key Logic
        api_key = None
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
            st.success("✅ AI Connected")
        else:
            api_key = st.text_input("🔑 Enter Gemini Key", type="password")
        
        # MENU
        options = ["DASHBOARD", "🧠 3D AI LAB", "💰 WALLET PRO 10.0", "✅ TASKS", "📓 NOTEBOOK", "📊 ATTENDANCE"]
        
        if user['role'] == "Admin": 
            options.append("💸 LOAN MANAGER (BOSS)")
            options.append("🏢 STAFF JOBS PRO-2")
            options.append("👥 USER MANAGER")
            
        options.append("🚪 LOGOUT")
        
        menu = st.radio("MENU", options)
        if menu == "🚪 LOGOUT": st.session_state.user = None; st.rerun()

    # --- DASHBOARD ---
    if menu == "DASHBOARD":
        st.markdown("<div class='glass-card'><h1>🚀 LIVE DASHBOARD</h1></div>", unsafe_allow_html=True)
        df_exp = get_data("Expenses")
        my_exp = df_exp[df_exp['user'] == user['username']] if not df_exp.empty else pd.DataFrame()
        spent = my_exp['amount'].sum() if not my_exp.empty else 0
        c1, c2, c3 = st.columns(3)
        c1.metric("TOTAL SPEND", f"₹{spent}")
        c2.metric("XP", st.session_state.xp)
        if not my_exp.empty:
            st.plotly_chart(px.bar(my_exp, x='category', y='amount', color='category'), use_container_width=True)

    # --- 🧠 3D AI LAB ---
    elif menu == "🧠 3D AI LAB":
        st.markdown("<div class='glass-card'><h1>🧠 3D LEARNING ENGINE</h1></div>", unsafe_allow_html=True)
        topic = st.text_input("🔍 Search Topic (e.g. Heart, Engine)", placeholder="Type here...")
        if st.button("🚀 LAUNCH LIVE 3D"):
            if not topic: st.error("Type a topic!")
            else:
                with st.spinner("⚡ Finding AI Model..."):
                    ai = ProLearningAI(api_key)
                    expl = ai.get_lesson(topic)
                    
                    st.session_state.xp += 50
                    c1, c2 = st.columns([1, 1.5])
                    with c1: st.markdown(f"<div class='glass-card'><h3>📘 {topic.upper()}</h3>{expl}</div>", unsafe_allow_html=True)
                    with c2:
                        st.markdown("<div class='glass-card'><h3>🎥 LIVE 3D VIEW</h3>", unsafe_allow_html=True)
                        components.iframe(f"https://sketchfab.com/search?q={topic}&type=models", height=500, scrolling=True)

    # --- 💰 WALLET PRO ---
    elif menu == "💰 WALLET PRO 10.0":
        st.markdown("<div class='glass-card'><h1>💰 WALLET PRO 10.0</h1><p>Luxury Edition</p></div>", unsafe_allow_html=True)
        t1, t2, t3, t4 = st.tabs(["➕ SMART ADD", "🔍 MANAGE", "📊 REPORT", "🧾 AUTO BILL"])
        
        # TAB 1: ADD (ALL TEXT FIELDS)
        with t1:
            with st.form("add"):
                st.subheader("Add New Item")
                c1, c2 = st.columns(2)
                d = c1.date_input("Date")
                c = c2.text_input("Category (Type Here)", placeholder="e.g. Food, Travel")
                a = c1.number_input("Amount (₹)", min_value=0)
                n = c2.text_input("Note / Details", placeholder="Item Description")
                
                if st.form_submit_button("💾 SAVE ITEM"):
                    eid = f"TXN-{random.randint(1000,9999)}"
                    add_row("Expenses", [eid, str(d), c, a, user['username'], n])
                    st.success(f"Saved! ID: {eid}"); st.rerun()
        
        # TAB 2: MANAGE
        with t2:
            df = get_data("Expenses")
            if not df.empty:
                if user['role']!='Admin': df=df[df['user']==user['username']]
                st.dataframe(df, use_container_width=True)
                c1, c2 = st.columns(2)
                with c1: 
                    did = st.text_input("Del ID"); 
                    if st.button("DEL"): delete_row_by_id("Expenses","id",did); st.rerun()
                with c2:
                    uid = st.text_input("Upd ID"); uamt = st.number_input("New Amt",0)
                    if st.button("UPD"): update_cell_value("Expenses",uid,4,uamt); st.rerun()
        
        # TAB 3: REPORT
        with t3:
            df = get_data("Expenses")
            if not df.empty:
                st.plotly_chart(px.pie(df, values='amount', names='category', title="Category Wise", hole=0.4), use_container_width=True)
                st.download_button("📥 CSV", df.to_csv().encode('utf-8'), "data.csv")
        
        # TAB 4: AUTO BILL
        with t4:
            st.subheader("🧾 Automatic Bill Generator")
            df = get_data("Expenses")
            if not df.empty:
                df['date'] = pd.to_datetime(df['date']); df['MY'] = df['date'].dt.strftime('%B %Y')
                sel = st.selectbox("Select Month", df['MY'].unique())
                bill = df[df['MY']==sel]
                
                st.markdown(f"<div class='glass-card' style='text-align:center;'><h2>TOTAL BILL</h2><h1>₹{bill['amount'].sum():,.0f}</h1><p>{sel}</p></div>", unsafe_allow_html=True)
                st.table(bill[['date','category','amount','note']])

    # --- BOSS LOANS ---
    elif menu == "💸 LOAN MANAGER (BOSS)":
        if user['role'] == "Admin":
            st.title("💸 BOSS LOAN MANAGER")
            t1, t2, t3 = st.tabs(["➕ ADD", "📊 REPORT", "🔍 MANAGE"])
            with t1:
                with st.form("ln"):
                    ld = st.date_input("Date"); la = st.text_input("App"); lam = st.number_input("Amt"); lr = st.number_input("Rate%")
                    if st.form_submit_button("SAVE"):
                        add_row("Loans", [f"LN-{random.randint(100,999)}", str(ld), la, lam, lr, "Due"])
                        st.success("Saved!")
            with t2:
                df = get_data("Loans")
                if not df.empty:
                    df['Amt'] = pd.to_numeric(df['amount']); df['Rate'] = pd.to_numeric(df['interest_rate'])
                    st.dataframe(df)
            with t3:
                st.dataframe(get_data("Loans"))
                did = st.text_input("Loan ID to Delete")
                if st.button("DELETE LOAN"): delete_row_by_id("Loans", "id", did); st.rerun()

    # --- STAFF JOBS PRO-2 ---
    elif menu == "🏢 STAFF JOBS PRO-2":
        if user['role'] == "Admin":
            st.markdown("<div class='glass-card'><h1>🏢 STAFF JOBS PRO-2</h1></div>", unsafe_allow_html=True)
            t1, t2 = st.tabs(["➕ ADD JOB", "🔍 MANAGE"])
            
            with t1:
                with st.form("jb"):
                    c1, c2 = st.columns(2)
                    jd = c1.date_input("Date")
                    jn = c2.text_input("Staff Name")
                    jco = c1.text_input("Company Name")
                    jsf = c2.selectbox("Shift", ["Full Day", "Half Day", "Night Shift"])
                    js = st.number_input("Salary (₹)", min_value=0)
                    
                    if st.form_submit_button("💾 SAVE JOB RECORD"):
                        jid = f"JOB-{random.randint(1000,9999)}"
                        # Saving: ID, Date, Name, Company, Shift, Salary
                        add_row("Jobs", [jid, str(jd), jn, jco, jsf, js])
                        st.success(f"Job Added! ID: {jid}")

            with t2:
                st.dataframe(get_data("Jobs"), use_container_width=True)
                did = st.text_input("Job ID to Delete")
                if st.button("DELETE JOB"): delete_row_by_id("Jobs", "id", did); st.rerun()
        else: st.error("Access Denied")

    # --- 👥 USER MANAGER (BOSS ONLY) ---
    elif menu == "👥 USER MANAGER":
        if user['role'] == "Admin":
            st.markdown("<div class='glass-card'><h1>👥 REGISTERED USERS DATA</h1></div>", unsafe_allow_html=True)
            df_users = get_data("Users")
            if not df_users.empty:
                st.metric("Total Members", len(df_users))
                st.markdown("### 📋 User Database (Username & Passwords)")
                st.dataframe(df_users, use_container_width=True)
                csv_users = df_users.to_csv(index=False).encode('utf-8')
                st.download_button("📥 DOWNLOAD USER DATA", csv_users, "users_data.csv", "text/csv")
            else: st.info("No users found.")
        else: st.error("Access Denied")

    # --- OTHER FEATURES ---
    elif menu == "✅ TASKS":
        st.title("✅ TASKS")
        with st.form("tsk"):
            tt = st.text_input("Task"); td = st.date_input("Date")
            if st.form_submit_button("ADD"): add_row("Tasks", [str(td), tt, "Pending", user['username']]); st.success("Added!")
        df = get_data("Tasks")
        if not df.empty: 
            for i,r in df[df['user']==user['username']].iterrows(): st.write(f"✅ {r['task']}")

    elif menu == "📓 NOTEBOOK":
        st.title("📓 NOTES")
        with st.form("nt"):
            ns = st.text_input("Subject"); nc = st.text_area("Note")
            if st.form_submit_button("SAVE"): add_row("Notebook", [str(datetime.now().date()), ns, nc, user['username']]); st.success("Saved!")
        df = get_data("Notebook")
        if not df.empty:
            for i,r in df[df['user']==user['username']].iterrows():
                with st.expander(r['subject']): st.write(r['note'])

    elif menu == "📊 ATTENDANCE":
        st.title("📊 ATTENDANCE")
        with st.form("at"):
            asub = st.selectbox("Sub", ["Math","Phy"]); ast = st.radio("Status", ["Present","Absent"])
            if st.form_submit_button("MARK"): add_row("Attendance", [str(datetime.now().date()), asub, ast, user['username']]); st.success("Marked!")
        df = get_data("Attendance")
        if not df.empty: st.dataframe(df[df['user']==user['username']])

if __name__ == "__main__":
    if st.session_state.user: main_app()
    else: login_page()