# 📊 Aplicație Demonstrativă PandasAI

Aplicație multi-pagină Streamlit pentru demonstrarea capacităților **PandasAI** în analiza datelor economice.

## 🎯 Despre Proiect

Această aplicație este dezvoltată ca material demonstrativ pentru un **capitol de carte despre PandasAI**. Prezintă capacitățile bibliotecii PandasAI în analiza unui dataset economic real, conținând indicatori pentru România, Bulgaria, Turcia și Grecia (1990-2023).

## 🤖 Ce este PandasAI?

**PandasAI** este o bibliotecă Python care adaugă capabilități de AI generativ la pandas DataFrames, permițând:

- 💬 Interogări în **limbaj natural**
- 📊 Generare **automată de vizualizări**
- 🔍 **Analize complexe** fără cod
- 📈 **Insights instant** din date

## 📚 Dataset

Dataset-ul conține următorii **indicatori economici**:

| Indicator | Descriere | Unitate |
|-----------|-----------|---------|
| **GDP** | Produsul Intern Brut per capita | USD |
| **FDI** | Foreign Direct Investment | % din PIB |
| **IU** | Internet Users | % din populație |
| **MCS** | Mobile Cellular Subscriptions | per 100 persoane |
| **PA** | Patent Applications | număr aplicații |
| **EF** | Economic Freedom Index | index (0-10) |

**Perioada**: 1990-2023  
**Țări**: România, Bulgaria, Turcia, Grecia  
**Total înregistrări**: 136 (34 ani × 4 țări)

## 🚀 Instalare și Configurare

### Cerințe

- Python 3.8+
- pip

### Pași de Instalare

1. **Clonează repository-ul**
```bash
git clone <repository-url>
cd PandasAI
```

2. **Instalează dependențele**
```bash
pip install -r requirements.txt
```

