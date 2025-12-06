import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_loader import load_data, get_column_info
from utils.config import get_agent
from utils.auth import require_api_key, get_api_key, get_selected_model
from utils.ui import setup_page, render_header, render_footer

# Setup page
setup_page(
    title="Exemple PandasAI",
    icon="📋",
    layout="wide"
)

# Check authentication - will stop execution if not authenticated
require_api_key()

render_header(
    title="📋 Galerie exemple PandasAI",
    description="Explorează exemple practice de utilizare a PandasAI pentru diferite scenarii de analiză"
)

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
st.header("🎯 Categorii de exemple")

example_categories = {
    "🔢 Calcule simple": [
        {
            "title": "Media GDP pentru România",
            "query": "Care este media GDP pentru România în toată perioada?",
            "description": "Exemplu simplu de calcul al mediei pentru o țară specifică"
        },
        {
            "title": "Valoare maximă",
            "query": "Care este valoarea maximă a Internet Users și în ce an a fost atinsă?",
            "description": "Găsește valoarea maximă și contextul acesteia"
        },
        {
            "title": "Număr de înregistrări",
            "query": "Câte înregistrări avem pentru fiecare țară?",
            "description": "Numără înregistrările grupate pe țări"
        }
    ],
    
    "📊 Agregări și grupări": [
        {
            "title": "Media pe țări",
            "query": "Calculează media tuturor indicatorilor pentru fiecare țară",
            "description": "Agregare complexă cu multiple coloane"
        },
        {
            "title": "Suma pe decade",
            "query": "Grupează datele pe decade și calculează suma Patent Applications pentru fiecare țară",
            "description": "Grupare temporală cu agregare"
        },
        {
            "title": "Top 5 ani",
            "query": "Arată-mi top 5 ani cu cel mai mare GDP pentru Bulgaria",
            "description": "Sortare și limitare de rezultate"
        }
    ],
    
    "📈 Analiză temporală": [
        {
            "title": "Evoluție în timp",
            "query": "Arată evoluția GDP pentru toate țările între 2010 și 2020",
            "description": "Filtrare temporală și vizualizare"
        },
        {
            "title": "Rata de creștere",
            "query": "Calculează rata de creștere anuală a Internet Users pentru România",
            "description": "Calcul de rate de schimbare"
        },
        {
            "title": "Comparație perioade",
            "query": "Compară media GDP între perioada 1990-2000 și 2010-2020 pentru toate țările",
            "description": "Comparație între intervale temporale"
        }
    ],
    
    "🔗 Corelații": [
        {
            "title": "Corelație simplă",
            "query": "Care este corelația dintre GDP și Internet Users?",
            "description": "Calcul de corelație între două variabile"
        },
        {
            "title": "Matrice corelație",
            "query": "Creează o matrice de corelație pentru toți indicatorii numerici",
            "description": "Corelații multiple între toate variabilele"
        },
        {
            "title": "Corelație pe țară",
            "query": "Care este corelația dintre FDI și Economic Freedom Index pentru fiecare țară separat?",
            "description": "Corelații grupate pe categorii"
        }
    ],
    
    "⚖️ Comparații": [
        {
            "title": "Comparație între țări",
            "query": "Compară GDP-ul mediu între România și Bulgaria",
            "description": "Comparație simplă între două entități"
        },
        {
            "title": "Clasament",
            "query": "Creează un clasament al țărilor bazat pe Economic Freedom Index în 2023",
            "description": "Sortare și clasificare"
        },
        {
            "title": "Diferențe relative",
            "query": "Cu cât diferă Mobile Subscriptions între Turcia și Grecia în 2020?",
            "description": "Calcul de diferențe absolute și relative"
        }
    ],
    
    "📉 Vizualizări": [
        {
            "title": "Grafic linie",
            "query": "Creează un grafic cu evoluția GDP pentru toate țările",
            "description": "Vizualizare time series"
        },
        {
            "title": "Grafic bare",
            "query": "Arată un grafic cu bare cu Patent Applications pentru fiecare țară în 2023",
            "description": "Comparație vizuală"
        },
        {
            "title": "Scatter plot",
            "query": "Creează un grafic de dispersie (scatter plot) între GDP și Internet Users",
            "description": "Vizualizare relație între variabile"
        }
    ],
    
    "🔍 Filtrări complexe": [
        {
            "title": "Filtrare multiplă",
            "query": "Arată datele pentru România și Bulgaria unde GDP > 8000",
            "description": "Filtrare pe multiple condiții"
        },
        {
            "title": "Top N cu condiție",
            "query": "Care sunt top 3 ani cu cel mai mare FDI pentru fiecare țară?",
            "description": "Filtrare și sortare grupată"
        },
        {
            "title": "Interval de valori",
            "query": "Găsește toate înregistrările unde Internet Users este între 50 și 70",
            "description": "Filtrare pe interval"
        }
    ],
    
    "🧮 Calcule avansate": [
        {
            "title": "Statistici descriptive",
            "query": "Calculează media, mediana, deviația standard și quartilele pentru GDP în fiecare țară",
            "description": "Multiple statistici descriptive"
        },
        {
            "title": "Procente și proporții",
            "query": "Care este procentul de creștere a Internet Users în România între 2000 și 2023?",
            "description": "Calcule procentuale"
        },
        {
            "title": "Scorurile Z",
            "query": "Calculează scorurile Z pentru GDP și identifică valorile extreme",
            "description": "Normalizare și detecție valori extreme (outliers)"
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
    st.header("📜 Istoric execuții")
    
    if st.button("🗑️ Șterge istoric"):
        st.session_state.examples_history = []
        st.rerun()
    
    for idx, item in enumerate(reversed(st.session_state.examples_history)):
        with st.expander(f"**{item['title']}** - {item['category']}", expanded=(idx == 0)):
            st.markdown(f"**Întrebare:** {item['query']}")
            st.markdown("**Rezultat:**")
            
            response = item['response']
            if isinstance(response, str):
                # Filter out file paths and inf values from response
                if not response.startswith('/') and not response.startswith('exports/') and response.lower() != 'inf':
                    st.write(response)
            elif isinstance(response, (pd.DataFrame, pd.Series)):
                st.dataframe(response, use_container_width=True)
            else:
                response_str = str(response)
                if not response_str.startswith('/') and not response_str.startswith('exports/') and response_str.lower() != 'inf':
                    st.write(response_str)
            
            # Check for charts
            chart_path = "exports/charts/temp_chart.png"
            if os.path.exists(chart_path):
                st.image(chart_path)
render_footer()
