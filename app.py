import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import time
import requests
from streamlit_lottie import st_lottie

# --- 1. PAGE CONFIGURATION & THEME ---
st.set_page_config(page_title="Abhishek Jatav | Data Analyst Portfolio", page_icon="📊", layout="wide")

# --- 2. ASSETS & STYLING (CSS) ---
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Animations (Internet required)
lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
lottie_data = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_qp1q7mct.json")

# Custom CSS for Professional Look
st.markdown("""
<style>
    /* Background & Text Colors */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #30363D;
    }
    
    /* Custom Card Design for Metrics */
    div[data-testid="metric-container"] {
        background-color: #262730;
        border: 1px solid #41444C;
        padding: 15px;
        border-radius: 10px;
        color: white;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #58A6FF !important;
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Button Styling */
    .stButton>button {
        background-color: #238636;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #2EA043;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. AUTHENTICATION (LOGIN) ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def login_page():
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st_lottie(lottie_coding, height=200, key="login_anim")
        st.markdown("<h2 style='text-align: center;'>🔐 Access Secure Portfolio</h2>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login to Dashboard")
            
            if submitted:
                if username == "Abhishek" and password == "12345":
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = "Abhishek"
                    st.session_state['points'] = 500
                    st.success("Access Granted! Redirecting...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("⚠️ Access Denied! Try: Abhishek / 12345")

# --- 4. MAIN DASHBOARD ---
def main_dashboard():
    # --- SIDEBAR PROFILE ---
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
        st.markdown(f"### Hello, {st.session_state['username']}!")
        st.write("Python Developer | Data Analyst")
        st.metric("Future Points", st.session_state['points'], "Active")
        st.write("---")
        
        # Navigation
        selected = st.radio("Navigate", ["🏠 Home", "📊 Power BI", "📈 Tableau", "📗 Excel Tools", "🤖 AI Insight"])
        
        st.write("---")
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()

    # --- PAGE LOGIC ---
    
    # 1. HOME PAGE
    if selected == "🏠 Home":
        col1, col2 = st.columns([2, 1])
        with col1:
            st.title("Hi, I am Abhishek Jatav 👋")
            st.subheader("Transforming Data into Actionable Insights")
            st.write("""
            I specialize in building end-to-end data solutions using **Python, SQL, and Power BI**.
            This portfolio demonstrates my ability to handle complex datasets and create industry-standard dashboards.
            """)
            
            # Social Links & Resume
            st.markdown("""
            <a href='#' style='text-decoration:none; margin-right:15px;'>🔵 LinkedIn</a>
            <a href='#' style='text-decoration:none; margin-right:15px;'>⚫ GitHub</a>
            <a href='#' style='text-decoration:none;'>📄 Download Resume</a>
            """, unsafe_allow_html=True)
            
            st.write("---")
            # Metrics
            m1, m2, m3 = st.columns(3)
            m1.metric("Projects", "5+", "Completed")
            m2.metric("Experience", "Fresher", "Ready to Join")
            m3.metric("Tech Stack", "Full Stack", "Data")

        with col2:
            st_lottie(lottie_data, height=300)

    # 2. POWER BI
    elif selected == "📊 Power BI":
        st.title("Sales & Analytics Dashboard")
        st.markdown("Live interaction via **Power BI Service**.")
        
        # Replace this link with your actual Power BI link
        power_bi_link = "https://app.powerbi.com/view?r=eyJrIjoiNzY3NTI5N2EtOWE1OS00MzM2LWI3ZDgtN2Q4ZGI5ZGI5ZGI5IiwidCI6IjZkODg4ODg4LWI3ZDgtN2Q4ZGI5ZGI5ZGI5In0%3D"
        
        components.iframe(power_bi_link, width=1100, height=700)

    # 3. TABLEAU
    elif selected == "📈 Tableau":
        st.title("Visual Storytelling")
        st.markdown("Interactive visualizations via **Tableau Public**.")
        
        base_link = "https://public.tableau.com/views/Superstore_24/Overview"
        tableau_link = base_link + "?:embed=yes&:showVizHome=no"
        components.iframe(tableau_link, width=1100, height=700)

    # 4. EXCEL
    elif selected == "📗 Excel Tools":
        st.title("Excel Automation & Analysis")
        uploaded_file = st.file_uploader("Upload Dataset for Instant Analysis", type=['xlsx', 'csv'])
        
        if uploaded_file:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            c1, c2 = st.columns(2)
            c1.info(f"Rows: {df.shape[0]}")
            c2.info(f"Columns: {df.shape[1]}")
            
            st.dataframe(df, use_container_width=True)
            st.bar_chart(df.select_dtypes(include='number'))

    # 5. AI ASSISTANT
    elif selected == "🤖 AI Insight":
        st.title("Project Assistant (AI Bot)")
        
        with st.chat_message("assistant"):
            st.write("Hello! I am Abhishek's AI bot. Ask me about this project or my skills.")

        prompt = st.chat_input("Ask something (e.g., 'What is your tech stack?')")
        
        if prompt:
            with st.chat_message("user"):
                st.write(prompt)
            
            with st.chat_message("assistant"):
                # Smart Responses
                p = prompt.lower()
                if "python" in p:
                    st.write("Abhishek is proficient in **Python** for Data Cleaning (Pandas) and Web Dev (Streamlit).")
                elif "sql" in p:
                    st.write("He uses **MySQL** for database management and complex queries.")
                elif "contact" in p:
                    st.write("You can reach him at **abhishek@email.com**.")
                else:
                    st.write("That's an interesting question! This project showcases Data Analytics capabilities.")

# --- 5. EXECUTION FLOW ---
if __name__ == "__main__":
    if st.session_state['logged_in']:
        main_dashboard()
    else:
        login_page()