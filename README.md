# PandasAI Demo Application

A multi-page Streamlit application demonstrating **PandasAI** capabilities for economic data analysis.

## About the Project

This application was developed as demonstration material for a **book chapter about PandasAI**. It showcases the PandasAI library capabilities using a real economic dataset containing indicators for Romania, Bulgaria, Turkey, and Greece (1990-2023).

## What is PandasAI?

**PandasAI** is a Python library that adds generative AI capabilities to pandas DataFrames, enabling:

- Queries in **natural language**
- **Automatic visualization** generation
- **Complex analyses** without code
- **Instant insights** from data

## Dataset

The dataset contains the following **economic indicators**:

| Indicator | Description | Unit |
|-----------|-------------|------|
| **GDP** | Gross Domestic Product per capita | USD |
| **FDI** | Foreign Direct Investment | % of GDP |
| **IU** | Internet Users | % of population |
| **MCS** | Mobile Cellular Subscriptions | per 100 people |
| **PA** | Patent Applications | number of applications |
| **EF** | Economic Freedom Index | index (0-10) |

**Period**: 1990-2023  
**Countries**: Romania, Bulgaria, Turkey, Greece  
**Total records**: 136 (34 years x 4 countries)

## Installation and Configuration

### Requirements

- Python 3.8+
- pip

### Installation Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd PandasAI
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Get Groq API Key**
   - Visit [https://console.groq.com/](https://console.groq.com/)
   - Create a free account
   - Generate an API key
   - Groq offers ultra-fast inference for open-source models

4. **Run the application**
```bash
streamlit run app.py
```

5. **Access the application**
   - Open browser at `http://localhost:8501`
   - Enter API Key in the sidebar
   - Start exploring!

## Application Structure

### Main Pages

#### **Home Page** (`app.py`)
- Introduction to PandasAI
- Dataset presentation
- Quick start guide
- Navigation to features

#### **1. General Exploration**
- General descriptive statistics
- Interactive visualizations (Plotly)
- Dynamic filters for countries and periods
- Visual comparisons between indicators
- Filtered data export

#### **2. Chat with PandasAI**
- **Conversational interface** with PandasAI
- Natural language queries (Romanian/English)
- Conversation history
- Predefined example questions
- Text, table, and chart responses

**Example questions:**
- "What is the average GDP for Romania?"
- "Compare Internet Users between all countries in 2023"
- "Create a chart with FDI evolution for Bulgaria"
- "Which country has the highest Patent Applications growth?"

#### **3. Analysis with PandasAI**
- **Descriptive Statistics**: Mean, median, standard deviation
- **Correlations and Relationships**: Identify dependencies between variables
- **Comparative Analysis**: Compare countries and periods
- **Predictions and Trends**: Temporal patterns
- **Complex Analysis**: Multi-dimensional queries

#### **4. PandasAI Examples Gallery**
- **24+ practical examples** organized by categories
- One-click executable examples
- Execution history
- Custom query section
- Tips and best practices

**Example categories:**
- Simple Calculations
- Aggregations and Groupings
- Temporal Analysis
- Correlations
- Comparisons
- Visualizations
- Complex Filters
- Advanced Calculations

#### **5. Reporting Agent**
- **Automated report generation** from a research objective
- Multi-step agentic workflow: Planning, Execution, Synthesis
- PDF export with professional formatting
- Chart gallery integration

## Technologies Used

- **Streamlit**: Web application framework
- **PandasAI**: AI-powered data analysis
- **Pandas**: Data manipulation
- **Plotly**: Interactive visualizations
- **Groq**: API for fast LLM inference
- **FPDF2**: PDF generation
- **Python 3.8+**: Programming language

## Usage Examples

### Example 1: Simple Question
```
Question: "What is the average GDP for Romania?"
Response: PandasAI automatically calculates the mean and returns the value
```

### Example 2: Comparison
```
Question: "Compare average GDP between Romania and Bulgaria"
Response: Comparative table with mean values for both countries
```

### Example 3: Visualization
```
Question: "Create a chart with Internet Users evolution for all countries"
Response: Automatically generated line chart with time evolution
```

### Example 4: Complex Analysis
```
Question: "What is the correlation between GDP and Internet Users for each country?"
Response: Table with correlation coefficients for each country
```

## Demonstrated Concepts

The application demonstrates the following **PandasAI capabilities**:

### 1. **Natural Language Processing**
- Understanding natural language questions
- Context and intent processing
- Multilingual support (Romanian/English)

### 2. **Automatic Code Generation**
- Transforming questions into Pandas code
- Operation optimization
- Edge case handling

### 3. **Statistical Analysis**
- Descriptive statistics
- Correlations and relationships
- Complex aggregations
- Filtering and sorting

### 4. **Automatic Visualizations**
- Automatic chart type selection
- Relevant chart generation
- Formatting and styling

### 5. **Contextual Intelligence**
- Dataset context understanding
- Adaptation to data types
- Relevant suggestions

## File Structure

```
PandasAI/
├── app.py                          # Main page
├── requirements.txt                # Python dependencies
├── README.md                       # Documentation
├── digi.csv                        # Economic dataset
├── utils/
│   ├── config.py                   # PandasAI and Groq configuration
│   ├── auth.py                     # API key authentication
│   ├── ui.py                       # UI components
│   └── data_loader.py              # Data loading functions
├── pages/
│   ├── 1_Explorare_Generala.py
│   ├── 2_Chat_cu_PandasAI.py
│   ├── 3_Analiza_cu_PandasAI.py
│   ├── 4_Exemple_PandasAI.py
│   └── 5_Agent_Raportare.py
├── exports/
│   └── charts/                     # Generated charts
└── cache/                          # PandasAI cache
```

## Advanced Configuration

### LLM Model Customization

In `utils/config.py`, you can modify the model used:

```python
llm = GroqLLM(
    api_token=api_key,
    model="llama-3.3-70b-versatile"  # Modify here
)
```

### Available Models (Groq)
- `llama-3.3-70b-versatile` (recommended)
- `llama3-70b-8192`
- `mixtral-8x7b-32768`

## Usage Tips

### Effective Questions

**Best Practices:**
- Be specific: "Average GDP for Romania" vs "GDP Romania"
- Specify period: "between 2010 and 2020"
- Request visualizations: "Create a chart..."
- Use clear terms: "compare", "calculate", "show"

**Things to Avoid:**
- Vague questions: "Tell me about the data"
- Too many simultaneous requirements
- Ambiguous terms without context
- Implicit assumptions

### Debugging

If you encounter problems:
1. Rephrase the question more simply
2. Check column names
3. Split complex questions into simpler ones
4. Verify the API Key

## Contributions

This project is developed as educational material for a book chapter about PandasAI.

## License

This project is developed for educational purposes.

## Contact

For questions or suggestions about the application, please open an issue in the repository.

---

**Developed for demonstrating PandasAI capabilities**
