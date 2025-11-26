import streamlit as st
import pandas as pd
import sys
import os
from fpdf import FPDF
import io
import time

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_loader import load_data, get_column_info
from utils.config import get_agent, OpenRouterLLM
from utils.auth import require_api_key, get_selected_model
from utils.ui import setup_page, render_header, render_footer


def create_pdf_report(goal, report_text, charts):
    class PDF(FPDF):
        def header(self):
            self.set_font('Helvetica', 'B', 15)
            self.cell(0, 10, 'Raport Analiza PandasAI', 0, 1, 'C')
            self.ln(5)
            
        def footer(self):
            self.set_y(-15)
            self.set_font('Helvetica', 'I', 8)
            self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

    pdf = PDF()
    pdf.add_page()
    
    # Helper to clean text for Latin-1 (Standard Fonts)
    def clean_text(text):
        # Replace characters not supported in Latin-1
        replacements = {
            'ă': 'a', 'Ă': 'A',
            'ș': 's', 'Ș': 'S',
            'ț': 't', 'Ț': 'T',
            'î': 'i', 'Î': 'I',
            'â': 'a', 'Â': 'A',
            '„': '"', '”': '"',
            '–': '-', '—': '-'
        }
        for char, repl in replacements.items():
            text = text.replace(char, repl)
        return text.encode('latin-1', 'replace').decode('latin-1')

    # Title
    pdf.set_font("Helvetica", "B", 12)
    pdf.multi_cell(0, 10, f"Obiectiv: {clean_text(goal)}")
    pdf.ln(5)
    
    # Content
    pdf.set_font("Helvetica", "", 11)
    
    # Simple Markdown parsing
    lines = report_text.split('\n')
    for line in lines:
        cleaned_line = clean_text(line)
        if line.startswith('# '):
            pdf.set_font("Helvetica", "B", 14)
            pdf.multi_cell(0, 10, cleaned_line.replace('# ', ''))
            pdf.set_font("Helvetica", "", 11)
        elif line.startswith('## '):
            pdf.set_font("Helvetica", "B", 12)
            pdf.multi_cell(0, 10, cleaned_line.replace('## ', ''))
            pdf.set_font("Helvetica", "", 11)
        elif line.startswith('### '):
            pdf.set_font("Helvetica", "B", 11)
            pdf.multi_cell(0, 10, cleaned_line.replace('### ', ''))
            pdf.set_font("Helvetica", "", 11)
        else:
            pdf.multi_cell(0, 6, cleaned_line)
            
    # Charts
    if charts:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "Grafice Generate", 0, 1, 'L')
        pdf.ln(5)
        
        for i, chart_path in enumerate(charts):
            if os.path.exists(chart_path):
                pdf.set_font("Helvetica", "B", 10)
                pdf.cell(0, 10, f"Figura {i+1}", 0, 1, 'L')
                # Calculate width to fit
                pdf.image(chart_path, w=170)
                pdf.ln(10)

    return pdf.output()


# Setup page
setup_page(
    title="Agent de Raportare",
    icon="📝",
    layout="wide"
)

render_header(
    title="📝 Agent de raportare autonom",
    description="Descrie un obiectiv și lasă agentul să planifice, să analizeze și să scrie un raport complet."
)

# Require API key authentication
api_key = require_api_key()

# Load data
df = load_data()
column_info = get_column_info()

# Initialize agent
if "agent_reporter" not in st.session_state:
    with st.spinner("Inițializez Agentul de Raportare..."):
        st.session_state.agent_reporter = get_agent(df, api_key, get_selected_model())

# Initialize direct LLM for text generation tasks
llm_direct = OpenRouterLLM(api_key, get_selected_model())

# Main Interface
st.markdown("""
<div style="background-color: #e8f4f8; padding: 20px; border-radius: 10px; border-left: 5px solid #3498db; margin-bottom: 20px;">
    <h4>🤖 Cum funcționează?</h4>
    <ol>
        <li><strong>Planificare</strong>: Agentul analizează obiectivul tău și creează un plan de întrebări.</li>
        <li><strong>Execuție</strong>: Răspunde la fiecare întrebare folosind datele, generând grafice și analize.</li>
        <li><strong>Sinteză</strong>: Compilează toate informațiile într-un raport final coerent.</li>
    </ol>
</div>
""", unsafe_allow_html=True)

goal = st.text_area(
    "🎯 Obiectivul Raportului:",
    placeholder="Ex: Analizează evoluția economică a României în ultimii 10 ani și compar-o cu media regională.",
    height=100
)

