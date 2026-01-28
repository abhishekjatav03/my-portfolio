import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Abhishek Jatav | AI Architect",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. 3D AI BRAIN FUNCTION (Pure Python - No Internet Needed) ---
def create_3d_network():
    # Generate random 3D coordinates for a "Neural Network" look
    N = 100
    x = np.random.randn(N)
    y = np.random.randn(N)
    z = np.random.randn(N)
    
    # Create Lines (Connections)
    edge_x = []
    edge_y = []
    edge_z = []
    for i in range(N):
        for j in range(i+1, N):
            if np.random.rand() > 0.98: # Connect random nodes
                edge_x.extend([x[i], x[j], None])
                edge_y.extend([y[i], y[j], None])
                edge_z.extend([z[i], z[j], None])

    # 3D Traces
    edge_trace = go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        mode='lines',
        line=dict(color='#00f260', width=1), # Neon Green Lines
        hoverinfo='none'
    )

    node_trace = go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers',
        marker=dict(
            size=5,
            color=z,
            colorscale='Viridis',
            opacity=0.8
        )
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        scene=dict(
            xaxis=dict(showbackground=False, showticklabels=False, title=''),
            yaxis=dict(showbackground=False, showticklabels=False, title=''),
            zaxis=dict(showbackground=False, showticklabels=False, title=''),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, b=0, t=0),
        showlegend=False
    )
    return fig

# --- 3. CUSTOM CSS (Cyberpunk Style) ---
st.markdown("""
<style>
    /* Dark Sci-Fi Background */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(#111 1px, transparent 1px);
        background-size: 20px 20px;
        color: white;
        font-family: 'Courier New', monospace;
    }
    
    /* Neon Headings */
    h1 {
        text-shadow: 0 0 10px #00f260, 0 0 20px #00f260;
        color: #fff !important;
    }
    
    /* Glass Cards */
    .glass-box {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 242, 96, 0.3);
        box-shadow: 0 0 15px rgba(0, 242, 96, 0.1);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        backdrop-filter: blur(5px);
    }
    
    /* Custom Buttons */
    .stButton>button {
        background: black;
        border: 1px solid #00f260;
        color: #00f260;
        border-radius: 5px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: #00f260;
        color: black;
        box-shadow: 0 0 20px #00f260;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/924/924915.png", width=80)
    st.markdown("### SYSTEM: ONLINE")
    st.markdown("USER: **ABHISHEK JATAV**")
    
    selected = option_menu(
        menu_title=None,
        options=["Neural Core", "Mission Control", "Data Uplink", "Comm-Link"],
        icons=["cpu", "activity", "database", "wifi"],
        default_index=0,
        styles={
            "container": {"background-color": "black"},
            "icon": {"color": "#00f260"}, 
            "nav-link": {"color": "white"},
            "nav-link-selected": {"background-color": "#1a1a1a", "border-left": "3px solid #00f260"},
        }
    )

# --- 5. PAGE LOGIC ---

# === HOME (NEURAL CORE) ===
if selected == "Neural Core":
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h1>ABHISHEK JATAV</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#00f260;'>>> AI & DATA ANALYTICS OPERATIVE</h3>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='glass-box'>
        <b>SYSTEM STATUS:</b> READY<br>
        <b>CURRENT OBJECTIVE:</b> Solving complex data problems.<br>
        <b>TOOLS:</b> Python, SQL, 3D Visualization.
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        c1.metric("Processing Power", "100%")
        c2.metric("Projects Deployed", "5+")

    with col2:
        # HERE IS THE AI 3D OPTION
        st.plotly_chart(create_3d_network(), use_container_width=True)
        st.caption("Interact: Drag to rotate the Neural Network")

# === PROJECTS (MISSION CONTROL) ===
elif selected == "Mission Control":
    st.title("🚀 MISSION CONTROL (DASHBOARDS)")
    
    tab1, tab2 = st.tabs(["[SECURE] SALES DATA", "[PUBLIC] TABLEAU"])
    
    with tab1:
        st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
        st.write("Initializing Power BI Interface...")
        # Replace Link
        link = "https://app.powerbi.com/view?r=eyJrIjoiNzY3NTI5N2EtOWE1OS00MzM2LWI3ZDgtN2Q4ZGI5ZGI5ZGI5IiwidCI6IjZkODg4ODg4LWI3ZDgtN2Q4ZGI5ZGI5ZGI5In0%3D"
        components.iframe(link, width=1000, height=550)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with tab2:
        st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
        st.write("Fetching Tableau Visuals...")
        link_tab = "https://public.tableau.com/views/Superstore_24/Overview?:showVizHome=no&:embed=true"
        components.iframe(link_tab, width=1000, height=550)
        st.markdown("</div>", unsafe_allow_html=True)

# === SKILLS (DATA UPLINK) ===
elif selected == "Data Uplink":
    st.title("📡 DATA UPLINK (SKILLS)")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("<div class='glass-box'><h3>🐍 PYTHON</h3><p>Automation & AI</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='glass-box'><h3>🗄️ SQL</h3><p>Database Architecture</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='glass-box'><h3>📊 POWER BI</h3><p>Visual Intelligence</p></div>", unsafe_allow_html=True)

    # 3D Bar Chart for Skills
    st.subheader("Skill Proficiency Matrix")
    langs = ['Python', 'SQL', 'Tableau', 'Excel']
    level = [90, 85, 80, 95]
    
    fig_bar = go.Figure(data=[go.Bar(
        x=langs, y=level,
        marker_color=['#00f260', '#0575E6', '#e74c3c', '#f1c40f']
    )])
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# === CONTACT (COMM-LINK) ===
elif selected == "Comm-Link":
    col1, col2 = st.columns(2)
    
    with col1:
        st.title("📞 ESTABLISH COMM-LINK")
        with st.form("hacker_form"):
            st.write("Enter Transmission Details:")
            name = st.text_input("Identity")
            msg = st.text_area("Encrypted Message")
            
            if st.form_submit_button("TRANSMIT DATA"):
                with st.spinner("Encrypting & Sending..."):
                    time.sleep(1)
                    st.success("TRANSMISSION RECEIVED.")
                    st.balloons()
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div class='glass-box'>
        <h3>📍 LOCATE OPERATIVE</h3>
        <p>> STATUS: ONLINE</p>
        <p>> LOCATION: INDORE, INDIA</p>
        <p>> EMAIL: abhishek@email.com</p>
        </div>
        """, unsafe_allow_html=True)