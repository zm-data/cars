import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

url = 'https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv'
df = pd.read_csv(url)

# Renommer les colonnes pour plus de clarté
df = df.rename(columns={'mpg': 'Miles_per_Gallon', 'cylinders': 'Cylinders', 'cubicinches': 'CubicInches',
                        'hp': 'Horsepower', 'weightlbs': 'Weightlbs', 'time-to-60': 'Time_to_60',
                        'year': 'Year', 'continent': 'Continent'})

# Nettoyer la colonne 'Weightlbs' en supprimant les caractères non numériques
df['Weightlbs'] = pd.to_numeric(df['Weightlbs'].replace('[^\d.]', '', regex=True), errors='coerce')

# Sidebar pour le filtrage par région
region_filter = st.sidebar.selectbox('Filtrer par région:', df['Continent'].unique())

# Filtrage du dataframe en fonction de la région sélectionnée
filtered_df = df[df['Continent'] == region_filter]

# Analyse de corrélation
st.header('Analyse de corrélation')
correlation_matrix = filtered_df.corr(numeric_only=True)  # Explicitly set numeric_only to True
fig, ax = plt.subplots()
sns.heatmap(correlation_matrix, annot=True, ax=ax)
st.pyplot(fig)

# Analyse de distribution
st.header('Analyse de distribution')
for column in filtered_df.columns:
    if filtered_df[column].dtype in ['int64', 'float64']:
        st.subheader(f'Distribution de {column}')
        fig, ax = plt.subplots()
        sns.histplot(filtered_df[column], kde=True, ax=ax)
        st.pyplot(fig)

# Affichage du dataframe
st.write(f'## Analyse de voitures par région ({region_filter})')
st.write(filtered_df)

