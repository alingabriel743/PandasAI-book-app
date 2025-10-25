import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_loader import load_data, get_column_info
from utils.config import get_agent
from utils.auth import require_api_key, get_api_key, get_selected_model

st.set_page_config(page_title="Exemple PandasAI", page_icon="📋", layout="wide")

# Check authentication - will stop execution if not authenticated
require_api_key()

st.title("📋 Galerie Exemple PandasAI")
st.markdown("Explorează exemple practice de utilizare a PandasAI pentru diferite scenarii de analiză")

# Load data
df = load_data()
column_info = get_column_info()

# Initialize agent
if "agent_examples" not in st.session_state:
    with st.spinner("Inițializez PandasAI Agent..."):
        st.session_state.agent_examples = get_agent(df, get_api_key(), get_selected_model())

# Initialize history
if "examples_history" not in st.session_state:
    st.session_state.examples_history = []

# Example categories
st.header("🎯 Categorii de Exemple")

example_categories = {
    "🔢 Calcule Simple": [
        {
            "title": "Media GDP pentru România",
            "query": "Care este media GDP pentru România în toată perioada?",
            "description": "Exemplu simplu de calcul al mediei pentru o țară specifică"
        },
        {
            "title": "Valoare Maximă",
            "query": "Care este valoarea maximă a Internet Users și în ce an a fost atinsă?",
            "description": "Găsește valoarea maximă și contextul acesteia"
        },
        {
            "title": "Număr de Înregistrări",
            "query": "Câte înregistrări avem pentru fiecare țară?",
            "description": "Numără înregistrările grupate pe țări"
        }
    ],
    
    "📊 Agregări și Grupări": [
        {
            "title": "Media pe Țări",
            "query": "Calculează media tuturor indicatorilor pentru fiecare țară",
            "description": "Agregare complexă cu multiple coloane"
        },
        {
            "title": "Suma pe Decade",
            "query": "Grupează datele pe decade și calculează suma Patent Applications pentru fiecare țară",
            "description": "Grupare temporală cu agregare"
        },
        {
            "title": "Top 5 Ani",
            "query": "Arată-mi top 5 ani cu cel mai mare GDP pentru Bulgaria",
            "description": "Sortare și limitare de rezultate"
        }
    ],
    
    "📈 Analiză Temporală": [
        {
            "title": "Evoluție în Timp",
            "query": "Arată evoluția GDP pentru toate țările între 2010 și 2020",
            "description": "Filtrare temporală și vizualizare"
        },
        {
            "title": "Rata de Creștere",
            "query": "Calculează rata de creștere anuală a Internet Users pentru România",
            "description": "Calcul de rate de schimbare"
        },
        {
            "title": "Comparație Perioade",
            "query": "Compară media GDP între perioada 1990-2000 și 2010-2020 pentru toate țările",
            "description": "Comparație între intervale temporale"
        }
    ],
    
    "🔗 Corelații": [
        {
            "title": "Corelație Simplă",
            "query": "Care este corelația dintre GDP și Internet Users?",
            "description": "Calcul de corelație între două variabile"
        },
        {
            "title": "Matrice Corelație",
            "query": "Creează o matrice de corelație pentru toți indicatorii numerici",
            "description": "Corelații multiple între toate variabilele"
        },
        {
            "title": "Corelație pe Țară",
            "query": "Care este corelația dintre FDI și Economic Freedom Index pentru fiecare țară separat?",
            "description": "Corelații grupate pe categorii"
        }
    ],
    
    "⚖️ Comparații": [
        {
            "title": "Comparație între Țări",
            "query": "Compară GDP-ul mediu între România și Bulgaria",
            "description": "Comparație simplă între două entități"
        },
        {
            "title": "Ranking",
            "query": "Creează un ranking al țărilor bazat pe Economic Freedom Index în 2023",
            "description": "Sortare și clasificare"
        },
        {
            "title": "Diferențe Relative",
            "query": "Cu cât diferă Mobile Subscriptions între Turcia și Grecia în 2020?",
            "description": "Calcul de diferențe absolute și relative"
        }
    ],
    
    "📉 Vizualizări": [
        {
            "title": "Grafic Linie",
            "query": "Creează un grafic cu evoluția GDP pentru toate țările",
            "description": "Vizualizare time series"
        },
        {
            "title": "Grafic Bare",
            "query": "Arată un bar chart cu Patent Applications pentru fiecare țară în 2023",
            "description": "Comparație vizuală"
        },
        {
            "title": "Scatter Plot",
            "query": "Creează un scatter plot între GDP și Internet Users",
            "description": "Vizualizare relație între variabile"
        }
    ],
    
    "🔍 Filtrări Complexe": [
        {
            "title": "Filtrare Multiplă",
            "query": "Arată datele pentru România și Bulgaria unde GDP > 8000",
            "description": "Filtrare pe multiple condiții"
        },
        {
            "title": "Top N cu Condiție",
            "query": "Care sunt top 3 ani cu cel mai mare FDI pentru fiecare țară?",
            "description": "Filtrare și sortare grupată"
        },
        {
            "title": "Interval de Valori",
            "query": "Găsește toate înregistrările unde Internet Users este între 50 și 70",
            "description": "Filtrare pe interval"
        }
    ],
    
    "🧮 Calcule Avansate": [
        {
            "title": "Statistici Descriptive",
            "query": "Calculează media, mediana, deviația standard și quartilele pentru GDP în fiecare țară",
            "description": "Multiple statistici descriptive"
        },
        {
            "title": "Procente și Proporții",
            "query": "Care este procentul de creștere a Internet Users în România între 2000 și 2023?",
            "description": "Calcule procentuale"
        },
        {
            "title": "Z-Scores",
            "query": "Calculează z-scores pentru GDP și identifică valorile extreme",
            "description": "Normalizare și detecție outliers"
        }
    ]
}

