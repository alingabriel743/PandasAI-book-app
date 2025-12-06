import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_loader import load_data, get_column_info
from utils.config import get_agent
from utils.auth import require_api_key, get_selected_model
from utils.ui import setup_page, render_header, render_footer

# Setup page
setup_page(
    title="Analiză cu PandasAI",
    icon="🔍",
    layout="wide"
)

render_header(
    title="🔍 Analiză avansată cu PandasAI",
    description="Demonstrează capacitățile avansate ale PandasAI pentru analiză de date"
)

st.info("""
**💡 Notă:** Această pagină oferă o abordare **structurată** a analizei, ghidându-te prin categorii specifice. 
Pentru conversații libere, folosește pagina **Chat**. Pentru rapoarte complete autonome, încearcă **Agent de Raportare**.
""")

# Require API key authentication
api_key = require_api_key()

# Load data
df = load_data()
column_info = get_column_info()

# Initialize agent
if "agent_advanced" not in st.session_state:
    with st.spinner("Inițializez PandasAI Agent..."):
        st.session_state.agent_advanced = get_agent(df, api_key, get_selected_model())

# Analysis categories
st.header("📊 Categorii de analiză")

# Use radio for better visibility of options
analysis_category = st.radio(
    "Selectează categoria de analiză:",
    [
        "Statistici descriptive",
        "Corelații și relații",
        "Analiză comparativă",
        "Predicții și tendințe",
        "Analiză complexă"
    ],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("---")

if analysis_category == "Statistici descriptive":
    st.subheader("📈 Statistici descriptive cu PandasAI")
    
    st.markdown("""
    PandasAI poate genera automat statistici descriptive complexe despre date.
    Selectează o întrebare predefinită sau scrie una personalizată.
    """)
    
    predefined_queries = [
        "Calculează media, mediana și deviația standard pentru GDP în fiecare țară",
        "Care sunt valorile minime și maxime pentru toți indicatorii în România?",
        "Arată-mi un sumar statistic complet pentru toate țările în 2023",
        "Care este distribuția valorilor pentru Internet Users în toate țările?",
        "Calculează quartilele pentru Economic Freedom Index pe țări",
        "Care este coeficientul de variație pentru FDI în fiecare țară?"
    ]
    
    selected_query = st.selectbox(
        "Întrebări predefinite:",
        [""] + predefined_queries,
        key="stats_query"
    )
    
    if st.button("🔍 Analizează", key="stats_btn", type="primary"):
        if selected_query:
            with st.spinner("PandasAI analizează datele..."):
                try:
                    # Delete old chart before processing
                    chart_path = "exports/charts/temp_chart.png"
                    if os.path.exists(chart_path):
                        try:
                            os.remove(chart_path)
                        except:
                            pass
                    
                    response = st.session_state.agent_advanced.chat(selected_query)
                    
                    st.markdown("---")
                    col_result, _ = st.columns([1, 1])
                    with col_result:
                        st.subheader("📊 Rezultat:")
                        if isinstance(response, str):
                            # Filter out file paths from response
                            if not response.startswith('/') and not response.startswith('exports/'):
                                st.write(response)
                        elif isinstance(response, (pd.DataFrame, pd.Series)):
                            st.dataframe(response)
                        else:
                            response_str = str(response)
                            if not response_str.startswith('/') and not response_str.startswith('exports/'):
                                st.write(response_str)
                    
                    # Check for newly generated charts
                    if os.path.exists(chart_path):
                        st.image(chart_path)
                
                except Exception as e:
                    st.error(f"Eroare: {str(e)}")

elif analysis_category == "Corelații și relații":
    st.subheader("🔗 Analiză corelații cu PandasAI")
    
    st.markdown("""
    PandasAI poate identifica și analiza relații între variabile.
    """)
    
    predefined_queries = [
        "Care este corelația dintre GDP și Internet Users pentru toate țările?",
        "Există o relație între Economic Freedom Index și FDI?",
        "Arată-mi corelațiile dintre toți indicatorii pentru România",
        "Care indicatori sunt cel mai puternic corelați cu GDP?",
        "Creează o matrice de corelație pentru toate variabilele numerice",
        "Există o relație liniară între Mobile Subscriptions și Internet Users?"
    ]
    
    selected_query = st.selectbox(
        "Întrebări predefinite:",
        [""] + predefined_queries,
        key="corr_query"
    )
    
    custom_query = st.text_area(
        "Sau scrie o întrebare personalizată:",
        placeholder="Ex: Compară corelația dintre GDP și IU în România vs Bulgaria",
        key="corr_custom"
    )
    
    if st.button("🔍 Analizează corelații", type="primary"):
        query = custom_query if custom_query else selected_query
        if query:
            with st.spinner("PandasAI analizează corelațiile..."):
                try:
                    # Delete old chart before processing
                    chart_path = "exports/charts/temp_chart.png"
                    if os.path.exists(chart_path):
                        try:
                            os.remove(chart_path)
                        except:
                            pass
                    
                    response = st.session_state.agent_advanced.chat(query)
                    
                    st.subheader("📊 Rezultat:")
                    if isinstance(response, str):
                        # Filter out file paths from response
                        if not response.startswith('/') and not response.startswith('exports/'):
                            st.write(response)
                    elif isinstance(response, (pd.DataFrame, pd.Series)):
                        st.dataframe(response, use_container_width=True)
                    else:
                        response_str = str(response)
                        if not response_str.startswith('/') and not response_str.startswith('exports/'):
                            st.write(response_str)
                    
                    # Check for newly generated charts
                    if os.path.exists(chart_path):
                        st.image(chart_path)
                
                except Exception as e:
                    st.error(f"Eroare: {str(e)}")

elif analysis_category == "Analiză comparativă":
    st.subheader("⚖️ Analiză comparativă cu PandasAI")
    
    st.markdown("""
    PandasAI poate efectua comparații complexe între țări, perioade și indicatori.
    """)
    
    predefined_queries = [
        "Compară GDP-ul mediu între toate cele 4 țări în ultimii 10 ani",
        "Care țară a avut cea mai mare creștere a Internet Users între 2000 și 2023?",
        "Compară performanța economică (GDP, FDI, EF) între România și Bulgaria",
        "Care țară are cele mai bune valori pentru toți indicatorii în 2023?",
        "Arată diferențele dintre țări pentru Patent Applications în 2020",
        "Compară evoluția Mobile Subscriptions între Turcia și Grecia"
    ]
    
    selected_query = st.selectbox(
        "Întrebări predefinite:",
        [""] + predefined_queries,
        key="comp_query"
    )
    
    custom_query = st.text_area(
        "Sau scrie o întrebare personalizată:",
        placeholder="Ex: Care țară a avut cea mai stabilă evoluție a GDP între 1990 și 2023?",
        key="comp_custom"
    )
    
    if st.button("🔍 Compară", type="primary"):
        query = custom_query if custom_query else selected_query
        if query:
            with st.spinner("PandasAI efectuează comparația..."):
                try:
                    # Delete old chart before processing
                    chart_path = "exports/charts/temp_chart.png"
                    if os.path.exists(chart_path):
                        try:
                            os.remove(chart_path)
                        except:
                            pass
                    
                    response = st.session_state.agent_advanced.chat(query)
                    
                    st.subheader("📊 Rezultat:")
                    if isinstance(response, str):
                        # Filter out file paths from response
                        if not response.startswith('/') and not response.startswith('exports/'):
                            st.write(response)
                    elif isinstance(response, (pd.DataFrame, pd.Series)):
                        st.dataframe(response, use_container_width=True)
                    else:
                        response_str = str(response)
                        if not response_str.startswith('/') and not response_str.startswith('exports/'):
                            st.write(response_str)
                    
                    # Check for newly generated charts
                    if os.path.exists(chart_path):
                        st.image(chart_path)
                
                except Exception as e:
                    st.error(f"Eroare: {str(e)}")

elif analysis_category == "Predicții și tendințe":
    st.subheader("🔮 Analiză tendințe cu PandasAI")
    
    st.markdown("""
    PandasAI poate identifica tendințe și pattern-uri în date.
    """)
    
    predefined_queries = [
        "Care este trendul general al GDP pentru România în ultimii 30 de ani?",
        "Identifică pattern-urile de creștere pentru Internet Users în toate țările",
        "Care indicatori arată o tendință de creștere constantă pentru Bulgaria?",
        "Există o tendință sezonieră sau ciclică în datele economice?",
        "Care țară are cea mai predictibilă evoluție a Economic Freedom Index?",
        "Arată-mi anii cu cele mai mari schimbări pentru toți indicatorii"
    ]
    
    selected_query = st.selectbox(
        "Întrebări predefinite:",
        [""] + predefined_queries,
        key="trend_query"
    )
    
    custom_query = st.text_area(
        "Sau scrie o întrebare personalizată:",
        placeholder="Ex: Bazat pe datele istorice, care ar fi valoarea estimată a GDP pentru România în 2024?",
        key="trend_custom"
    )
    
    if st.button("🔍 Analizează tendințe", type="primary"):
        query = custom_query if custom_query else selected_query
        if query:
            with st.spinner("PandasAI analizează tendințele..."):
                try:
                    # Delete old chart before processing
                    chart_path = "exports/charts/temp_chart.png"
                    if os.path.exists(chart_path):
                        try:
                            os.remove(chart_path)
                        except:
                            pass
                    
                    response = st.session_state.agent_advanced.chat(query)
                    
                    st.subheader("📊 Rezultat:")
                    if isinstance(response, str):
                        # Filter out file paths from response
                        if not response.startswith('/') and not response.startswith('exports/'):
                            st.write(response)
                    elif isinstance(response, (pd.DataFrame, pd.Series)):
                        st.dataframe(response, use_container_width=True)
                    else:
                        response_str = str(response)
                        if not response_str.startswith('/') and not response_str.startswith('exports/'):
                            st.write(response_str)
                    
                    # Check for newly generated charts
                    if os.path.exists(chart_path):
                        st.image(chart_path)
                
                except Exception as e:
                    st.error(f"Eroare: {str(e)}")

else:  # Analiză complexă
    st.subheader("🧠 Analiză complexă cu PandasAI")
    
    st.markdown("""
    PandasAI poate răspunde la întrebări complexe care necesită multiple operații de analiză.
    """)
    
    predefined_queries = [
        "Care sunt top 3 factori care influențează GDP în fiecare țară?",
        "Identifică outliers și anomalii în datele pentru toate țările",
        "Grupează țările bazat pe similaritatea indicatorilor economici",
        "Care este impactul FDI asupra celorlalți indicatori economici?",
        "Creează un profil economic complet pentru fiecare țară în 2023",
        "Care țară are cea mai echilibrată dezvoltare pe toți indicatorii?"
    ]
    
    selected_query = st.selectbox(
        "Întrebări predefinite:",
        [""] + predefined_queries,
        key="complex_query"
    )
    
    custom_query = st.text_area(
        "Sau scrie o întrebare personalizată complexă:",
        placeholder="Ex: Analizează relația dintre dezvoltarea digitală (IU, MCS) și dezvoltarea economică (GDP, FDI) pentru toate țările",
        height=100,
        key="complex_custom"
    )
    
    if st.button("🔍 Analizează complex", type="primary"):
        query = custom_query if custom_query else selected_query
        if query:
            with st.spinner("PandasAI efectuează analiza complexă... Acest lucru poate dura mai mult."):
                try:
                    # Delete old chart before processing
                    chart_path = "exports/charts/temp_chart.png"
                    if os.path.exists(chart_path):
                        try:
                            os.remove(chart_path)
                        except:
                            pass
                    
                    response = st.session_state.agent_advanced.chat(query)
                    
                    st.subheader("📊 Rezultat:")
                    if isinstance(response, str):
                        # Filter out file paths from response
                        if not response.startswith('/') and not response.startswith('exports/'):
                            st.write(response)
                    elif isinstance(response, (pd.DataFrame, pd.Series)):
                        st.dataframe(response, use_container_width=True)
                    else:
                        response_str = str(response)
                        if not response_str.startswith('/') and not response_str.startswith('exports/'):
                            st.write(response_str)
                    
                    # Check for newly generated charts
                    if os.path.exists(chart_path):
                        st.image(chart_path)
                
                except Exception as e:
                    st.error(f"Eroare: {str(e)}")

# Information section
st.markdown("---")
st.subheader("💡 Despre capacitățile PandasAI")

with st.expander("🎯 Ce poate face PandasAI?"):
    st.markdown("""
    ### Capacități principale:
    
    1. **Analiză statistică automată**
       - Calculează statistici descriptive complexe
       - Identifică distribuții și pattern-uri
       - Detectează valori extreme (outliers) și anomalii
    
    2. **Analiză relațională**
       - Calculează corelații între variabile
       - Identifică dependențe și relații
       - Analizează cauzalitate
    
    3. **Comparații inteligente**
       - Compară între grupuri (țări, perioade)
       - Identifică diferențe semnificative
       - Ierarhizează și clasifică
    
    4. **Analiză temporală**
       - Identifică tendințe și pattern-uri
       - Calculează rate de creștere
       - Detectează schimbări semnificative
    
    5. **Vizualizări automate**
       - Generează grafice relevante
       - Alege tipul optim de vizualizare
       - Creează dashboard-uri
    
    6. **Analiză complexă**
       - Combină multiple operații
       - Răspunde la întrebări multi-dimensionale
       - Oferă insights acționabile
    
    ### Avantaje față de Pandas tradițional:
    
    - ✅ **Limbaj natural**: Nu necesită cunoștințe de programare
    - ✅ **Inteligență contextuală**: Înțelege intenția utilizatorului
    - ✅ **Automatizare**: Generează cod automat
    - ✅ **Flexibilitate**: Se adaptează la diferite tipuri de întrebări
    - ✅ **Vizualizări**: Creează grafice automat când este relevant
    """)

with st.expander("📚 Exemple de întrebări avansate"):
    st.markdown("""
    ### Întrebări statistice:
    - "Calculează asimetria (skewness) și boltirea (kurtosis) pentru GDP în fiecare țară"
    - "Care este intervalul de încredere 95% pentru media FDI?"
    - "Efectuează un test de normalitate pentru Internet Users"
    
    ### Întrebări de corelație:
    - "Care perechi de variabile au corelația cea mai puternică?"
    - "Există coliniaritate între indicatori?"
    - "Calculează corelația parțială dintre GDP și IU controlând pentru Year"
    
    ### Întrebări comparative:
    - "Care țară a avut cea mai volatilă evoluție economică?"
    - "Compară performanța relativă a țărilor folosind scoruri Z (z-scores)"
    - "Identifică țara cu cea mai echilibrată dezvoltare"
    
    ### Întrebări temporale:
    - "Care a fost rata de creștere anuală compusă (CAGR) pentru GDP?"
    - "Identifică punctele de inflexiune în evoluția indicatorilor"
    - "Care ani au fost cei mai buni/răi pentru fiecare țară?"
    
    ### Întrebări complexe:
    - "Creează un scoring compozit bazat pe toți indicatorii"
    - "Grupează anii în perioade bazat pe similaritatea indicatorilor"
    - "Identifică factorii comuni care explică variația în date"
    """)

render_footer()
