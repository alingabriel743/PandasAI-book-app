import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    """Load and prepare the economic data"""
    df = pd.read_csv('digi.csv')
    
    # Convert columns with mixed types to float
    numeric_columns = ['GDP', 'FDI', 'IU', 'MCS', 'PA', 'EF']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

def get_column_info():
    """Return information about dataset columns"""
    return {
        "Country": {
            "ro": "Țara",
            "description": "Numele țării",
            "type": "categorical"
        },
        "Year": {
            "ro": "Anul",
            "description": "Anul observației",
            "type": "temporal"
        },
        "GDP": {
            "ro": "PIB",
            "description": "Produsul Intern Brut per capita (USD)",
            "type": "numeric",
            "unit": "USD"
        },
        "FDI": {
            "ro": "FDI",
            "description": "Foreign Direct Investment (% din PIB)",
            "type": "numeric",
            "unit": "%"
        },
        "IU": {
            "ro": "IU",
            "description": "Internet Users (% din populație)",
            "type": "numeric",
            "unit": "%"
        },
        "MCS": {
            "ro": "MCS",
            "description": "Mobile Cellular Subscriptions (per 100 persoane)",
            "type": "numeric",
            "unit": "per 100"
        },
        "PA": {
            "ro": "PA",
            "description": "Patent Applications (aplicații de brevete)",
            "type": "numeric",
            "unit": "count"
        },
        "EF": {
            "ro": "EF",
            "description": "Economic Freedom Index",
            "type": "numeric",
            "unit": "index"
        }
    }

def get_country_colors():
    """Return consistent colors for each country"""
    return {
        "Romania": "#0038A8",  # Blue
        "Bulgaria": "#00966E",  # Green
        "Turkey": "#E30A17",    # Red
        "Greece": "#0D5EAF"     # Blue
    }

def filter_data(df, countries=None, years=None, indicators=None):
    """Filter dataframe based on selections"""
    filtered_df = df.copy()
    
    if countries:
        filtered_df = filtered_df[filtered_df['Country'].isin(countries)]
    
    if years:
        filtered_df = filtered_df[
            (filtered_df['Year'] >= years[0]) & 
            (filtered_df['Year'] <= years[1])
        ]
    
    if indicators:
        cols_to_keep = ['Country', 'Year'] + indicators
        filtered_df = filtered_df[cols_to_keep]
    
    return filtered_df