5. **Obține API Key Groq**
   - Vizitează [https://console.groq.com/](https://console.groq.com/)
   - Creează un cont gratuit
   - Generează un API key
   - Groq oferă inferență ultra-rapidă pentru modele open-source

4. **Rulează aplicația**
```bash
streamlit run app.py
```

5. **Accesează aplicația**
   - Deschide browser-ul la `http://localhost:8501`
   - Introdu API Key-ul în bara laterală
   - Începe să explorezi!

## 📱 Structura Aplicației

### Pagini Principale

#### 🏠 **Pagina Principală** (`app.py`)
- Introducere în PandasAI
- Prezentare dataset
- Ghid de utilizare rapidă
- Navigare către funcționalități

#### 📈 **1. Explorare Generală**
- Statistici descriptive generale
- Vizualizări interactive (Plotly)
- Filtre dinamice pentru țări și perioade
- Comparații vizuale între indicatori
- Export date filtrate

#### 🤖 **2. Chat cu PandasAI**
- **Interfață conversațională** cu PandasAI
- Întrebări în limbaj natural (română/engleză)
- Istoric conversație
- Exemple de întrebări predefinite
- Răspunsuri text, tabele și grafice

**Exemple de întrebări:**
- "Care este media GDP pentru România?"
- "Compară Internet Users între toate țările în 2023"
- "Creează un grafic cu evoluția FDI pentru Bulgaria"
- "Care țară are cea mai mare creștere a Patent Applications?"

#### 📊 **3. Analiză Comparativă**
- Comparații anuale între țări
- Comparații pe perioade de timp
- Analiză multi-indicator
- Grafice radar și heatmap
- Rankings și clasamente

#### 📉 **4. Analiză Temporală**
- Tendințe generale în timp
- Analiză rate de creștere
- Comparații între perioade
- Medii mobile
- Analiză pe decade

#### 🔍 **5. Analiză cu PandasAI**
- **Statistici Descriptive**: Media, mediana, deviație standard
- **Corelații și Relații**: Identifică dependențe între variabile
- **Analiză Comparativă**: Compară țări și perioade
- **Predicții și Tendințe**: Pattern-uri temporale
- **Analiză Complexă**: Întrebări multi-dimensionale

#### 📋 **6. Galerie Exemple PandasAI**
- **24+ exemple practice** organizate pe categorii
- Exemple executabile cu un click
- Istoric execuții
- Secțiune pentru întrebări personalizate
- Sfaturi și best practices

**Categorii de exemple:**
- 🔢 Calcule Simple
- 📊 Agregări și Grupări
- 📈 Analiză Temporală
- 🔗 Corelații
- ⚖️ Comparații
- 📉 Vizualizări
- 🔍 Filtrări Complexe
- 🧮 Calcule Avansate

## 🛠️ Tehnologii Utilizate

- **Streamlit**: Framework pentru aplicații web
- **PandasAI**: Analiză date cu AI
- **Pandas**: Manipulare date
- **Plotly**: Vizualizări interactive
- **Groq**: API pentru modele LLM rapide
- **Python 3.8+**: Limbaj de programare

## 📖 Exemple de Utilizare

### Exemplu 1: Întrebare Simplă
```
Întrebare: "Care este media GDP pentru România?"
Răspuns: PandasAI calculează automat media și returnează valoarea
```

### Exemplu 2: Comparație
```
Întrebare: "Compară GDP-ul mediu între România și Bulgaria"
Răspuns: Tabel comparativ cu valorile medii pentru ambele țări
```

### Exemplu 3: Vizualizare
```
Întrebare: "Creează un grafic cu evoluția Internet Users pentru toate țările"
Răspuns: Grafic line chart generat automat cu evoluția în timp
```

### Exemplu 4: Analiză Complexă
```
Întrebare: "Care este corelația dintre GDP și Internet Users pentru fiecare țară?"
Răspuns: Tabel cu coeficienți de corelație pentru fiecare țară
```

## 🎓 Concepte Demonstrate

Aplicația demonstrează următoarele **capabilități ale PandasAI**:

### 1. **Natural Language Processing**
- Înțelegere întrebări în limbaj natural
- Procesare context și intenție
- Suport multilingv (română/engleză)

### 2. **Generare Automată de Cod**
- Transformare întrebări în cod Pandas
- Optimizare operații
- Gestionare edge cases

### 3. **Analiză Statistică**
- Statistici descriptive
- Corelații și relații
- Agregări complexe
- Filtrări și sortări

### 4. **Vizualizări Automate**
- Selecție automată tip grafic
- Generare chart-uri relevante
- Formatare și stilizare

### 5. **Inteligență Contextuală**
- Înțelegere context dataset
- Adaptare la tipul datelor
- Sugestii relevante

## 📝 Structura Fișierelor

```
PandasAI/
├── app.py                          # Pagina principală
├── requirements.txt                # Dependențe Python
├── README.md                       # Documentație
├── digi.csv                        # Dataset economic
├── utils/
│   ├── config.py                   # Configurare PandasAI și Groq
│   └── data_loader.py              # Funcții încărcare date
├── pages/
│   ├── 1_📈_Explorare_Generala.py
│   ├── 2_🤖_Chat_cu_PandasAI.py
│   ├── 3_📊_Analiza_Comparativa.py
│   ├── 4_📉_Analiza_Temporala.py
│   ├── 5_🔍_Analiza_cu_PandasAI.py
│   └── 6_📋_Exemple_PandasAI.py
├── exports/
│   └── charts/                     # Grafice generate
└── cache/                          # Cache PandasAI
```

## 🔧 Configurare Avansată

### Personalizare Model LLM

În `utils/config.py`, poți modifica modelul folosit:

```python
llm = GroqLLM(
    api_token=api_key,
    model="llama3-70b-8192"  # Modifică aici
)
```

### Modele Disponibile (Groq)
- `llama-3.3-70b-versatile`
- `llama3-70b-8192`
- `mixtral-8x7b-32768`

## 💡 Sfaturi pentru Utilizare

### Întrebări Eficiente

✅ **Bune Practici:**
- Fii specific: "Media GDP pentru România" vs "GDP România"
- Specifică perioada: "între 2010 și 2020"
- Cere vizualizări: "Creează un grafic..."
- Folosește termeni clari: "compară", "calculează", "arată"

❌ **De Evitat:**
- Întrebări vagi: "Spune-mi despre date"
- Prea multe cerințe simultan
- Termeni ambigui fără context
- Presupuneri implicite

### Debugging

Dacă întâmpini probleme:
1. Reformulează întrebarea mai simplu
2. Verifică numele coloanelor
3. Împarte întrebări complexe în mai multe simple
4. Verifică API Key-ul

## 🤝 Contribuții

Acest proiect este dezvoltat ca material educațional pentru un capitol de carte despre PandasAI.

## 📄 Licență

Acest proiect este dezvoltat în scop educațional.

## 📧 Contact

Pentru întrebări sau sugestii legate de aplicație, te rog deschide un issue în repository.

---

**Dezvoltat cu ❤️ pentru demonstrarea capacităților PandasAI**
