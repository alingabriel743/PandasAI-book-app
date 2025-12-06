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
from utils.config import get_agent, GroqLLM
from utils.auth import require_api_key, get_selected_model
from utils.ui import setup_page, render_header, render_footer


# Initialize session state for report data
if "report_data" not in st.session_state:
    st.session_state.report_data = None

def create_pdf_report(goal, report_text, charts):
    # Determine font paths
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    font_regular = os.path.join(base_path, 'assets', 'fonts', 'NotoSans-Regular.ttf')
    font_bold = os.path.join(base_path, 'assets', 'fonts', 'NotoSans-Bold.ttf')
    
    class PDF(FPDF):
        def __init__(self, font_family='Helvetica', **kwargs):
            super().__init__(**kwargs)
            self.font_family = font_family
            
        def header(self):
            if self.page_no() > 1:
                # Header with line
                self.set_draw_color(200, 200, 200)
                self.line(10, 15, 200, 15)
                
                self.set_font(self.font_family, '', 9)
                self.set_text_color(128, 128, 128)
                self.cell(0, 10, 'Raport Analiza PandasAI', new_x="LMARGIN", new_y="NEXT", align='L')
                self.set_y(10) # Reset Y to align right part
                self.cell(0, 10, f'{time.strftime("%d-%m-%Y")}', new_x="LMARGIN", new_y="NEXT", align='R')
                self.ln(5)
            
        def footer(self):
            self.set_y(-15)
            self.set_font(self.font_family, '', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, f'Pagina {self.page_no()}', align='C')

    # Explicitly set A4 format and margins
    pdf = PDF(orientation='P', unit='mm', format='A4')
    
    # Try to load Unicode Fonts
    font_family = 'Helvetica' # Default fallback
    font_error = None
    
    try:
        if os.path.exists(font_regular) and os.path.exists(font_bold):
            pdf.add_font('NotoSans', '', font_regular)
            pdf.add_font('NotoSans', 'B', font_bold)
            font_family = 'NotoSans'
    except Exception as e:
        font_error = str(e)
        print(f"Font loading error: {e}")
        
    # Set the font family for the instance
    pdf.font_family = font_family
    
    # Helper to clean text
    def clean_text(text):
        if not isinstance(text, str):
            return str(text)
            
        # Common replacements for both fonts (normalization)
        replacements = {
            '„': '"', '”': '"', '“': '"', '’': "'",
            '–': '-', '—': '-', '…': '...',
            '\u2013': '-', '\u2014': '-', '\u2019': "'"
        }
        for char, repl in replacements.items():
            text = text.replace(char, repl)

        # If using Unicode font, return as is
        if font_family == 'NotoSans':
            return text
            
        # If using Helvetica (fallback), replace special chars
        latin_replacements = {
            'ă': 'a', 'Ă': 'A', 'ș': 's', 'Ș': 'S', 'ț': 't', 'Ț': 'T',
            'î': 'i', 'Î': 'I', 'â': 'a', 'Â': 'A'
        }
        for char, repl in latin_replacements.items():
            text = text.replace(char, repl)
            
        # Final safety net for Latin-1
        return text.encode('latin-1', 'replace').decode('latin-1')
        
    pdf.set_margins(left=15, top=15, right=15)
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # --- COVER PAGE ---
    pdf.add_page()
    
    # Decorative line
    pdf.set_draw_color(52, 152, 219) # Blue
    pdf.set_line_width(1)
    pdf.line(20, 60, 190, 60)
    
    pdf.set_font(font_family, 'B', 24)
    pdf.set_text_color(44, 62, 80) # Dark Blue
    pdf.ln(60)
    pdf.cell(0, 15, clean_text("RAPORT DE ANALIZĂ"), new_x="LMARGIN", new_y="NEXT", align='C')
    
    pdf.set_font(font_family, '', 14)
    pdf.set_text_color(50, 50, 50)
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"Obiectiv: {clean_text(goal)}", align='C')
    
    pdf.line(20, 140, 190, 140)
    
    pdf.set_y(240)
    pdf.set_font(font_family, '', 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, f"Generat la: {time.strftime('%d-%m-%Y %H:%M')}", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.cell(0, 8, "Generat de: PandasAI Agent", new_x="LMARGIN", new_y="NEXT", align='C')
    
    # --- CONTENT PAGES ---
    pdf.add_page()
    
    # Content
    pdf.set_font(font_family, "", 11)
    pdf.set_text_color(0, 0, 0)
    
    # Simple Markdown parsing
    lines = report_text.split('\n')
    
    for i, line in enumerate(lines):
        # Clean bold markers for cleaner PDF text
        clean_line_content = line.replace('**', '').replace('__', '')
        cleaned_line = clean_text(clean_line_content)
        
        if not cleaned_line.strip():
            pdf.ln(2) # Small gap for empty lines
            continue
            
        try:
            if line.startswith('# '):
                pdf.ln(8)
                pdf.set_font(font_family, "B", 16)
                pdf.set_text_color(41, 128, 185) # Blue
                pdf.multi_cell(0, 8, cleaned_line.replace('# ', ''), align='L')
                pdf.set_text_color(0, 0, 0)
                pdf.set_font(font_family, "", 11)
                pdf.ln(2)
            elif line.startswith('## '):
                pdf.ln(6)
                pdf.set_font(font_family, "B", 13)
                pdf.set_text_color(52, 73, 94) # Dark Grey/Blue
                pdf.multi_cell(0, 8, cleaned_line.replace('## ', ''), align='L')
                pdf.set_text_color(0, 0, 0)
                pdf.set_font(font_family, "", 11)
                pdf.ln(1)
            elif line.startswith('### '):
                pdf.ln(4)
                pdf.set_font(font_family, "B", 11)
                pdf.set_text_color(0, 0, 0)
                pdf.multi_cell(0, 6, cleaned_line.replace('### ', ''), align='L')
                pdf.set_font(font_family, "", 11)
            elif line.startswith('- '):
                pdf.set_x(25)
                pdf.multi_cell(0, 6, f"•  {cleaned_line.replace('- ', '')}")
                pdf.set_x(20)
            elif line.strip().startswith('|'):
                # Table row - use Monospaced font
                pdf.set_font("Courier", "", 8) # Smaller font for tables
                pdf.multi_cell(0, 4, cleaned_line) # Tighter line height
                pdf.set_font(font_family, "", 11) # Restore
            else:
                # Regular paragraph
                # Try standard rendering
                try:
                    pdf.multi_cell(0, 6, cleaned_line)
                except Exception:
                    # If it fails, try reducing font size
                    pdf.set_font(font_family, "", 10)
                    pdf.multi_cell(0, 6, cleaned_line)
                    pdf.set_font(font_family, "", 11) # Restore
                    
        except Exception:
            # Try to render simplified version
            try:
                safe_line = cleaned_line.encode('latin-1', 'replace').decode('latin-1')
                pdf.set_font('Helvetica', '', 10) # Fallback to core font for this line
                pdf.multi_cell(0, 6, safe_line)
                pdf.set_font(font_family, "", 11) # Restore font
            except:
                pass
            
    # --- CHARTS SECTION ---
    if charts:
        pdf.add_page()
        pdf.set_font(font_family, "B", 16)
        pdf.set_text_color(41, 128, 185)
        pdf.cell(0, 10, clean_text("Anexă: Grafice Generate"), new_x="LMARGIN", new_y="NEXT", align='L')
        pdf.ln(10)
        
        for i, chart_path in enumerate(charts):
            if os.path.exists(chart_path):
                try:
                    if pdf.get_y() > 200:
                        pdf.add_page()
                        
                    pdf.set_font(font_family, "B", 10)
                    pdf.set_text_color(0, 0, 0)
                    pdf.cell(0, 10, f"Figura {i+1}", new_x="LMARGIN", new_y="NEXT", align='L')
                    
                    pdf.image(chart_path, w=160)
                    pdf.ln(10)
                except Exception:
                    pass

    return pdf.output()


# Setup page
setup_page(
    title="Agent de Raportare",
    icon="📝",
    layout="wide"
)

render_header(
    title="📝 Agent de raportare automatizat",
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
llm_direct = GroqLLM(api_key, get_selected_model())

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

# Input for goal
goal = st.text_area(
    "🎯 Obiectivul Raportului:",
    value=st.session_state.report_data["goal"] if st.session_state.report_data else "",
    placeholder="Ex: Analizează evoluția economică a României în ultimii 10 ani și compar-o cu media regională.",
    height=100
)

# Generate button
if st.button("🚀 Generează Raport Complet", type="primary"):
    if not goal:
        st.warning("Te rog introdu un obiectiv pentru raport.")
    else:
        # Reset previous data
        st.session_state.report_data = None
        
        report_container = st.container()
        
        # 1. PLANNING PHASE
        with st.status("1️⃣ Planificare...", expanded=True) as status:
            st.write("Analizez obiectivul și generez planul de întrebări...")
            
            # Prepare context about the dataset
            columns_desc = "\\n".join([f"- {col}: {info['description']} ({info.get('unit', '')})" for col, info in column_info.items()])
            data_sample = df.head(3).to_string(index=False)
            
            planning_prompt = f"""
            Ești un analist de date expert. Obiectivul utilizatorului este: "{goal}".
            
            Ai acces la un dataset cu următoarele coloane:
            {columns_desc}
            
            Mostră de date:
            {data_sample}
            
            Generează o listă de 3-5 întrebări specifice și analitice pe care le putem pune unui sistem PandasAI pentru a atinge acest obiectiv.
            Întrebările trebuie să fie clare, specifice și să poată fi răspunse EXCLUSIV folosind coloanele disponibile.
            Returnează DOAR lista de întrebări, fiecare pe o linie nouă, fără numerotare sau alt text.
            """
            
            try:
                # Use direct LLM call for planning
                plan_response = llm_direct._generate_text(planning_prompt)
                
                if isinstance(plan_response, str):
                    questions = [q.strip() for q in plan_response.split('\n') if q.strip()]
                    questions = questions[:5]
                else:
                    questions = ["Care este evoluția generală?", "Care sunt tendințele?"]
                
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
                    chart_path = "exports/charts/temp_chart.png"
                    if os.path.exists(chart_path):
                        os.remove(chart_path)
                    
                    # Execute query
                    response = st.session_state.agent_reporter.chat(question)
                    
                    result_entry = {
                        "question": question,
                        "response": str(response),
                        "chart": None
                    }
                    
                    if os.path.exists(chart_path):
                        new_chart_name = f"exports/charts/report_chart_{int(time.time())}_{i}.png"
                        os.rename(chart_path, new_chart_name)
                        result_entry["chart"] = new_chart_name
                        charts.append(new_chart_name)
                        st.image(new_chart_name, caption="Grafic generat", width=400)
                    
                    results.append(result_entry)
                    
                    with st.expander("Vezi rezultatul intermediar"):
                        st.write(response)
                        
                except Exception as e:
                    st.error(f"Eroare la întrebarea '{question}': {str(e)}")
                
                progress_bar.progress((i + 1) / len(questions))
            
            status.update(label="✅ Execuție completă!", state="complete", expanded=False)

        # 3. SYNTHESIS PHASE
        with st.status("3️⃣ Redactare Raport...", expanded=True) as status:
            st.write("Sintetizez toate informațiile într-un raport final...")
            
            context = f"Obiectiv Original: {goal}\n\nRezultate Analiză:\n"
            for res in results:
                context += f"\nÎntrebare: {res['question']}\nRăspuns: {res['response']}\n"
            
            writer_prompt = f"""
            Ești un redactor de rapoarte economice de top, specializat în analize macroeconomice profunde.
            Obiectivul tău este să scrii un raport EXTREM DE DETALIAT și VOLUMINOS bazat pe datele de mai jos.
            
            CERINȚĂ DE STIL:
            - **PREFERĂ PARAGRAFELE**: Scrie text cursiv, narativ. Evită listele cu puncte (bullet points) pentru analiza principală.
            - **FOLOSEȘTE BULLET POINTS DOAR UNDE E NECESAR**: Doar pentru enumerări stricte sau recomandări punctuale la final.
            - **VOLUM**: Fiecare secțiune de analiză trebuie să aibă MINIM 400-500 de cuvinte de text continuu.
            
            REGULI DE REDACTARE:
            1. **CONTEXT**: Pentru fiecare cifră, explică ce înseamnă în context economic real. De exemplu, dacă FDI a crescut, discută despre atractivitatea pieței, stabilitate, integrare UE etc.
            2. **COMPARĂ ȘI CONTRASTEAZĂ**: Nu doar enumera valorile. Discută diferențele în fraze complexe. (ex: "În timp ce Grecia a înregistrat o creștere modestă, Turcia a explodat economic datorită...")
            3. **STRUCTURĂ NARATIVĂ**: Folosește conectori logici (În plus, Pe de altă parte, Totuși, În consecință).
            
            Datele de analizat:
            {context}
            
            Te rog să generezi raportul complet respectând următoarea structură:
            
            # [Titlu Profesional și Academic]
            
            ## Rezumat Executiv
            [Un rezumat cuprinzător de minim 300 de cuvinte, scris ca un eseu, nu ca o listă.]
            
            ## Analiză Detaliată a Indicatorilor
            [Aceasta este partea principală. Pentru fiecare întrebare/indicator:]
            ### [Titlu Secțiune]
            [Scrie o analiză profundă de 3-4 paragrafe lungi. Începe cu prezentarea datelor, continuă cu comparația și termină cu interpretarea contextului. NU folosi bullet points aici.]
            
            ## Concluzii și Recomandări Strategice
            [Aici poți folosi o combinație de text introductiv și o listă scurtă de recomandări punctuale.]
            """
            
            try:
                # Use direct LLM call for writing
                final_report = llm_direct._generate_text(writer_prompt)
                
                # SAVE TO SESSION STATE
                st.session_state.report_data = {
                    "goal": goal,
                    "questions": questions,
                    "results": results,
                    "report": final_report,
                    "charts": charts,
                    "timestamp": time.time()
                }
                
                status.update(label="✅ Raport generat!", state="complete", expanded=False)
                st.rerun() # Rerun to display results from session state
                
            except Exception as e:
                st.error(f"Eroare la redactare: {str(e)}")

# Display Report if available in Session State
if st.session_state.report_data:
    data = st.session_state.report_data
    
    st.markdown("---")
    
    # Display Planning Phase (collapsible)
    with st.status("✅ Planificare completă!", state="complete", expanded=False) as status:
        st.info(f"**Obiectiv:** {data['goal']}")
        st.write("**Întrebări generate:**")
        for i, q in enumerate(data.get("questions", []), 1):
            st.write(f"{i}. {q}")
    
    # Display Execution Phase (collapsible)
    with st.status("✅ Execuție completă!", state="complete", expanded=False) as status:
        for res in data.get("results", []):
            with st.expander(f"📊 {res['question']}", expanded=False):
                st.write(res['response'])
                if res.get('chart') and os.path.exists(res['chart']):
                    st.image(res['chart'], width=400)
    
    # Display Synthesis Phase (collapsible)
    with st.status("✅ Raport generat!", state="complete", expanded=False) as status:
        st.markdown(data["report"])
    
    if data["charts"]:
        st.subheader("📊 Galerie Grafice")
        cols = st.columns(2)
        for idx, chart in enumerate(data["charts"]):
            with cols[idx % 2]:
                st.image(chart, caption=f"Figura {idx+1}")
    
    # Download buttons
    st.success("Raportul este gata! Poți descărca rezultatele mai jos.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="📥 Descarcă Raport (MD)",
            data=data["report"],
            file_name="raport_analiza.md",
            mime="text/markdown"
        )
    
    with col2:
        # Generate PDF
        try:
            pdf_bytes = create_pdf_report(data["goal"], data["report"], data["charts"])
            st.download_button(
                label="📄 Descarcă Raport (PDF)",
                data=bytes(pdf_bytes),
                file_name="raport_analiza.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Eroare la generarea PDF: {str(e)}")
    
    if st.button("🔄 Începe o nouă analiză"):
        st.session_state.report_data = None
        st.rerun()

render_footer()