if st.button("🚀 Generează Raport Complet", type="primary"):
    if not goal:
        st.warning("Te rog introdu un obiectiv pentru raport.")
    else:
        report_container = st.container()
        
        # 1. PLANNING PHASE
        with st.status("1️⃣ Planificare...", expanded=True) as status:
            st.write("Analizez obiectivul și generez planul de întrebări...")
            
            planning_prompt = f"""
            Ești un analist de date expert. Obiectivul utilizatorului este: "{goal}".
            Generează o listă de 3-5 întrebări specifice și analitice pe care le putem pune unui sistem PandasAI pentru a atinge acest obiectiv.
            Întrebările trebuie să fie clare, specifice și să poată fi răspunse folosind datele disponibile (GDP, FDI, Internet Users, etc.).
            Returnează DOAR lista de întrebări, fiecare pe o linie nouă, fără numerotare sau alt text.
            """
            
            try:
                # Use direct LLM call for planning (text generation only), bypassing PandasAI code generation
                plan_response = llm_direct._generate_text(planning_prompt)
                
                # Parse questions (assuming string output split by newlines)
                if isinstance(plan_response, str):
                    questions = [q.strip() for q in plan_response.split('\n') if q.strip()]
                    # Limit to 5 questions max to be safe
                    questions = questions[:5]
                else:
                    # Fallback if something weird happens
                    questions = [
                        f"Care este evoluția generală pentru {goal}?",
                        "Care sunt tendințele principale?",
                        "Există corelații interesante?"
                    ]
                
                st.success(f"Plan generat cu {len(questions)} întrebări:")
                for i, q in enumerate(questions, 1):
                    st.write(f"{i}. {q}")
                
                status.update(label="✅ Planificare completă!", state="complete", expanded=False)
                
            except Exception as e:
                st.error(f"Eroare la planificare: {str(e)}")
                st.stop()

        # 2. EXECUTION PHASE
        results = []
        charts = []
        
        with st.status("2️⃣ Execuție Analiză...", expanded=True) as status:
            progress_bar = st.progress(0)
            
            for i, question in enumerate(questions):
                st.write(f"**Analizez:** {question}")
                
                try:
                    # Clean up old chart
                    chart_path = "exports/charts/temp_chart.png"
                    if os.path.exists(chart_path):
                        os.remove(chart_path)
                    
                    # Execute query - this NEEDS code generation, so we use agent.chat()
                    response = st.session_state.agent_reporter.chat(question)
                    
                    # Store result
                    result_entry = {
                        "question": question,
                        "response": str(response),
                        "chart": None
                    }
                    
                    # Check for chart
                    if os.path.exists(chart_path):
                        # Rename chart to save it
                        new_chart_name = f"exports/charts/report_chart_{int(time.time())}_{i}.png"
                        os.rename(chart_path, new_chart_name)
                        result_entry["chart"] = new_chart_name
                        charts.append(new_chart_name)
                        st.image(new_chart_name, caption="Grafic generat", width=400)
                    
                    results.append(result_entry)
                    
                    # Show text result briefly
                    with st.expander("Vezi rezultatul intermediar"):
                        st.write(response)
                        
                except Exception as e:
                    st.error(f"Eroare la întrebarea '{question}': {str(e)}")
                
                progress_bar.progress((i + 1) / len(questions))
            
            status.update(label="✅ Execuție completă!", state="complete", expanded=False)

        # 3. SYNTHESIS PHASE
        with st.status("3️⃣ Redactare Raport...", expanded=True) as status:
            st.write("Sintetizez toate informațiile într-un raport final...")
            
            # Prepare context for the writer
            context = f"Obiectiv Original: {goal}\n\nRezultate Analiză:\n"
            for res in results:
                context += f"\nÎntrebare: {res['question']}\nRăspuns: {res['response']}\n"
            
            writer_prompt = f"""
            Ești un redactor de rapoarte economice profesionist.
            Folosind datele de mai jos, scrie un raport complet în format Markdown.
            
            Structura raportului:
            # Titlu Sugestiv
            ## Rezumat Executiv
            ## Analiză Detaliată (folosește secțiuni pentru fiecare aspect analizat)
            ## Concluzii și Recomandări
            
            Datele:
            {context}
            
            Important:
            - Scrie în limba Română.
            - Fii profesionist și obiectiv.
            - Nu menționa "Agentul" sau "PandasAI", scrie ca și cum ar fi un raport uman.
            - Formatează frumos cu bold, liste, etc.
            """
            
            try:
                # Use direct LLM call for writing (text generation only)
                final_report = llm_direct._generate_text(writer_prompt)
                
                status.update(label="✅ Raport generat!", state="complete", expanded=False)
                
                # Display Final Report
                st.markdown("---")
                st.header("📄 Raport Final")
                
                st.markdown(final_report)
                
                # Display collected charts at the bottom or interleaved if we could (complex)
                # For now, display them in a gallery at the bottom
                if charts:
                    st.subheader("📊 Galerie Grafice")
                    cols = st.columns(2)
                    for idx, chart in enumerate(charts):
                        with cols[idx % 2]:
                            st.image(chart, caption=f"Figura {idx+1}")
                
                # Download buttons
                st.success("Raportul a fost generat! Folosește butoanele de mai jos pentru a-l salva.")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.download_button(
                        label="📥 Descarcă Raport (MD)",
                        data=final_report,
                        file_name="raport_analiza.md",
                        mime="text/markdown"
                    )
                
                with col2:
                    # Generate PDF
                    try:
                        pdf_bytes = create_pdf_report(goal, final_report, charts)
                        st.download_button(
                            label="📄 Descarcă Raport (PDF)",
                            data=bytes(pdf_bytes),
                            file_name="raport_analiza.pdf",
                            mime="application/pdf"
                        )
                    except Exception as e:
                        st.error(f"Eroare la generarea PDF: {str(e)}")
                
            except Exception as e:
                st.error(f"Eroare la redactare: {str(e)}")

render_footer()
