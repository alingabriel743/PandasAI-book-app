import streamlit as st
from utils.config import test_groq_connection

def init_session_state():
    """Initialize session state variables"""
    if "api_key" not in st.session_state:
        st.session_state.api_key = None
    if "api_key_valid" not in st.session_state:
        st.session_state.api_key_valid = False
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "llama-3.3-70b-versatile"

def show_api_key_input():
    """Show API key input in sidebar if not authenticated"""
    init_session_state()
    
    if not st.session_state.api_key_valid:
        st.sidebar.header("🔐 Autentificare")
        
        api_key_input = st.sidebar.text_input(
            "Groq API Key:",
            type="password",
            key="api_key_input",
            help="Introdu API Key-ul tău Groq pentru a debloca toate funcționalitățile"
        )
        
        if st.sidebar.button("🔓 Validează API key", type="primary"):
            if api_key_input:
                with st.spinner("Validez API Key-ul..."):
                    success, message = test_groq_connection(api_key_input)
                    
                    if success:
                        st.session_state.api_key = api_key_input
                        st.session_state.api_key_valid = True
                        st.sidebar.success("✅ API Key validat cu succes!")
                        st.rerun()
                    else:
                        # Ensure error message is properly displayed
                        error_display = message if message else "Eroare necunoscuta"
                        st.sidebar.error(f"❌ API Key invalid: {error_display}")
            else:
                st.sidebar.warning("Te rog introdu un API Key")
        
        st.sidebar.info("""
        ### 🔑 Cum obții API key:
        
        1. Vizitează [console.groq.com](https://console.groq.com/keys)
        2. Creează cont gratuit
        3. Generează API key
        4. Introdu-l mai sus
        
        **Notă**: API Key-ul va rămâne activ pentru toată sesiunea în toate paginile.
        """)
        
        return False
    else:
        st.sidebar.success("✅ Autentificat")
        st.sidebar.markdown(f"**API Key**: `...{st.session_state.api_key[-8:]}`")
        
        # Model info (single model - no selection needed)
        st.sidebar.markdown("---")
        st.sidebar.subheader("🤖 Model AI")
        st.sidebar.info("**Llama 3.3 70B Versatile**\n\nModel optimizat pentru analiză de date și generare de cod Python/Pandas.")
        
        st.sidebar.markdown("---")
        
        if st.sidebar.button("🔒 Deconectează", type="primary"):
            st.session_state.api_key = None
            st.session_state.api_key_valid = False
            st.rerun()
        
        return True

def require_api_key():
    """Require API key to access page content"""
    init_session_state()
    
    if not show_api_key_input():
        st.warning("⚠️ Te rog autentifică-te cu API Key-ul Groq pentru a accesa această pagină.")
        st.info("""
        ### De ce este necesar API key-ul?
        
        Această aplicație folosește **PandasAI** care necesită acces la modele AI (LLM) 
        pentru a procesa întrebările tale în limbaj natural și a genera analize.
        
        **Groq** oferă inferență ultra-rapidă pentru modele open-source.
        """)
        st.stop()
    
    return st.session_state.api_key

def get_api_key():
    """Get the current API key from session state"""
    init_session_state()
    return st.session_state.api_key

def get_selected_model():
    """Get the currently selected model from session state"""
    init_session_state()
    return st.session_state.selected_model
