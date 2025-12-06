# PandasAI Streamlit Application - Project Documentation

## Project Overview

**Project Name**: PandasAI Demonstrative Application  
**Project Type**: Multi-page Streamlit Web Application  
**Domain**: Data Analysis & AI-powered Analytics  
**Purpose**: Educational demonstration of PandasAI capabilities for analyzing economic data from Southeast European countries (Romania, Bulgaria, Turkey, Greece) spanning 1990-2023

## Technology Stack

### Core Technologies
- **Python**: 3.8+ (primary language)
- **Streamlit**: >=1.28.0 (web framework for multi-page app)
- **PandasAI**: >=2.0.0 (AI-powered data analysis)
- **Pandas**: >=2.0.0 (data manipulation)
- **OpenAI**: >=1.0.0 (API client for LLM integration)

### Visualization Libraries
- **Plotly**: >=5.17.0 (interactive charts)
- **Matplotlib**: >=3.7.0 (static visualizations)
- **Kaleido**: >=0.2.1 (static image export)

### Scientific Computing
- **NumPy**: >=1.24.0 (numerical operations)
- **SciPy**: >=1.11.0 (scientific computing)

### Utilities
- **python-dotenv**: >=1.0.0 (environment variables)
- **openpyxl**: >=3.1.0 (Excel file support)

## Project Structure

```
PandasAI/
├── app.py                          # Main entry point & home page
├── requirements.txt                # Python dependencies
├── README.md                       # User documentation
├── digi.csv                        # Economic dataset (1990-2023)
├── start_app.sh                    # Shell script to launch app
├── .gitignore                      # Git ignore rules
├── utils/                          # Utility modules
│   ├── auth.py                     # API key authentication & session management
│   ├── config.py                   # PandasAI agent configuration & OpenRouter LLM
│   └── data_loader.py              # Data loading and column metadata
├── pages/                          # Streamlit multi-page structure
│   ├── 1_📈_Explorare_Generala.py  # General data exploration
│   ├── 2_🤖_Chat_cu_PandasAI.py    # Natural language chat interface
│   ├── 3_🔍_Analiza_cu_PandasAI.py # Advanced AI-powered analysis
│   └── 4_📋_Exemple_PandasAI.py    # Example queries gallery
├── exports/                        # Generated outputs
│   └── charts/                     # Auto-generated visualizations
└── cache/                          # PandasAI cache (disabled in config)
```

## Architecture & Design Patterns

### Application Architecture
- **Multi-Page Application**: Streamlit's native multi-page structure
- **Session State Management**: Centralized state in `st.session_state`
- **Modular Design**: Utilities separated into dedicated modules
- **API-First**: External LLM via Groq API (not local models)

### Key Architectural Decisions
1. **Groq Integration**: Uses Groq API for ultra-fast LLM access
2. **Stateless Agent Creation**: PandasAI agents created per session with cache disabled
3. **Chart Management**: Temporary charts with unique timestamps for history
4. **Authentication Flow**: API key validation before page access

## Code Organization Conventions

### File Naming
- **Main app**: `app.py` (entry point)
- **Pages**: Numbered with emoji prefixes (e.g., `1_📈_Explorare_Generala.py`)
- **Utilities**: Lowercase with underscores (e.g., `data_loader.py`)

### Module Structure
- **utils/auth.py**: Authentication, session state, model selection
- **utils/config.py**: LLM configuration, PandasAI agent creation
- **utils/data_loader.py**: Data loading, column metadata

### Import Patterns
```python
# Standard library
import os
import sys

# Third-party
import streamlit as st
import pandas as pd

# Local utilities (with path manipulation for pages)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.auth import require_api_key, get_selected_model
from utils.config import get_agent
from utils.data_loader import load_data
```

### Path Aliases
- No custom path aliases
- Pages use `sys.path.append()` to access parent directory utilities

## State Management

### Session State Variables
```python
# Authentication
st.session_state.api_key          # Groq API key
st.session_state.api_key_valid    # Boolean validation status
st.session_state.selected_model   # Current LLM model ID

# PandasAI Agents (per page)
st.session_state.agent            # Chat page agent
st.session_state.agent_advanced   # Advanced analysis agent
st.session_state.agent_examples   # Examples page agent

# Chat History
st.session_state.messages         # List of chat messages with images
st.session_state.current_query    # Temporary query from example buttons
```

