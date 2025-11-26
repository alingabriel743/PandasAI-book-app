import streamlit as st
import plotly.express as px
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_loader import load_data, get_column_info, get_country_colors
from utils.ui import setup_page, render_header, render_footer

# Setup page
setup_page(
    title="Explorare generală",
    icon="📈",
    layout="wide"
)

render_header(
    title="📈 Explorare generală a datelor",
    description="Vizualizări și statistici generale despre dataset-ul economic"
)

# Load data
df = load_data()
column_info = get_column_info()
colors = get_country_colors()

# Sidebar filters
st.sidebar.header("🔍 Filtre")
selected_countries = st.sidebar.multiselect(
    "Selectează țări:",
    options=df['Country'].unique(),
    default=df['Country'].unique()
)

year_range = st.sidebar.slider(
    "Interval ani:",
    min_value=int(df['Year'].min()),
    max_value=int(df['Year'].max()),
    value=(int(df['Year'].min()), int(df['Year'].max()))
)

# Filter data
filtered_df = df[
    (df['Country'].isin(selected_countries)) &
    (df['Year'] >= year_range[0]) &
    (df['Year'] <= year_range[1])
]

# Overview metrics
st.header("📊 Statistici generale")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total înregistrări", len(filtered_df))
with col2:
    st.metric("Țări selectate", len(selected_countries))
with col3:
    st.metric("Ani acoperiți", f"{year_range[0]}-{year_range[1]}")
with col4:
    st.metric("Indicatori", len([col for col in df.columns if col not in ['Country', 'Year']]))

st.markdown("---")

# Data preview
st.header("👀 Previzualizare date")
col1, col2 = st.columns([3, 1])

with col1:
    st.dataframe(
        filtered_df.head(20),
        use_container_width=True,
        height=400
    )

with col2:
    st.subheader("Informații coloane")
    for col, info in column_info.items():
        if col in ['Country', 'Year']:
            continue
        with st.expander(f"**{col}** - {info['ro']}"):
            st.write(f"📝 {info['description']}")
            if 'unit' in info:
                st.write(f"📏 Unitate: {info['unit']}")

st.markdown("---")

# Distribution visualizations
st.header("📊 Distribuții și tendințe")

tab1, tab2, tab3 = st.tabs(["📈 Evoluție temporală", "📊 Comparații", "🎯 Distribuții"])

with tab1:
    st.subheader("Evoluția indicatorilor în timp")
    
    indicator = st.selectbox(
        "Selectează indicator:",
        options=['GDP', 'FDI', 'IU', 'MCS', 'PA', 'EF'],
        format_func=lambda x: f"{x} - {column_info[x]['description']}"
    )
    
    fig = px.line(
        filtered_df,
        x='Year',
        y=indicator,
        color='Country',
        markers=True,
        title=f"Evoluția {indicator} ({column_info[indicator]['description']})",
        labels={'Year': 'Anul', indicator: column_info[indicator]['description']},
        color_discrete_map=colors
    )
    
    fig.update_layout(
        hovermode='x unified',
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show statistics
    st.subheader(f"Statistici {indicator}")
    stats_df = filtered_df.groupby('Country')[indicator].agg(['mean', 'min', 'max', 'std']).round(2)
    stats_df.columns = ['Media', 'Minim', 'Maxim', 'Deviație standard']
    st.dataframe(stats_df, use_container_width=True)

with tab2:
    st.subheader("Comparație între țări")
    
    year_to_compare = st.select_slider(
        "Selectează anul pentru comparație:",
        options=sorted(filtered_df['Year'].unique()),
        value=int(filtered_df['Year'].max())
    )
    
    comparison_data = filtered_df[filtered_df['Year'] == year_to_compare]
    
    # Create subplots for all indicators
    indicators = ['GDP', 'FDI', 'IU', 'MCS', 'PA', 'EF']
    
    col1, col2 = st.columns(2)
    
    for idx, indicator in enumerate(indicators):
        with col1 if idx % 2 == 0 else col2:
            fig = px.bar(
                comparison_data,
                x='Country',
                y=indicator,
                title=f"{indicator} - {year_to_compare}",
                labels={'Country': 'Țara', indicator: column_info[indicator]['description']},
                color='Country',
                color_discrete_map=colors
            )
            fig.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Distribuția valorilor")
    
    indicator_dist = st.selectbox(
        "Selectează indicator pentru distribuție:",
        options=['GDP', 'FDI', 'IU', 'MCS', 'PA', 'EF'],
        format_func=lambda x: f"{x} - {column_info[x]['description']}",
        key="dist_indicator"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Histogram
        fig = px.histogram(
            filtered_df,
            x=indicator_dist,
            color='Country',
            marginal='box',
            title=f"Distribuție {indicator_dist}",
            labels={indicator_dist: column_info[indicator_dist]['description']},
            color_discrete_map=colors,
            nbins=30
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Box plot
        fig = px.box(
            filtered_df,
            x='Country',
            y=indicator_dist,
            color='Country',
            title=f"Box Plot {indicator_dist}",
            labels={'Country': 'Țara', indicator_dist: column_info[indicator_dist]['description']},
            color_discrete_map=colors
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Summary statistics
st.header("📈 Statistici descriptive complete")

selected_indicator = st.selectbox(
    "Selectează indicator pentru statistici detaliate:",
    options=['GDP', 'FDI', 'IU', 'MCS', 'PA', 'EF'],
    format_func=lambda x: f"{x} - {column_info[x]['description']}",
    key="stats_indicator"
)

stats_by_country = filtered_df.groupby('Country')[selected_indicator].describe().round(2)
stats_by_country.columns = ['Count', 'Media', 'Dev. std', 'Min', '25%', '50% (Mediană)', '75%', 'Max']

st.dataframe(stats_by_country, use_container_width=True)

# Download filtered data
st.markdown("---")
st.subheader("💾 Descarcă date filtrate")

csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Descarcă CSV",
    data=csv,
    file_name=f"date_economice_{year_range[0]}_{year_range[1]}.csv",
    mime="text/csv"
)

render_footer()
