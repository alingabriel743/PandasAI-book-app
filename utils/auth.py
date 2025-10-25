import streamlit as st
from utils.config import test_openrouter_connection

def init_session_state():
    """Initialize session state variables"""
    if "api_key" not in st.session_state:
        st.session_state.api_key = None
    if "api_key_valid" not in st.session_state:
        st.session_state.api_key_valid = False
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "qwen/qwen-2.5-72b-instruct:free"

def show_api_key_input():
    """Show API key input in sidebar if not authenticated"""
    init_session_state()
    
    if not st.session_state.api_key_valid:
        st.sidebar.header("🔐 Autentificare")
        
        api_key_input = st.sidebar.text_input(
            "OpenRouter API Key:",
            type="password",
            key="api_key_input",
            help="Introdu API Key-ul tău OpenRouter pentru a debloca toate funcționalitățile"
        )
        
        if st.sidebar.button("🔓 Validează API Key", type="primary"):
            if api_key_input:
                with st.spinner("Validez API Key-ul..."):
                    success, message = test_openrouter_connection(api_key_input)
                    
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
        ### 🔑 Cum obții API Key:
        
        1. Vizitează [OpenRouter.ai](https://openrouter.ai/)
        2. Creează cont gratuit
        3. Generează API key
        4. Introdu-l mai sus
        
        **Notă**: API Key-ul va rămâne activ pentru toată sesiunea în toate paginile.
        """)
        
        return False
    else:
        st.sidebar.success("✅ Autentificat")
        st.sidebar.markdown(f"**API Key**: `...{st.session_state.api_key[-8:]}`")
        
        # Model selection
        st.sidebar.markdown("---")
        st.sidebar.subheader("🤖 Selectare Model")
        
        model_options = {
            "Qwen2.5 72B Instruct": "qwen/qwen-2.5-72b-instruct:free",
            "Meta: Llama 3.3 70B Instruct": "meta-llama/llama-3.3-70b-instruct:free"
        }
        
        # Find current model display name
        current_model_display = None
        for display_name, model_id in model_options.items():
            if model_id == st.session_state.selected_model:
                current_model_display = display_name
                break
        
        if current_model_display is None:
            current_model_display = list(model_options.keys())[0]
        
        selected_display = st.sidebar.selectbox(
            "Alege modelul AI:",
            options=list(model_options.keys()),
            index=list(model_options.keys()).index(current_model_display),
            help="Selectează modelul AI care va procesa întrebările tale"
        )
        
        # Update selected model if changed
        new_model = model_options[selected_display]
        if new_model != st.session_state.selected_model:
            st.session_state.selected_model = new_model
            # Clear agents to force recreation with new model
            if "agent" in st.session_state:
                del st.session_state.agent
            if "agent_advanced" in st.session_state:
                del st.session_state.agent_advanced
            if "agent_examples" in st.session_state:
                del st.session_state.agent_examples
            st.rerun()
        
        st.sidebar.markdown("---")
        
        if st.sidebar.button("🔒 Deconectează", type="secondary"):
            st.session_state.api_key = None
            st.session_state.api_key_valid = False
            st.rerun()
        
        return True

def require_api_key():
    """Require API key to access page content"""
    init_session_state()
    
    if not show_api_key_input():
        st.warning("⚠️ Te rog autentifică-te cu API Key-ul OpenRouter pentru a accesa această pagină.")
        st.info("""
        ### De ce este necesar API Key-ul?
        
        Această aplicație folosește **PandasAI** care necesită acces la modele AI (LLM) 
        pentru a procesa întrebările tale în limbaj natural și a genera analize.
        
        **OpenRouter** oferă acces **gratuit** la modele precum Llama 3.3 70B.
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
