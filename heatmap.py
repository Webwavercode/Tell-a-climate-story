import streamlit as st
from streamlit_jupyter import StreamlitPatcher, tqdm

# Patch Streamlit to work with Jupyter Notebook
StreamlitPatcher().jupyter()

# Rest of your code remains the same
import plotly.express as px
import pandas as pd

@st.cache_data
def get_data(file_name):
    return pd.read_csv(file_name)

@st.cache_data
def get_co_data(): 
    file_name = "co-emissions-per-capita.csv"
    return get_data(file_name)

@st.cache_data
def get_methane_data():
    file_name = "per-capita-methane-emissions.csv"
    return get_data(file_name)

@st.cache_data
def get_nitrous_oxide_data():
    file_name = "per-capita-nitrous-oxide.csv"
    return get_data(file_name)

st.set_page_config(layout = "wide")

df_co = get_co_data()
df_co = df_co.rename(columns={'Year': 'year', 'Entity': 'country', 'Code': 'iso_code', 'Annual CO₂ emissions (per capita)': 'co_per_capita'})

df_methane = get_methane_data()
df_methane = df_methane.rename(columns={'Year': 'year', 'Entity': 'country', 'Code': 'iso_code', 'Per-capita methane emissions in CO₂ equivalents': 'methane_emissions'})

df_nitrous_oxide = get_nitrous_oxide_data()
df_nitrous_oxide = df_nitrous_oxide.rename(columns={'Year': 'year', 'Entity': 'country', 'Code': 'iso_code', 'Per-capita nitrous oxide emissions in CO₂ equivalents': 'nitrous_oxide_emissions'})

col2, space2, col3 = st.columns((10,1,10))

with col2:
    year = st.slider('Select year', df_co['year'].min(), df_co['year'].max())
    
    df_co_year = df_co[df_co['year']==year]
    df_methane_year = df_methane[df_methane['year']==year]
    df_nitrous_oxide_year = df_nitrous_oxide[df_nitrous_oxide['year']==year]
    
    fig = px.choropleth(df_co_year, locations="iso_code",
                        color="co_per_capita",
                        hover_name="country",
                        range_color=(0,25),
                        color_continuous_scale=px.colors.sequential.Reds)
    
    fig2 = px.choropleth(df_methane_year, locations="iso_code",
                        color="methane_emissions",
                        hover_name="country",
                        range_color=(0,25),
                        color_continuous_scale=px.colors.sequential.Blues)
    
    fig3 = px.choropleth(df_nitrous_oxide_year, locations="iso_code",
                        color="nitrous_oxide_emissions",
                        hover_name="country",
                        range_color=(0,25),
                        color_continuous_scale=px.colors.sequential.Greens)
    
    st.plotly_chart(fig, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.plotly_chart(fig3, use_container_width=True)
