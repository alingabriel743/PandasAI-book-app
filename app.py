import streamlit as st
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.auth import show_api_key_input
from utils.ui import setup_page, render_footer, render_feature_card

# Setup page with custom styles
# Setup page with custom styles
setup_page(
    title="Explorare date economice cu PandasAI",
    icon="📊",
    layout="wide"
)

# Show API key input in sidebar
show_api_key_input()

# Hero Section
st.markdown("""
<div class="hero-section">
    <div class="hero-title">📊 Explorare date economice cu PandasAI</div>
    <div class="hero-subtitle">
        O platformă interactivă pentru analiza datelor economice din Europa de Sud-Est (1990-2023)
        folosind puterea AI generativ.
    </div>
</div>
""", unsafe_allow_html=True)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🤖 Ce este PandasAI?")
    st.markdown("""
    <div style="background-color: white; padding: 20px; border-radius: 10px; border-left: 5px solid #007bff; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
        <p style="font-size: 1.1rem; line-height: 1.6;">
        <strong>PandasAI</strong> este o bibliotecă Python revoluționară care adaugă capabilități de 
        <strong>AI generativ</strong> la pandas DataFrames. Această aplicație demonstrează cum poți:
        </p>
        <ul style="list-style-type: none; padding-left: 0;">
            <li style="margin-bottom: 10px;">💬 <strong>Interacționa în limbaj natural</strong> cu datele tale</li>
            <li style="margin-bottom: 10px;">📊 <strong>Genera vizualizări automate</strong> instantaneu</li>
            <li style="margin-bottom: 10px;">🔍 <strong>Descoperi insights ascunse</strong> fără a scrie cod complex</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📚 Despre dataset")
    st.markdown("""
    Dataset-ul acoperă perioada **1990-2023** pentru **România, Bulgaria, Turcia și Grecia**.
    Include indicatori cheie precum:
    """)
    
    # Dataset indicators as pills/badges
    indicators = [
        ("GDP", "Produs intern brut", "💰"),
        ("FDI", "Investiții străine", "🌍"),
        ("Internet Users", "Digitalizare", "💻"),
        ("Mobile Subs", "Conectivitate", "📱"),
        ("Patents", "Inovație", "💡"),
        ("Economic Freedom", "Libertate ec.", "⚖️")
    ]
    
    cols = st.columns(3)
    for idx, (code, name, icon) in enumerate(indicators):
        with cols[idx % 3]:
            st.markdown(f"""
            <div style="text-align: center; padding: 10px; background: white; border-radius: 8px; margin-bottom: 10px; border: 1px solid #eee;">
                <div style="font-size: 1.5rem;">{icon}</div>
                <div style="font-weight: bold;">{code}</div>
                <div style="font-size: 0.8rem; color: #666;">{name}</div>
            </div>
            """, unsafe_allow_html=True)

with col2:
    st.markdown("### 🚀 Start rapid")
    
    steps = [
        ("1", "Obține API key", "Gratuit de la OpenRouter.ai"),
        ("2", "Configurează", "Introdu cheia în meniul lateral"),
        ("3", "Explorează", "Alege o pagină din meniu")
    ]
    
    for num, title, desc in steps:
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 15px; background: white; padding: 10px; border-radius: 8px;">
            <div style="background: #007bff; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 15px;">{num}</div>
            <div>
                <div style="font-weight: bold;">{title}</div>
                <div style="font-size: 0.8rem; color: #666;">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("""
    **Sfat:** Începe cu pagina "Explorare generală" pentru a te familiariza cu datele, apoi încearcă "Chat cu PandasAI"!
    """)

st.markdown("---")

# Features showcase with new card design
st.header("🎯 Funcționalități principale")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(render_feature_card(
        "📈", 
        "Explorare generală", 
        "Statistici descriptive, grafice interactive și filtre dinamice pentru o privire de ansamblu.",
        "Mergi la pagină",
        "/Explorare_Generala"
    ), unsafe_allow_html=True)

with col2:
    st.markdown(render_feature_card(
        "🤖", 
        "Chat inteligent", 
        "Pune întrebări în limbaj natural și primește răspunsuri și vizualizări instant.",
        "Mergi la pagină",
        "/Chat_cu_PandasAI"
    ), unsafe_allow_html=True)

with col3:
    st.markdown(render_feature_card(
        "🔍", 
        "Analiză avansată", 
        "Corelații, predicții, comparații complexe și analiză statistică detaliată.",
        "Mergi la pagină",
        "/Analiza_cu_PandasAI"
    ), unsafe_allow_html=True)

with col4:
    st.markdown(render_feature_card(
        "📋", 
        "Exemple practice", 
        "O galerie de peste 24 de exemple gata de rulat pentru a învăța rapid.",
        "Mergi la pagină",
        "/Exemple_PandasAI"
    ), unsafe_allow_html=True)

# Footer
render_footer()
