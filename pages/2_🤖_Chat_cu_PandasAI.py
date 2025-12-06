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
    title="Chat cu PandasAI",
    icon="🤖",
    layout="wide"
)

render_header(
    title="🤖 Chat cu PandasAI",
    description="Pune întrebări în limbaj natural despre datele economice"
)

# Require API key authentication
api_key = require_api_key()

# Load data
df = load_data()
column_info = get_column_info()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    with st.spinner("Inițializez PandasAI Agent..."):
        st.session_state.agent = get_agent(df, api_key, get_selected_model())

# Display dataset info
with st.expander("📊 Informații despre setul de date", expanded=False):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total înregistrări", len(df))
    with col2:
        st.metric("Țări", df['Country'].nunique())
    with col3:
        st.metric("Ani", f"{df['Year'].min()}-{df['Year'].max()}")
    
    st.subheader("Coloane disponibile:")
    for col, info in column_info.items():
        st.write(f"**{col}**: {info['description']}")

# Example queries
with st.expander("💡 Exemple de întrebări", expanded=False):
    st.markdown("Click pe un exemplu pentru a-l copia în chat:")
    
    example_queries = [
        "Care este media PIB-ului pentru România în toată perioada?",
        "Care țară a avut cel mai mare Internet Usage în 2020?",
        "Arată-mi evoluția subscripțiilor mobile pentru Turcia între 2000 și 2010",
        "Compară Economic Freedom Index între toate țările în 2023",
        "Care este corelația dintre PIB și utilizatorii de internet pentru Grecia?",
        "Creează un grafic cu evoluția PIB-ului pentru toate țările",
        "Care țară a avut cea mai mare creștere a FDI între 2010 și 2020?",
        "Calculează media Patent Applications pentru Bulgaria după 2015",
        "Arată-mi top 3 ani cu cel mai mare PIB pentru România",
        "Care este diferența dintre PIB-ul Greciei și al Bulgariei în 2023?"
    ]
    
    cols = st.columns(2)
    for idx, example in enumerate(example_queries):
        with cols[idx % 2]:
            if st.button(example, key=f"example_{idx}", use_container_width=True):
                st.session_state.current_query = example

st.markdown("---")

# --- MAIN CHAT INTERFACE ---

# Chat interface
st.subheader("💬 Conversație")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message and message["image"]:
            # Check if image still exists before displaying
            if os.path.exists(message["image"]):
                st.image(message["image"])

# Chat input
if prompt := st.chat_input("Pune o întrebare despre date...") or st.session_state.get("current_query"):
    if st.session_state.get("current_query"):
        prompt = st.session_state.current_query
        st.session_state.current_query = None
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response from PandasAI
    with st.chat_message("assistant"):
        with st.spinner("Analizez întrebarea..."):
            try:
                # Delete old chart before processing new question
                chart_path = "exports/charts/temp_chart.png"
                if os.path.exists(chart_path):
                    try:
                        os.remove(chart_path)
                    except:
                        pass
                
                response = st.session_state.agent.chat(prompt)
                
                # Display response
                if isinstance(response, str):
                    st.markdown(response)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "image": None
                    })
                elif isinstance(response, (pd.DataFrame, pd.Series)):
                    st.dataframe(response, use_container_width=True)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Iată rezultatul:\n\n{response.to_string()}",
                        "image": None
                    })
                else:
                    st.write(str(response))
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": str(response),
                        "image": None
                    })
                
                # Check for newly generated charts and save a copy
                if os.path.exists(chart_path):
                    st.image(chart_path)
                    # Save a copy of the chart with unique name for history
                    import time
                    unique_chart_path = f"exports/charts/chart_{int(time.time() * 1000)}.png"
                    try:
                        import shutil
                        shutil.copy2(chart_path, unique_chart_path)
                        # Update last message with unique image path
                        if st.session_state.messages:
                            st.session_state.messages[-1]["image"] = unique_chart_path
                    except Exception as e:
                        # If copy fails, don't save image reference
                        pass
            
            except Exception as e:
                error_msg = f"❌ Eroare la procesarea întrebării: {str(e)}"
                st.error(error_msg)
                st.info("Încearcă să reformulezi întrebarea sau verifică API Key-ul.")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "image": None
                })

# Clear chat button
if st.session_state.messages:
    if st.button("🗑️ Șterge conversația", type="secondary"):
        st.session_state.messages = []
        st.rerun()



# Tips section
st.markdown("---")
with st.expander("💡 Sfaturi pentru întrebări"):
    st.markdown("""
    **1. Întrebări statistice:**
    - "Care este media/mediana/suma pentru [indicator]?"
    
    **2. Comparații:**
    - "Compară [indicator] între [țară1] și [țară2]"
    
    **3. Analize temporale:**
    - "Arată evoluția [indicator] între [an1] și [an2]"
    
    **4. Vizualizări:**
    - "Creează un grafic cu [indicator]"
    """)

with st.expander("🤖 Despre PandasAI"):
    st.caption("""
    PandasAI este o bibliotecă Python care adaugă capabilități de AI generativ la seturi de date (DataFrames).
    Permite utilizatorilor să pună întrebări despre datele lor în limbaj natural.
    """)

render_footer()
