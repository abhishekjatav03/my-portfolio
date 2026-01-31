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
    }
    h1, h2, h3 { color: #1f2937; font-weight: 800; }
    .xp-card {
        background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #111827, #374151);
        color: white;
        border-radius: 10px;
        font-weight: bold;
        border: none;
    }
    .best-deal { background: #dcfce7; border-left: 5px solid #22c55e; padding: 15px; border-radius: 10px; color: #14532d; }
    .high-risk { background: #fee2e2; border-left: 5px solid #ef4444; padding: 15px; border-radius: 10px; color: #7f1d1d; }
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
            st.error("⚠️ Secrets not found!")
            st.stop()
        creds_dict = dict(st.secrets["gcp_service_account"])
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        return client.open("Luxora_DB")
    except Exception as e:
        st.error(f"⚠️ DB Error: {e}"); st.stop()

def get_data(sheet_name):
    try: return pd.DataFrame(connect_db().worksheet(sheet_name).get_all_records())
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
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.active = True
        else: self.active = False

    def get_lesson(self, topic):
        if not self.active: return "⚠️ API Key Missing!"
        prompt = f"Explain '{topic}' simply. Format: Definition, How it works, Fun Fact. Keep it short."
        try: return self.model.generate_content(prompt).text
        except: return "⚠️ AI Error."

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
        
        # --- FIXED AUTO-KEY INDENTATION ---
        try:
            if "GEMINI_API_KEY" in st.secrets:
                api_key = st.secrets["GEMINI_API_KEY"]
                st.success("✅ AI Key Linked")
            else:
                api_key = st.text_input("🔑 Enter Gemini Key", type="password")
        except:
            api_key = st.text_input("🔑 Enter Gemini Key", type="password")
        
        # MENU
        options = ["DASHBOARD", "🧠 3D AI LAB", "💰 WALLET PRO 10.0", "✅ TASKS", "📓 NOTEBOOK", "📊 ATTENDANCE", "🤖 AI TUTOR"]
        if user['role'] == "Admin": 
            options.append("💸 LOAN MANAGER (BOSS)")
            options.append("🏢 STAFF JOBS PRO")
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
        c2.metric("LEVEL", st.session_state.level)
        c3.metric("XP", st.session_state.xp)
        
        if not my_exp.empty:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.plotly_chart(px.bar(my_exp, x='category', y='amount', color='category', title="Live Spending Tracker"), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # --- 💸 LOAN MANAGER (BOSS) ---
    elif menu == "💸 LOAN MANAGER (BOSS)":
        if user['role'] == "Admin":
            st.markdown("<div class='glass-card'><h1>💸 BOSS LOAN COMMAND CENTER</h1></div>", unsafe_allow_html=True)
            tab1, tab2, tab3 = st.tabs(["➕ ADD LOAN", "📉 INTELLIGENT REPORT", "🔍 MANAGE LOANS"])
            
            with tab1:
                with st.form("loan_form"):
                    c1, c2 = st.columns(2)
                    l_date = c1.date_input("Loan Date")
                    l_app = c2.text_input("App Name (e.g. Cred)")
                    l_amt = c1.number_input("Amount (₹)", min_value=0)
                    l_rate = c2.number_input("Interest Rate (%)", min_value=0.0, step=0.1)
                    l_note = st.text_input("Note / Deadline")
                    if st.form_submit_button("SAVE RECORD"):
                        lid = f"LN-{random.randint(1000,9999)}"
                        add_row("Loans", [lid, str(l_date), l_app, l_amt, l_rate, l_note])
                        st.success(f"Loan Added! ID: {lid}")

            with tab2:
                df_loan = get_data("Loans")
                if not df_loan.empty:
                    df_loan['amount'] = pd.to_numeric(df_loan['amount'], errors='coerce')
                    df_loan['interest_rate'] = pd.to_numeric(df_loan['interest_rate'], errors='coerce')
                    df_loan['Total_Interest'] = df_loan['amount'] * (df_loan['interest_rate'] / 100)
                    df_loan['Total_Payable'] = df_loan['amount'] + df_loan['Total_Interest']
                    
                    min_idx = df_loan['interest_rate'].idxmin(); best_app = df_loan.loc[min_idx]
                    st.markdown(f"<div class='best-deal'>🏆 <b>BEST DEAL:</b> {best_app['app_name']} ({best_app['interest_rate']}%)</div>", unsafe_allow_html=True)
                    
                    c1, c2 = st.columns(2)
                    c1.metric("Total Debt", f"₹{df_loan['amount'].sum():,.0f}")
                    c2.metric("Total Interest", f"₹{df_loan['Total_Interest'].sum():,.0f}")
                    st.plotly_chart(px.bar(df_loan, x='app_name', y=['amount', 'Total_Interest'], barmode='group'), use_container_width=True)
                    
                    csv = df_loan.to_csv(index=False).encode('utf-8')
                    st.download_button("📥 DOWNLOAD SMART REPORT", csv, "loan_report.csv", "text/csv")
                else: st.info("No loans found.")

            with tab3:
                lid = st.text_input("Enter Loan ID (LN-....)")
                if lid:
                    c1, c2 = st.columns(2)
                    with c1:
                        u_amt = st.number_input("New Amount", min_value=0)
                        if st.button("UPDATE AMOUNT"):
                            if update_cell_value("Loans", lid, 4, u_amt): st.success("Updated!"); st.rerun()
                    with c2:
                        if st.button("DELETE LOAN"):
                            if delete_row_by_id("Loans", "id", lid): st.warning("Deleted!"); st.rerun()
                st.dataframe(get_data("Loans"), use_container_width=True)
        else: st.error("Access Denied")

    # --- 🏢 STAFF JOBS PRO ---
    elif menu == "🏢 STAFF JOBS PRO":
        if user['role'] == "Admin":
            st.markdown("<div class='glass-card'><h1>🏢 STAFF MANAGEMENT PRO</h1></div>", unsafe_allow_html=True)
            tab1, tab2, tab3 = st.tabs(["➕ ADD JOB", "🔍 UPDATE/DELETE", "📊 SMART REPORTS"])
            
            # TAB 1: ADD
            with tab1:
                with st.form("job_form"):
                    c1, c2 = st.columns(2)
                    jd = c1.date_input("Date")
                    js = c2.text_input("Staff Name")
                    jr = c1.text_input("Role / Work Type")
                    jsal = c2.number_input("Salary (₹)", min_value=0)
                    if st.form_submit_button("SAVE JOB"):
                        jid = f"JOB-{random.randint(1000,9999)}"
                        add_row("Jobs", [jid, str(jd), js, jr, jsal])
                        st.success(f"Job Added! ID: {jid}")

            with tab2:
                st.subheader("Manage Staff Records")
                search_jid = st.text_input("Enter Job ID (JOB-....)")
                if search_jid:
                    col1, col2 = st.columns(2)
                    with col1:
                        new_sal = st.number_input("Update Salary", min_value=0)
                        if st.button("UPDATE SALARY"):
                            if update_cell_value("Jobs", search_jid, 5, new_sal): st.success("Salary Updated!"); st.rerun()
                            else: st.error("ID Not Found")
                    with col2:
                        if st.button("DELETE JOB RECORD"):
                            if delete_row_by_id("Jobs", "id", search_jid): st.warning("Deleted Successfully!"); st.rerun()
                            else: st.error("ID Not Found")
                st.dataframe(get_data("Jobs"), use_container_width=True)

            with tab3:
                st.subheader("📊 Staff Payroll Report")
                df_jobs = get_data("Jobs")
                if not df_jobs.empty:
                    df_jobs['salary'] = pd.to_numeric(df_jobs['salary'], errors='coerce')
                    total_payroll = df_jobs['salary'].sum()
                    st.markdown(f"<div class='bill-box'><h3>Total Payroll</h3><h1>₹{total_payroll:,.0f}</h1></div>", unsafe_allow_html=True)
                    st.plotly_chart(px.pie(df_jobs, values='salary', names='name', title="Salary Distribution"), use_container_width=True)
                    csv_jobs = df_jobs.to_csv(index=False).encode('utf-8')
                    st.download_button("📥 DOWNLOAD EXCEL REPORT", csv_jobs, "staff_report.csv", "text/csv")
                else: st.info("No records found.")
        else: st.error("Access Denied")

    # --- 🧠 3D AI LAB (LIVE) ---
    elif menu == "🧠 3D AI LAB":
        st.markdown("<div class='glass-card'><h1>🧠 3D LEARNING ENGINE</h1></div>", unsafe_allow_html=True)
        topic = st.text_input("🔍 Search Anything (Heart, Engine, Pyramids)", placeholder="Type here...")
        if st.button("🚀 LAUNCH LIVE 3D"):
            if not topic or not api_key: st.error("Topic or Key missing!")
            else:
                with st.spinner("⚡ Connecting to 3D Server..."):
                    ai = ProLearningAI(api_key)
                    expl = ai.get_lesson(topic)
                    
                    if "⚠️" in expl: st.error(expl)
                    else:
                        st.session_state.xp += 50
                        c1, c2 = st.columns([1, 1.5])
                        with c1: st.markdown(f"<div class='glass-card'><h3>📘 {topic.upper()}</h3>{expl}</div>", unsafe_allow_html=True); st.success("+50 XP!")
                        with c2:
                            st.markdown("<div class='glass-card'><h3>🎥 LIVE 3D VIEW</h3>", unsafe_allow_html=True)
                            components.iframe(src=f"https://sketchfab.com/search?q={topic}&type=models", height=500, scrolling=True)
                            st.markdown("</div>", unsafe_allow_html=True)

    # --- 💰 WALLET PRO 10.0 (LUXURY EDITION) ---
    elif menu == "💰 WALLET PRO 10.0":
        st.markdown("<div class='glass-card'><h1>💰 WALLET PRO 10.0</h1><p>SMART LUXURY EDITION</p></div>", unsafe_allow_html=True)
        tab1, tab2, tab3, tab4 = st.tabs(["➕ SMART ADD", "🔍 MANAGE & DELETE", "📊 PRO ANALYSIS", "🧾 AUTO BILL"])
        
        with tab1:
            with st.form("add_exp"):
                c1, c2 = st.columns(2)
                d = c1.date_input("Date")
                cat = c2.selectbox("Select Category", ["Food", "Travel", "Fees", "Books", "Recharge", "Shopping", "Other"])
                a = c1.number_input("Amount (₹)", min_value=0)
                n = c2.text_input("Item Name / Note")
                if st.form_submit_button("💾 SAVE TRANSACTION"):
                    eid = f"TXN-{random.randint(1000,9999)}"
                    add_row("Expenses", [eid, str(d), cat, a, user['username'], n])
                    st.success(f"Saved! Transaction ID: {eid}"); time.sleep(1); st.rerun()

        with tab2:
            st.subheader("Manage Transactions")
            df = get_data("Expenses")
            if not df.empty:
                if user['role'] != 'Admin': df = df[df['user'] == user['username']]
                st.write("📋 **Your Transactions:** (Copy ID to Delete/Update)")
                st.dataframe(df, use_container_width=True)
                st.write("---")
                c1, c2 = st.columns(2)
                with c1:
                    del_id = st.text_input("Enter TXN ID to Delete")
                    if st.button("DELETE"): 
                        if delete_row_by_id("Expenses", "id", del_id): st.warning("Deleted!"); st.rerun()
                with c2:
                    up_id = st.text_input("Enter TXN ID to Update")
                    n_amt = st.number_input("New Amount", min_value=0)
                    if st.button("UPDATE"):
                        if update_cell_value("Expenses", up_id, 4, n_amt): st.success("Updated!"); st.rerun()
            else: st.info("No transactions found.")

        with tab3:
            df = get_data("Expenses")
            if not df.empty:
                if user['role'] != 'Admin': df = df[df['user'] == user['username']]
                c1, c2 = st.columns(2)
                with c1: st.plotly_chart(px.pie(df, values='amount', names='category', title="Category Breakdown", hole=0.4), use_container_width=True)
                with c2: st.plotly_chart(px.bar(df, x='date', y='amount', title="Daily Spend Trend"), use_container_width=True)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 DOWNLOAD REPORT", csv, "wallet.csv", "text/csv")
            else: st.info("No data.")

        with tab4:
            df = get_data("Expenses")
            if not df.empty:
                if user['role'] != 'Admin': df = df[df['user'] == user['username']]
                df['date'] = pd.to_datetime(df['date']); df['MY'] = df['date'].dt.strftime('%B %Y')
                sel = st.selectbox("Select Month", df['MY'].unique())
                bill = df[df['MY'] == sel]
                st.markdown(f"<div class='bill-box'><h3>Total Bill: ₹{bill['amount'].sum():,.0f}</h3></div>", unsafe_allow_html=True)
                st.table(bill[['date','category','amount','note']])
            else: st.info("No data.")

    # --- TASKS ---
    elif menu == "✅ TASKS":
        st.title("✅ TO-DO LIST")
        c1, c2 = st.columns([1, 2])
        with c1:
            with st.form("task_f"):
                td = st.date_input("Deadline"); tt = st.text_input("Task")
                if st.form_submit_button("ADD"):
                    add_row("Tasks", [str(td), tt, "Pending", user['username']]); st.success("Added!"); st.rerun()
        with c2:
            df = get_data("Tasks")
            if not df.empty:
                for i, row in df[df['user'] == user['username']].iterrows():
                    st.markdown(f"<div style='border-left:5px solid green; padding:10px; background:rgba(255,255,255,0.6); margin:5px; border-radius:5px;'><b>{row['task']}</b></div>", unsafe_allow_html=True)

    # --- NOTEBOOK ---
    elif menu == "📓 NOTEBOOK":
        st.title("📓 NOTES")
        with st.form("note_f"):
            s = st.text_input("Subject"); c = st.text_area("Content")
            if st.form_submit_button("SAVE"): add_row("Notebook", [str(datetime.now().date()), s, c, user['username']]); st.success("Saved!")
        df = get_data("Notebook")
        if not df.empty:
            for i, row in df[df['user'] == user['username']].iterrows():
                with st.expander(f"📌 {row['subject']}"): st.write(row['note'])

    # --- ATTENDANCE ---
    elif menu == "📊 ATTENDANCE":
        st.title("📊 ATTENDANCE")
        with st.form("att_f"):
            s = st.selectbox("Sub", ["Math","Phy","CS"]); stt = st.radio("Status", ["Present","Absent"])
            if st.form_submit_button("MARK"): add_row("Attendance", [str(datetime.now().date()), s, stt, user['username']]); st.success("Marked!")
        df = get_data("Attendance")
        if not df.empty: st.dataframe(df[df['user'] == user['username']])

    # --- AI TUTOR ---
    elif menu == "🤖 AI TUTOR":
        st.title("🤖 CHAT WITH AI")
        if api_key:
            genai.configure(api_key=api_key); model = genai.GenerativeModel('gemini-pro')
            prompt = st.chat_input("Ask...")
            if prompt:
                st.markdown(f"<div style='background:white; padding:10px; border-radius:10px; margin:5px;'><b>You:</b> {prompt}</div>", unsafe_allow_html=True)
                try:
                    res = model.generate_content(prompt).text
                    st.markdown(f"<div style='background:#e0e7ff; padding:10px; border-radius:10px; margin:5px;'><b>AI:</b> {res}</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")

if __name__ == "__main__":
    if st.session_state.user: main_app()
    else: login_page()