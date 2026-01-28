import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import plotly.graph_objects as go
import requests
from streamlit_lottie import st_lottie
import time

# --- 1. PAGE CONFIGURATION (Browser Tab Styling) ---
st.set_page_config(
    page_title="Abhishek Jatav | Data Scientist",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ASSETS & LOADER ---
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Premium 3D Animations
lottie_hero = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_w51pcehl.json") # Futuristic AI
lottie_coding = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_mjpamj1n.json") # Tech Dashboard

# --- 3. HIGH-END CUSTOM CSS (The "Luxury" Look) ---
st.markdown("""
<style>
    /* 1. Main Background - Deep Space Black */
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #1a1a2e 100%);
        font-family: 'Montserrat', sans-serif;
    }

    /* 2. Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 3. Text Styling - American Tech Style */
    h1, h2, h3 {
        color: #FFFFFF !important;
        font-weight: 700;
        letter-spacing: -1px;
    }
    h1 { font-size: 3.5rem !important; background: -webkit-linear-gradient(45deg, #00f260, #0575E6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    h2 { font-size: 2.2rem !important; border-bottom: 2px solid #0575E6; padding-bottom: 10px; display: inline-block; }
    p { color: #B0B3B8; font-size: 1.1rem; line-height: 1.6; }

    /* 4. Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(5, 117, 230, 0.5);
        box-shadow: 0 0 20px rgba(5, 117, 230, 0.2);
    }

    /* 5. Custom Button - Neon Glow */
    .stButton>button {
        background: transparent;
        border: 2px solid #0575E6;
        color: #0575E6;
        border-radius: 50px;
        padding: 10px 25px;
        font-weight: bold;
        transition: 0.4s;
    }
    .stButton>button:hover {
        background: #0575E6;
        color: white;
        box-shadow: 0 0 15px #0575E6;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR NAVIGATION (Modern App Style) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2202/2202112.png", width=80) # Placeholder Avatar
    st.markdown("<h3 style='text-align: center; color: white;'>ABHISHEK JATAV</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #0575E6; font-size: 14px;'>DATA ANALYTICS EXPERT</p>", unsafe_allow_html=True)
    
    # Modern Menu
    selected = option_menu(
        menu_title=None,
        options=["Profile", "Dashboard", "Analytics", "Contact"],
        icons=["person-bounding-box", "grid-fill", "bar-chart-line-fill", "envelope-fill"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#0575E6", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"5px", "--hover-color": "#1a1a2e", "color": "white"},
            "nav-link-selected": {"background-color": "#0575E6"},
        }
    )
    
    st.write("---")
    # Resume Download logic
    with open("requirements.txt", "rb") as file:
        st.download_button("📄 Download CV", data=file, file_name="Abhishek_Resume.pdf")

# --- 5. MAIN CONTENT SECTIONS ---

# === A. PROFILE (HOME) ===
if selected == "Profile":
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True) # Spacer
        st.markdown("<h1>DATA IS THE NEW CURRENCY.</h1>", unsafe_allow_html=True)
        st.markdown("""
        <p class='glass-card'>
        Hi, I'm <b>Abhishek</b>. I craft high-performance dashboards and scalable data pipelines. 
        My goal is simple: <b>Turn complex data into profitable decisions.</b>
        <br><br>
        Currently specializing in <b>Python Automation, SQL Architecture, and Advanced BI</b>.
        </p>
        """, unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Projects", "10+", "Global")
        c2.metric("Efficiency", "98%", "Optimized")
        c3.metric("Clients", "Global", "Reach")

    with col2:
        st_lottie(lottie_hero, height=450, key="hero_anim")

    # TECH STACK (Visual)
    st.write("---")
    st.subheader("⚡ Technical Arsenal")
    
    # Using Columns for Badges
    tech_cols = st.columns(6)
    techs = [
        ("Python", "https://img.icons8.com/color/48/python.png"),
        ("SQL", "https://img.icons8.com/color/48/sql.png"),
        ("PowerBI", "https://img.icons8.com/color/48/power-bi.png"),
        ("Tableau", "https://img.icons8.com/color/48/tableau-software.png"),
        ("Excel", "https://img.icons8.com/color/48/microsoft-excel-2019.png"),
        ("AI/ML", "https://img.icons8.com/fluency/48/artificial-intelligence.png")
    ]
    
    for col, (name, icon) in zip(tech_cols, techs):
        with col:
            st.image(icon, width=50)
            st.caption(name)

# === B. DASHBOARD (PROJECTS) ===
elif selected == "Dashboard":
    st.title("📂 Live Projects")
    st.markdown("<p>Interactive Business Intelligence Reports</p>", unsafe_allow_html=True)
    
    # Custom CSS Tab Styling via Streamlit
    tab1, tab2, tab3 = st.tabs(["🚀 Sales Power BI", "📈 Tableau Public", "🤖 Python Automation"])
    
    with tab1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 📊 Enterprise Sales Monitor")
        st.write("Real-time tracking of revenue, attrition, and KPI metrics.")
        # Replace Link
        link = "https://app.powerbi.com/view?r=eyJrIjoiNzY3NTI5N2EtOWE1OS00MzM2LWI3ZDgtN2Q4ZGI5ZGI5ZGI5IiwidCI6IjZkODg4ODg4LWI3ZDgtN2Q4ZGI5ZGI5ZGI5In0%3D"
        components.iframe(link, width=1000, height=600)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with tab2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 🌏 Superstore Global Analysis")
        link_tab = "https://public.tableau.com/views/Superstore_24/Overview?:showVizHome=no&:embed=true"
        components.iframe(link_tab, width=1000, height=600)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        col_a, col_b = st.columns(2)
        with col_a:
             st.markdown("""
             <div class='glass-card'>
             <h3>🐍 Python Automation Script</h3>
             <p>Automatically cleans 1 Million+ rows of raw Excel data and pushes to SQL Database.</p>
             <button style='background:#0575E6; color:white; border:none; padding:10px; border-radius:5px;'>View Code on GitHub</button>
             </div>
             """, unsafe_allow_html=True)
        with col_b:
            st_lottie(lottie_coding, height=200)

# === C. ANALYTICS (CUSTOM CHARTS) ===
elif selected == "Analytics":
    st.title("📈 Performance Analytics")
    st.markdown("My personal growth journey visualized.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Plotly High-End Chart (Radar Chart for Skills)
        categories = ['Python', 'SQL', 'Communication', 'Visualization', 'Statistics']
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
              r=[9, 8, 7, 10, 6],
              theta=categories,
              fill='toself',
              name='Abhishek',
              line_color='#0575E6'
        ))
        fig.update_layout(
          polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
          paper_bgcolor='rgba(0,0,0,0)',
          plot_bgcolor='rgba(0,0,0,0)',
          font=dict(color="white"),
          title="Skill Distribution Radar"
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        # Donut Chart
        labels = ['Data Cleaning', 'Modeling', 'Visualization', 'Reporting']
        values = [30, 20, 35, 15]
        fig2 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6)])
        fig2.update_traces(hoverinfo='label+percent', textinfo='value', marker=dict(colors=['#0575E6', '#00f260', '#8e44ad', '#f39c12']))
        fig2.update_layout(
            title="Project Time Allocation",
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="white")
        )
        st.plotly_chart(fig2, use_container_width=True)

# === D. CONTACT ===
elif selected == "Contact":
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.title("🤝 Let's Connect")
        st.markdown("Ready to transform your data strategy?")
        
        with st.form("contact_form_pro"):
            st.markdown("<h3 style='color: white;'>Send a Message</h3>", unsafe_allow_html=True)
            name = st.text_input("Name", placeholder="Elon Musk")
            email = st.text_input("Email", placeholder="elon@tesla.com")
            message = st.text_area("Message", placeholder="Let's build something crazy...")
            
            submit_btn = st.form_submit_button("🚀 Launch Message")
            if submit_btn:
                st.success("Message Transmitted Successfully!")
                st.balloons()
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div class='glass-card'>
            <h3>📍 Contact Details</h3>
            <p>📧 abhishek@example.com</p>
            <p>📱 +91 98765 43210</p>
            <p>🏢 Indore, Madhya Pradesh</p>
            <hr style='border-color: rgba(255,255,255,0.1);'>
            <p style='font-size: 12px; color: grey;'>Available for Freelance & Full-time roles.</p>
        </div>
        """, unsafe_allow_html=True)