# Display examples by category
for category, examples in example_categories.items():
    with st.expander(f"**{category}**", expanded=False):
        for idx, example in enumerate(examples):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**{example['title']}**")
                st.caption(example['description'])
                st.code(example['query'], language=None)
            
            with col2:
                if st.button("▶️ Rulează", key=f"{category}_{idx}", use_container_width=True):
                    with st.spinner("PandasAI procesează..."):
                        try:
                            # Delete old chart before processing
                            chart_path = "exports/charts/temp_chart.png"
                            if os.path.exists(chart_path):
                                try:
                                    os.remove(chart_path)
                                except:
                                    pass
                            
                            response = st.session_state.agent_examples.chat(example['query'])
                            
                            # Add to history
                            st.session_state.examples_history.append({
                                "category": category,
                                "title": example['title'],
                                "query": example['query'],
                                "response": response
                            })
                            
                            # Display result
                            st.success("✅ Executat cu succes!")
                            
                        except Exception as e:
                            st.error(f"❌ Eroare: {str(e)}")
            
            st.markdown("---")

# Display execution history
if st.session_state.examples_history:
    st.header("📜 Istoric Execuții")
    
    if st.button("🗑️ Șterge Istoric"):
        st.session_state.examples_history = []
        st.rerun()
    
    for idx, item in enumerate(reversed(st.session_state.examples_history)):
        with st.expander(f"**{item['title']}** - {item['category']}", expanded=(idx == 0)):
            st.markdown(f"**Întrebare:** {item['query']}")
            st.markdown("**Rezultat:**")
            
            response = item['response']
            if isinstance(response, str):
                st.write(response)
            elif isinstance(response, (pd.DataFrame, pd.Series)):
                st.dataframe(response, use_container_width=True)
            else:
                st.write(str(response))
            
            # Check for charts
            chart_path = "exports/charts/temp_chart.png"
            if os.path.exists(chart_path):
                st.image(chart_path)

# Custom query section
st.markdown("---")
st.header("✍️ Testează Propria Ta Întrebare")

custom_query = st.text_area(
    "Scrie o întrebare personalizată:",
    placeholder="Ex: Care este diferența medie dintre GDP-ul Greciei și al Turciei în ultimii 10 ani?",
    height=100
)