### State Initialization Pattern
```python
def init_session_state():
    """Initialize session state variables"""
    if "api_key" not in st.session_state:
        st.session_state.api_key = None
    if "api_key_valid" not in st.session_state:
        st.session_state.api_key_valid = False
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "llama-3.3-70b-versatile"
```

## LLM Integration (Groq)

### Custom LLM Class
```python
class OpenRouterLLM(BaseOpenAI):
    """Custom Groq LLM for PandasAI integration"""
```

**Key Features**:
- Inherits from `pandasai.llm.base.BaseOpenAI`
- Uses OpenAI client with Groq base URL
- Implements `_generate_text()` method
- Provides mock client for PandasAI compatibility

### Available Models
1. **Llama 3.3 70B Versatile (Groq)** (default): `llama-3.3-70b-versatile`
2. **Llama 3 70B (Groq)**: `llama3-70b-8192`
3. **Mixtral 8x7B (Groq)**: `mixtral-8x7b-32768`

**IMPORTANT**: These are API-accessed models via Groq, NOT local llama.cpp models

### Agent Configuration
```python
agent = Agent(df, config={
    "llm": llm, 
    "verbose": True,
    "enable_cache": False  # Disabled to avoid DuckDB lock issues
})
```

## Error Handling Patterns

### API Connection Testing
```python
def test_openrouter_connection(api_key):
    """Test OpenRouter connection with proper error handling"""
    try:
        # Test API call
        response = client.chat.completions.create(...)
        return True, response_content.encode('utf-8', errors='ignore').decode('utf-8')
    except Exception as e:
        error_msg = str(e).encode('utf-8', errors='ignore').decode('utf-8')
        return False, error_msg
```

### PandasAI Query Handling
```python
try:
    response = st.session_state.agent.chat(prompt)
    # Handle different response types
    if isinstance(response, str):
        st.markdown(response)
    elif isinstance(response, (pd.DataFrame, pd.Series)):
        st.dataframe(response)
except Exception as e:
    st.error(f"❌ Eroare: {str(e)}")
    st.info("Încearcă să reformulezi întrebarea")
```

## Chart Management

### Temporary Chart Handling
```python
chart_path = "exports/charts/temp_chart.png"

# Delete old chart before new query
if os.path.exists(chart_path):
    os.remove(chart_path)

# After query, save unique copy for history
unique_chart_path = f"exports/charts/chart_{int(time.time() * 1000)}.png"
shutil.copy2(chart_path, unique_chart_path)
```

## Data Model

### Dataset Structure
- **File**: `digi.csv`
- **Columns**: Country, Year, GDP, FDI, IU, MCS, PA, EF
- **Period**: 1990-2023 (34 years)
- **Countries**: Romania, Bulgaria, Turkey, Greece
- **Total Records**: 136 (34 years × 4 countries)

### Column Metadata
```python
COLUMN_INFO = {
    'Country': {'description': 'Țara', 'unit': ''},
    'Year': {'description': 'Anul', 'unit': ''},
    'GDP': {'description': 'PIB per capita', 'unit': 'USD'},
    'FDI': {'description': 'Foreign Direct Investment', 'unit': '% din PIB'},
    'IU': {'description': 'Internet Users', 'unit': '% din populație'},
    'MCS': {'description': 'Mobile Cellular Subscriptions', 'unit': 'per 100 persoane'},
    'PA': {'description': 'Patent Applications', 'unit': 'număr'},
    'EF': {'description': 'Economic Freedom Index', 'unit': 'index'}
}
```

## Testing Conventions

- No formal test framework currently implemented
- Manual testing through Streamlit interface
- API connection tested via `test_groq_connection()`

## Build & Development Workflow

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py

# Or use shell script
./start_app.sh
```

### Environment Variables
- API keys stored in session state (not environment variables)
- No `.env` file required (python-dotenv installed but not used)

## Key Dependencies & Purposes

### Core Dependencies
- **streamlit**: Web application framework, multi-page support
- **pandasai**: AI-powered data analysis, natural language queries
- **pandas**: Data manipulation, DataFrame operations
- **openai**: API client for Groq LLM access

### Visualization
- **plotly**: Interactive charts (line, bar, scatter, heatmap)
- **matplotlib**: Static visualizations, PandasAI chart generation
- **kaleido**: Export Plotly charts to static images

### Scientific
- **numpy**: Numerical operations, array handling
- **scipy**: Statistical functions, correlations

## Common Patterns

### Page Structure Pattern
```python
# 1. Imports with path manipulation
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 2. Page configuration
st.set_page_config(page_title="...", page_icon="...", layout="wide")

