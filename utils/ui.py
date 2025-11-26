import streamlit as st
import base64

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

def custom_css():
    return """
    <style>
        /* Global Styles */
        .stApp {
            background-color: #f8f9fa;
        }
        
        /* Headers */
        h1, h2, h3 {
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            color: #2c3e50;
            font-weight: 700;
        }
        
        h1 {
            padding-bottom: 1rem;
            border-bottom: 2px solid #e9ecef;
            margin-bottom: 2rem;
        }
        
        /* Cards */
        .css-1r6slb0, .stCard {
            background-color: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
        }
        
        /* Metrics */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            color: #007bff;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 1rem;
            color: #6c757d;
        }
        
        /* Sidebar Container */
        [data-testid="stSidebar"] {
            background-color: #2c3e50;
        }
        
        /* Sidebar Text */
        [data-testid="stSidebar"] .stMarkdown, 
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3, 
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span {
            color: #ecf0f1 !important;
        }
        
        /* Sidebar Links */
        [data-testid="stSidebar"] a {
            color: #3498db !important;
            text-decoration: none;
        }
        
        [data-testid="stSidebar"] a:hover {
            text-decoration: underline;
            color: #5dade2 !important;
        }
        
        /* Sidebar Inputs - Text Input */
        [data-testid="stSidebar"] input {
            color: #ecf0f1 !important;
            background-color: #34495e !important;
            border: 1px solid #46637f !important;
        }
        
        /* Sidebar Selectbox & Dropdowns */
        [data-testid="stSidebar"] [data-baseweb="select"] > div {
            background-color: #34495e !important;
            border-color: #46637f !important;
            color: #ecf0f1 !important;
        }
        
        [data-testid="stSidebar"] [data-baseweb="select"] span {
            color: #ecf0f1 !important;
        }
        
        /* Dropdown Menu Options */
        [data-baseweb="popover"] {
            background-color: #2c3e50 !important;
        }
        
        [data-baseweb="menu"] {
            background-color: #2c3e50 !important;
        }
        
        [data-baseweb="menu"] li {
            background-color: #2c3e50 !important;
            color: #ecf0f1 !important;
        }
        
        [data-baseweb="menu"] li:hover {
            background-color: #34495e !important;
        }
        
        /* Selected Option in Dropdown */
        [data-baseweb="menu"] li[aria-selected="true"] {
            background-color: #3498db !important;
        }
        
        /* Sidebar Alerts */
        [data-testid="stSidebar"] .stAlert {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        [data-testid="stSidebar"] .stAlert [data-testid="stMarkdownContainer"] {
            color: #ecf0f1 !important;
        }
        
        /* Buttons */
        .stButton > button {
            border-radius: 20px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        /* Custom Classes */
        .feature-card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            height: 100%;
            border: 1px solid #e9ecef;
            transition: transform 0.2s;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
            border-color: #007bff;
        }
        
        .feature-card h3 {
            color: #2c3e50 !important;
        }
        
        .feature-card p {
            color: #6c757d !important;
        }
        
        .hero-section {
            text-align: center;
            padding: 3rem 1rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            margin-bottom: 2rem;
        }
        
        .hero-title {
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 1rem;
            color: white !important;
        }
        
        .hero-subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
            max-width: 800px;
            margin: 0 auto;
            color: white !important;
        }
        
        /* Chat Messages */
        .stChatMessage {
            background-color: white;
            border-radius: 10px;
            padding: 1rem;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: white;
            border-radius: 5px;
            padding: 0 20px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #007bff;
            color: white;
        }
        
    </style>
    """

def setup_page(title, icon, layout="wide"):
    st.set_page_config(
        page_title=title,
        page_icon=icon,
        layout=layout,
        initial_sidebar_state="expanded"
    )
    st.markdown(custom_css(), unsafe_allow_html=True)

def render_header(title, description=None):
    if description:
        st.markdown(f"""
        <div style="margin-bottom: 2rem;">
            <h1>{title}</h1>
            <p style="font-size: 1.2rem; color: #6c757d;">{description}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.title(title)

def render_footer():
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem; color: #6c757d;'>
        <p><strong>Aplicație demonstrativă PandasAI</strong></p>
        <p style='font-size: 0.9rem;'>Construit cu ❤️ folosind PandasAI, Streamlit și OpenRouter</p>
        <p style='font-size: 0.8rem; opacity: 0.7;'>Dezvoltat pentru capitolul de carte despre PandasAI</p>
    </div>
    """, unsafe_allow_html=True)

def render_feature_card(icon, title, description, link_text=None, link_url=None):
    link_html = f'<a href="{link_url}" target="_self" style="text-decoration: none; color: #007bff; font-weight: bold;">{link_text} &rarr;</a>' if link_text and link_url else ""
    
    return f"""
    <div class="feature-card">
        <div style="font-size: 2rem; margin-bottom: 1rem;">{icon}</div>
        <h3 style="margin-bottom: 0.5rem; font-size: 1.2rem;">{title}</h3>
        <p style="color: #6c757d; font-size: 0.9rem; margin-bottom: 1rem;">{description}</p>
        {link_html}
    </div>
    """