if st.button("🚀 Execută Întrebare Personalizată", type="primary"):
    if custom_query:
        with st.spinner("PandasAI procesează întrebarea ta..."):
            try:
                # Delete old chart before processing
                chart_path = "exports/charts/temp_chart.png"
                if os.path.exists(chart_path):
                    try:
                        os.remove(chart_path)
                    except:
                        pass
                
                response = st.session_state.agent_examples.chat(custom_query)
                
                st.subheader("📊 Rezultat:")
                if isinstance(response, str):
                    st.write(response)
                elif isinstance(response, (pd.DataFrame, pd.Series)):
                    st.dataframe(response, use_container_width=True)
                else:
                    st.write(str(response))
                
                # Check for newly generated charts
                if os.path.exists(chart_path):
                    st.image(chart_path)
                
                # Add to history
                st.session_state.examples_history.append({
                    "category": "✍️ Custom",
                    "title": "Întrebare Personalizată",
                    "query": custom_query,
                    "response": response
                })
            
            except Exception as e:
                st.error(f"❌ Eroare: {str(e)}")
    else:
        st.warning("Te rog introdu o întrebare.")

# Tips section
st.markdown("---")
st.subheader("💡 Sfaturi pentru Întrebări Eficiente")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### ✅ Bune Practici:
    
    - **Fii specific**: "Media GDP pentru România" în loc de "GDP România"
    - **Specifică perioada**: "între 2010 și 2020" când este relevant
    - **Cere vizualizări**: "Creează un grafic..." pentru chart-uri
    - **Folosește termeni clari**: "compară", "calculează", "arată"
    - **Grupează logic**: "pentru fiecare țară" când vrei agregări
    """)

with col2:
    st.markdown("""
    ### ❌ De Evitat:
    
    - Întrebări vagi: "Spune-mi despre date"
    - Prea multe cerințe: "Calculează totul și arată toate graficele"
    - Termeni ambigui: "cel mai bun" fără context
    - Întrebări fără context: "Care este valoarea?" (a cărei valori?)
    - Presupuneri: "Arată trendul" (care trend?)
    """)

# Learning section
st.markdown("---")
st.subheader("📚 Învață Mai Mult despre PandasAI")

with st.expander("🎓 Concepte Cheie"):
    st.markdown("""
    ### Cum Funcționează PandasAI:
    
    1. **Procesare Limbaj Natural**
       - Primește întrebarea ta în text
       - Analizează intenția și contextul
       - Identifică entitățile relevante (țări, indicatori, perioade)
    
    2. **Generare Cod**
       - Creează cod Python/Pandas automat
       - Optimizează pentru performanță
       - Gestionează edge cases
    
    3. **Execuție și Validare**
       - Rulează codul generat
       - Validează rezultatele
       - Gestionează erorile
    
    4. **Formatare Răspuns**
       - Prezintă rezultatul într-un format ușor de înțeles
       - Generează vizualizări când este relevant
       - Oferă context și explicații
    
    ### Tipuri de Operații Suportate:
    
    - **Agregări**: sum, mean, median, count, min, max
    - **Filtrări**: where, filter, select
    - **Sortări**: sort, rank, top N
    - **Grupări**: group by, pivot
    - **Calcule**: arithmetic, percentages, ratios
    - **Statistici**: std, var, correlation, percentiles
    - **Vizualizări**: line, bar, scatter, heatmap
    - **Transformări**: normalize, scale, encode
    """)

with st.expander("🔧 Debugging și Troubleshooting"):
    st.markdown("""
    ### Dacă Întâmpini Probleme:
    
    1. **Reformulează Întrebarea**
       - Încearcă o formulare mai simplă
       - Împarte întrebarea complexă în mai multe întrebări simple
    
    2. **Verifică Datele**
       - Asigură-te că numele coloanelor sunt corecte
       - Verifică că valorile există în dataset
    
    3. **Fii Mai Explicit**
       - Specifică exact ce vrei să vezi
       - Menționează coloanele și condițiile clar
    
    4. **Testează Incremental**
       - Începe cu o întrebare simplă
       - Adaugă complexitate treptat
    
    5. **Verifică API Key**
       - Asigură-te că API key-ul este valid
       - Verifică că ai credit disponibil
    """)
