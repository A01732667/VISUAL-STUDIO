import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("📞 Dashboard de Llamadas")

try:
    df = pd.read_csv("llamadas_filtradas.csv")
    st.success("Datos cargados correctamente.")
except Exception as e:
    st.error(f"Error al cargar CSV: {e}")
    st.stop()

st.write("Primeras filas del DataFrame:")
st.dataframe(df.head())

# Preprocesamiento
df["Promesa_de_Pago"] = df["Promesa_de_Pago"].fillna(0)
df["Llamada_Contestada"] = df["Llamada_Contestada"].fillna(0)

# Tabla resumen
grouped = df.groupby(["Dia Semana", "Rango Hora"]).agg({
    "Promesa_de_Pago": "sum",
    "Llamada_Contestada": "sum",
    "ID Ally": "count"
}).rename(columns={"ID Ally": "Total Llamadas"}).reset_index()

grouped["Tasa Promesa"] = grouped["Promesa_de_Pago"] / grouped["Total Llamadas"]

st.subheader(" Tabla Resumen")
st.dataframe(grouped.head(20))

# Heatmap
st.subheader(" Heatmap de Tasa de Promesa de Pago")
pivot = grouped.pivot(index="Dia Semana", columns="Rango Hora", values="Tasa Promesa")

fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(pivot, annot=True, cmap="YlGnBu", ax=ax)
st.pyplot(fig)