# 3. Authentication requirement
api_key = require_api_key()

# 4. Data loading
df = load_data()

# 5. Agent initialization (if needed)
if "agent" not in st.session_state:
    st.session_state.agent = get_agent(df, api_key, get_selected_model())

# 6. Page content
st.title("...")
# ... page-specific content
```

### Authentication Pattern
```python
# In sidebar (all pages)
show_api_key_input()  # Shows input or authenticated status

# In page content (protected pages)
api_key = require_api_key()  # Stops execution if not authenticated
```

### Model Selection Pattern
```python
# User selects model in sidebar
model_options = {
    "Llama 3.3 70B Versatile (Groq)": "llama-3.3-70b-versatile",
    "Llama 3 70B (Groq)": "llama3-70b-8192"
}

# On model change, clear all agents to force recreation
if new_model != st.session_state.selected_model:
    st.session_state.selected_model = new_model
    if "agent" in st.session_state:
        del st.session_state.agent
    # ... delete other agents
    st.rerun()
```

## File Modification Guidelines

### When Modifying utils/config.py
- Maintain `OpenRouterLLM` class structure
- Keep `BaseOpenAI` inheritance
- Keep `BaseOpenAI` inheritance
- Preserve mock client pattern for PandasAI compatibility
- Update model list in both config.py and auth.py

### When Modifying utils/auth.py
- Keep session state initialization consistent
- Maintain model selection synchronization
- Preserve agent cleanup on model change
- Keep API key validation flow

### When Adding New Pages
- Follow naming convention: `N_emoji_Name.py`
- Include path manipulation for imports
- Use `require_api_key()` for protected pages
- Create separate agent in session state if needed

### When Modifying Data Loading
- Update `COLUMN_INFO` in data_loader.py
- Maintain column name consistency
- Update documentation in README.md

## Integration Points

### Streamlit ↔ PandasAI
- Agent created with DataFrame and LLM config
- Queries via `agent.chat(prompt)`
- Responses: str, DataFrame, Series, or chart files

### PandasAI ↔ Groq
- Custom `OpenRouterLLM` class bridges the gap
- Implements PandasAI's `BaseOpenAI` interface
- Uses OpenAI client with Groq base URL

### Session State ↔ Pages
- Shared authentication state across pages
- Separate agents per page to avoid conflicts
- Model selection affects all agents

## Project-Specific Idioms

### Romanian Language Support
- UI text primarily in Romanian
- Supports Romanian queries to PandasAI
- Column descriptions in Romanian

### Chart Export Pattern
```python
# PandasAI saves to: exports/charts/temp_chart.png
# App copies to: exports/charts/chart_{timestamp}.png
```

### Agent Recreation Pattern
```python
# Agents are NOT reused across sessions
# Each page creates its own agent
# Cache disabled to avoid DuckDB locks
```

### Error Message Encoding
```python
# All error messages encoded to handle special characters
error_msg = str(e).encode('utf-8', errors='ignore').decode('utf-8')
```

## Important Notes

1. **NO llama.cpp Integration**: Despite model names containing "llama", this project uses Groq API, NOT local llama.cpp library
2. **Cache Disabled**: PandasAI cache disabled to prevent DuckDB lock issues in multi-session Streamlit environment
3. **Stateless Agents**: Agents recreated per session, not persisted
4. **Chart Cleanup**: Old charts deleted before new queries to prevent accumulation
5. **UTF-8 Handling**: Explicit UTF-8 encoding/decoding for Romanian characters
6. **Model Selection**: Changing model clears all agents to force recreation with new model

## Development Best Practices

1. **Always test API key validation** before deploying changes
2. **Clear session state** when changing agent configuration
3. **Handle chart file existence** before displaying
4. **Encode/decode UTF-8** for all user-facing text
5. **Use `st.rerun()`** after session state changes that affect UI
6. **Disable cache** in PandasAI config for Streamlit apps
7. **Create separate agents** for different pages to avoid conflicts
