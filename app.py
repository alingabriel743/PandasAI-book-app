import streamlit as st
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.auth import show_api_key_input

# Configurare pagină
st.set_page_config(
    page_title="Explorare Date Economice cu PandasAI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Show API key input in sidebar
show_api_key_input()

# Pagina principală
st.title("📊 Explorare Date Economice cu PandasAI")

st.markdown("""
### Bine ați venit la aplicația demonstrativă PandasAI!

Această aplicație este concepută pentru a demonstra **capacitățile avansate ale PandasAI** 
în analiza datelor economice din România, Bulgaria, Turcia și Grecia (1990-2023).

---
""")

# Main content in columns
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### 🤖 Ce este PandasAI?
    
    **PandasAI** este o bibliotecă Python revoluționară care adaugă capabilități de 
    **AI generativ** la pandas DataFrames. Permite utilizatorilor să:
    
    - 💬 **Pună întrebări în limbaj natural** despre date
    - 📊 **Genereze automat vizualizări** relevante
    - 🔍 **Efectueze analize complexe** fără cod
    - 📈 **Obțină insights** instant din date
    
    ### 📚 Despre Dataset
    
    Dataset-ul conține **indicatori economici** pentru 4 țări din Europa de Sud-Est:
    
    | Indicator | Descriere | Unitate |
    |-----------|-----------|---------|
    | **GDP** | Produsul Intern Brut per capita | USD |
    | **FDI** | Foreign Direct Investment | % din PIB |
    | **IU** | Internet Users | % din populație |
    | **MCS** | Mobile Cellular Subscriptions | per 100 persoane |
    | **PA** | Patent Applications | număr |
    | **EF** | Economic Freedom Index | index |
    
    **Perioada**: 1990-2023 | **Țări**: România, Bulgaria, Turcia, Grecia
    """)

with col2:
    st.info("""
    ### 🚀 Start Rapid
    
    1. **Obține API Key**
       - Vizitează [OpenRouter.ai](https://openrouter.ai/)
       - Creează cont gratuit
       - Generează API key
    
    2. **Explorează Paginile**
       - 🤖 Chat cu PandasAI
       - 🔍 Analiză Avansată
       - 📋 Galerie Exemple
    
    3. **Pune Întrebări**
       - Folosește limbaj natural
       - Cere vizualizări
       - Explorează relații
    """)
    
    st.success("""
    ### ✨ Caracteristici
    
    ✅ Analiză în limbaj natural  
    ✅ Vizualizări automate  
    ✅ Statistici avansate  
    ✅ Corelații și tendințe  
    ✅ Comparații complexe  
    ✅ Exemple practice  
    """)

st.markdown("---")

# Features showcase
st.header("🎯 Funcționalități Principale")

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Explorare Generală", 
    "🤖 Chat Inteligent", 
    "🔍 Analiză Avansată", 
    "📋 Exemple Practice"
])

with tab1:
    st.markdown("""
    ### 📈 Explorare Generală a Datelor
    
    Vizualizează și explorează dataset-ul folosind:
    - **Statistici descriptive** pentru toți indicatorii
    - **Grafice interactive** pentru evoluții temporale
    - **Comparații vizuale** între țări
    - **Filtre dinamice** pentru perioade și indicatori
    
    👉 **Pagină**: Explorare Generală
    """)

with tab2:
    st.markdown("""
    ### 🤖 Chat cu PandasAI
    
    Pune întrebări în **limbaj natural** și primește răspunsuri instant:
    
    **Exemple de întrebări:**
    - "Care este media GDP pentru România?"
    - "Compară Internet Users între toate țările în 2023"
    - "Creează un grafic cu evoluția FDI pentru Bulgaria"
    - "Care țară are cea mai mare creștere a Patent Applications?"
    
    👉 **Pagină**: Chat cu PandasAI
    """)

with tab3:
    st.markdown("""
    ### 🔍 Analiză Avansată cu PandasAI
    
    Efectuează analize complexe organizate pe categorii:
    
    - **Statistici Descriptive**: Media, mediana, deviație standard
    - **Corelații și Relații**: Identifică dependențe între variabile
    - **Analiză Comparativă**: Compară țări și perioade
    - **Predicții și Tendințe**: Identifică pattern-uri temporale
    - **Analiză Complexă**: Întrebări multi-dimensionale
    
    👉 **Pagină**: Analiză cu PandasAI
    """)

with tab4:
    st.markdown("""
    ### 📋 Galerie Exemple PandasAI
    
    Explorează **peste 24 de exemple practice** organizate pe categorii:
    
    - 🔢 **Calcule Simple**: Media, maxim, count
    - 📊 **Agregări și Grupări**: Group by, sum, average
    - 📈 **Analiză Temporală**: Evoluții, rate de creștere
    - 🔗 **Corelații**: Relații între variabile
    - ⚖️ **Comparații**: Rankings, diferențe
    - 📉 **Vizualizări**: Grafice automate
    - 🔍 **Filtrări Complexe**: Condiții multiple
    - 🧮 **Calcule Avansate**: Statistici descriptive
    
    👉 **Pagină**: Exemple PandasAI
    """)

st.markdown("---")

# Why PandasAI section
st.header("💡 De Ce PandasAI?")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🎯 Accesibilitate
    
    - **Fără cod**: Nu necesită cunoștințe de programare
    - **Limbaj natural**: Întrebări în română/engleză
    - **Intuitiv**: Interface prietenoasă
    - **Rapid**: Rezultate instant
    """)

with col2:
    st.markdown("""
    ### 🚀 Productivitate
    
    - **Automatizare**: Generează cod automat
    - **Vizualizări**: Chart-uri relevante
    - **Flexibilitate**: Adaptare la context
    - **Eficiență**: Analize complexe simplificate
    """)

with col3:
    st.markdown("""
    ### 🔬 Capabilități
    
    - **Statistici**: Calcule avansate
    - **ML Integration**: Predicții și pattern-uri
    - **Multi-format**: Text, tabele, grafice
    - **Contextual**: Înțelege intenția
    """)

st.markdown("---")

# Getting started guide
with st.expander("📖 Ghid de Utilizare Rapidă"):
    st.markdown("""
    ### Pași pentru a Începe:
    
    #### 1. Configurare Inițială
    ```
    1. Obține un API Key gratuit de la OpenRouter.ai
    2. Introdu API Key-ul în bara laterală a oricărei pagini
    3. Așteaptă confirmarea conexiunii
    ```
    
    #### 2. Explorare Dataset
    ```
    - Mergi la "Explorare Generală" pentru o privire de ansamblu
    - Vizualizează statistici și grafice interactive
    - Filtrează date după țări și perioade
    ```
    
    #### 3. Interacțiune cu PandasAI
    ```
    - Accesează "Chat cu PandasAI"
    - Scrie întrebări în limbaj natural
    - Primește răspunsuri și vizualizări automate
    ```
    
    #### 4. Învățare prin Exemple
    ```
    - Explorează "Exemple PandasAI"
    - Rulează exemple predefinite
    - Înțelege diferite tipuri de analize
    ```
    
    #### 5. Analiză Avansată
    ```
    - Folosește "Analiză cu PandasAI"
    - Selectează categoria de analiză
    - Explorează capabilități complexe
    ```
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><strong>Aplicație Demonstrativă PandasAI</strong></p>
    <p>Construit cu ❤️ folosind PandasAI, Streamlit și OpenRouter</p>
    <p><em>Dezvoltat pentru capitolul de carte despre PandasAI</em></p>
</div>
""", unsafe_allow_html=True)
