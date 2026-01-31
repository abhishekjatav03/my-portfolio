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
    @keyframes gradient { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
    .stApp { background: linear-gradient(-45deg, #f3f4f6, #e0e7ff, #ffe4e6, #f0fdf4); background-size: 400% 400%; animation: gradient 15s ease infinite; }
    .glass-card { background: rgba(255,255,255,0.7); backdrop-filter: blur(10px); border-radius: 20px; border: 1px solid rgba(255,255,255,0.3); padding: 25px; box-shadow: 0 8px 32px 0 rgba(31,38,135,0.1); margin-bottom: 20px; }
    h1, h2, h3 { color: #1f2937; font-weight: 800; }
    .xp-card { background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%); color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px; }
    .stButton>button { background: linear-gradient(90deg, #111827, #374151); color: white; border-radius: 10px; font-weight: bold; border: none; }
    .best-deal { background: #dcfce7; border-left: 5px solid #22c55e; padding: 15px; border-radius: 10px; color: #14532d; }
    .high-risk { background: #fee2e2; border-left: 5px solid #ef4444; padding: 15px; border-radius: 10px; color: #7f1d1d; }
    .txn-badge { background: #e0f2fe; color: #0369a1; padding: 2px 8px; border-radius: 5px; font-size: 0.9em; font-family: monospace; border: 1px solid #7dd3fc; }
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
            st.error("⚠️ Secrets missing!"); st.stop()
        creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(st.secrets["gcp_service_account"]), scope)
        client = gspread.authorize(creds)
        return client.open("Luxora_DB")
    except Exception as e: st.error(f"DB Error: {e}"); st.stop()

def ensure_headers(ws, headers):
    try:
        if not ws.row_values(1): ws.append_row(headers)
    except: pass

def get_data(sheet_name):
    try:
        ws = connect_db().worksheet(sheet_name)
        if sheet_name == "Expenses": ensure_headers(ws, ["id", "date", "category", "amount", "user", "note"])
        elif sheet_name == "Loans": ensure_headers(ws, ["id", "date", "app_name", "amount", "interest_rate", "note"])
        elif sheet_name == "Jobs": ensure_headers(ws, ["id", "date", "name", "role", "salary"])
        return pd.DataFrame(ws.get_all_records())
    except: return pd.DataFrame()

def add_row(s, r): 
    try: connect_db().worksheet(s).append_row(r); return True
    except: return False

def delete_row_by_id(s, c, i):
    try: 
        ws = connect_db().worksheet(s)
        ws.delete_rows(ws.find(str(i)).row)
        return True
    except: return False

def update_cell_value(s, i, c, v):
    try:
        ws = connect_db().worksheet(s)
        ws.update_cell(ws.find(str(i)).row, c, v)
        return True
    except: return False

# ==========================================
# 3. AI ENGINE (SMART AUTO-CONNECT)
# ==========================================
class ProLearningAI:
    def __init__(self, api_key):
        self.active = False
        if api_key:
            genai.configure(api_key=api_key)
            self.active = True

    def get_lesson(self, topic):
        if not self.active: return "⚠️ API Key Missing!"
        
        prompt = f"Explain '{topic}' simply. Format: Definition, How it works, Fun Fact. Keep it short."
        
        # Try finding a working model automatically
        try:
            model = genai.GenerativeModel('gemini-pro') # Try Standard
            return model.generate_content(prompt).text
        except:
            try:
                model = genai.GenerativeModel('gemini-1.5-flash') # Try Flash
                return model.generate_content(prompt).text
            except Exception as e:
                return f"⚠️ AI Error: {e}. (Check API Key or Update requirements.txt)"

# ==========================================
# 4. MAIN APP
# ==========================================
if 'user' not in st.session_state: st.session_state.user = None
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'level' not in st.session_state: st.session_state.level = "🌱 Beginner"

def main_app():
    user = st.session_state.user
    with st.sidebar:
        st.markdown(f"<div class='xp-card'><h3>{st.session_state.level}</h3><h1>⭐ {st.session_state.xp} XP</h1></div>", unsafe_allow_html=True)
        st.write(f"👤 **{user['name']}**")
        
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            st.success(f"✅ AI Connected")
        except:
            api_key = st.text_input("🔑 Enter Key", type="password")

        options = ["DASHBOARD", "🧠 3D AI LAB", "💰 WALLET PRO 10.0", "✅ TASKS", "📓 NOTEBOOK", "📊 ATTENDANCE", "🤖 AI TUTOR"]
        if user['role'] == "Admin": options += ["💸 LOAN MANAGER", "🏢 STAFF JOBS"]
        options.append("🚪 LOGOUT")
        
        menu = st.radio("MENU", options)
        if menu == "🚪 LOGOUT": st.session_state.user = None; st.rerun()

    if menu == "DASHBOARD":
        st.markdown("<div class='glass-card'><h1>🚀 LIVE DASHBOARD</h1></div>", unsafe_allow_html=True)
        df = get_data("Expenses")
        my_df = df[df['user'] == user['username']] if not df.empty else pd.DataFrame()
        spent = my_df['amount'].sum() if not my_df.empty else 0
        c1, c2 = st.columns(2)
        c1.metric("TOTAL SPEND", f"₹{spent}")
        c2.metric("XP EARNED", st.session_state.xp)
        if not my_df.empty: st.plotly_chart(px.bar(my_df, x='category', y='amount', color='category'), use_container_width=True)

    elif menu == "🧠 3D AI LAB":
        st.markdown("<div class='glass-card'><h1>🧠 3D LEARNING ENGINE</h1></div>", unsafe_allow_html=True)
        topic = st.text_input("🔍 Search Topic (e.g. Heart, Engine)", placeholder="Type here...")
        if st.button("🚀 LAUNCH LIVE 3D"):
            if not topic: st.error("Type a topic!")
            else:
                with st.spinner("⚡ Finding best AI Model..."):
                    ai = ProLearningAI(api_key)
                    expl = ai.get_lesson(topic)
                    st.session_state.xp += 50
                    c1, c2 = st.columns([1, 1.5])
                    with c1: st.markdown(f"<div class='glass-card'><h3>📘 {topic.upper()}</h3>{expl}</div>", unsafe_allow_html=True)
                    with c2:
                        st.markdown("<div class='glass-card'><h3>🎥 LIVE 3D VIEW</h3>", unsafe_allow_html=True)
                        components.iframe(f"https://sketchfab.com/search?q={topic}&type=models", height=500, scrolling=True)

    elif menu == "💰 WALLET PRO 10.0":
        st.markdown("<div class='glass-card'><h1>💰 WALLET PRO 10.0</h1><p>SMART LUXURY EDITION</p></div>", unsafe_allow_html=True)
        t1, t2, t3, t4 = st.tabs(["➕ ADD", "🔍 MANAGE", "📊 REPORT", "🧾 BILL"])
        with t1:
            with st.form("add"):
                d = st.date_input("Date"); c = st.selectbox("Cat", ["Food","Travel","Fees","Other"])
                a = st.number_input("Amount", min_value=0); n = st.text_input("Note")
                if st.form_submit_button("SAVE"):
                    eid = f"TXN-{random.randint(1000,9999)}"
                    add_row("Expenses", [eid, str(d), c, a, user['username'], n])
                    st.success(f"Saved! ID: {eid}"); st.rerun()
        with t2:
            df = get_data("Expenses")
            if not df.empty:
                if user['role']!='Admin': df=df[df['user']==user['username']]
                st.write("📋 **Copy 'id' from below:**")
                st.dataframe(df, use_container_width=True)
                c1, c2 = st.columns(2)
                with c1:
                    did = st.text_input("Del ID")
                    if st.button("DEL"): delete_row_by_id("Expenses","id",did); st.rerun()
                with c2:
                    uid = st.text_input("Upd ID"); uamt = st.number_input("New Amt",0)
                    if st.button("UPD"): update_cell_value("Expenses",uid,4,uamt); st.rerun()
        with t3:
            df = get_data("Expenses")
            if not df.empty:
                st.plotly_chart(px.pie(df, values='amount', names='category'), use_container_width=True)
                st.download_button("📥 CSV", df.to_csv().encode('utf-8'), "data.csv")
        with t4:
            df = get_data("Expenses")
            if not df.empty:
                df['date'] = pd.to_datetime(df['date']); df['MY'] = df['date'].dt.strftime('%B %Y')
                sel = st.selectbox("Month", df['MY'].unique())
                bill = df[df['MY']==sel]
                st.markdown(f"<div class='bill-box'>Total: ₹{bill['amount'].sum()}</div>", unsafe_allow_html=True)
                st.table(bill[['date','category','amount']])

    elif menu == "💸 LOAN MANAGER":
        if user['role'] == "Admin":
            st.title("💸 BOSS LOAN MANAGER")
            t1, t2, t3 = st.tabs(["➕ ADD", "📊 REPORT", "🔍 MANAGE"])
            with t1:
                with st.form("ln"):
                    ld = st.date_input("Date"); la = st.text_input("App"); lam = st.number_input("Amt"); lr = st.number_input("Rate%")
                    if st.form_submit_button("SAVE"):
                        lid = f"LN-{random.randint(100,999)}"
                        add_row("Loans", [lid, str(ld), la, lam, lr, "Due"])
                        st.success(f"Saved! ID: {lid}")
            with t2:
                df = get_data("Loans")
                if not df.empty:
                    df['Amt'] = pd.to_numeric(df['amount']); df['Rate'] = pd.to_numeric(df['interest_rate'])
                    best = df.loc[df['Rate'].idxmin()]
                    st.markdown(f"<div class='best-deal'>🏆 Best: {best['app_name']} ({best['Rate']}%)</div>", unsafe_allow_html=True)
                    st.dataframe(df)
            with t3:
                st.dataframe(get_data("Loans"))
                did = st.text_input("Loan ID to Delete")
                if st.button("DELETE LOAN"): delete_row_by_id("Loans", "id", did); st.rerun()

    elif menu == "🏢 STAFF JOBS":
        if user['role'] == "Admin":
            st.title("🏢 STAFF JOBS")
            t1, t2 = st.tabs(["➕ ADD", "🔍 MANAGE"])
            with t1:
                with st.form("jb"):
                    jd = st.date_input("Date"); jn = st.text_input("Name"); jr = st.text_input("Role"); js = st.number_input("Salary")
                    if st.form_submit_button("SAVE"):
                        add_row("Jobs", [f"JOB-{random.randint(100,999)}", str(jd), jn, jr, js])
                        st.success("Saved!")
            with t2:
                st.dataframe(get_data("Jobs"))
                did = st.text_input("Job ID to Delete")
                if st.button("DELETE JOB"): delete_row_by_id("Jobs", "id", did); st.rerun()

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

    elif menu == "🤖 AI TUTOR":
        st.title("🤖 AI TUTOR")
        q = st.chat_input("Ask me...")
        if q:
            st.write(f"**You:** {q}")
            ai = ProLearningAI(api_key)
            st.write(f"**AI:** {ai.get_lesson(q)}")

# LOGIN PAGE
if not st.session_state.user:
    c1, c2, c3 = st.columns([1,1.5,1])
    with c2:
        st.markdown("<br><div class='glass-card' style='text-align:center;'><h1>💎 ABHISHEK LUXORA PRO 10.0</h1><p>INDORE EDITION</p></div>", unsafe_allow_html=True)
        u = st.text_input("User"); p = st.text_input("Pass", type="password")
        if st.button("LOGIN"):
            df = get_data("Users")
            if not df.empty:
                user = df[(df['username'].astype(str)==u) & (df['password'].astype(str)==p)]
                if not user.empty: st.session_state.user = user.iloc[0].to_dict(); st.rerun()
                else: st.error("Wrong Pass")
        
        nm = st.text_input("Name"); nu = st.text_input("New ID"); np = st.text_input("New Pass", type="password")
        if st.button("REGISTER"): add_row("Users", [nu, np, nm, "User"]); st.success("Registered!")
else:
    main_app()