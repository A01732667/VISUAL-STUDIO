
import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar datos
@st.cache_data
def load_data():
    xls = pd.ExcelFile("BASE.xlsx")
    df_contacto = xls.parse('Contacto - Team 5')
    return df_contacto

df_contacto = load_data()

# Configuración inicial
st.set_page_config(page_title="Dashboard Contacto", layout="wide")
st.title("📞 Dashboard de Contacto y Cobranza")

# Limpieza básica
df_contacto = df_contacto.rename(columns=lambda x: x.strip())
df_contacto = df_contacto[df_contacto['Días de atraso'].notna()]

# Métricas clave
col1, col2, col3 = st.columns(3)
col1.metric("Clientes en mora", df_contacto.shape[0])
col2.metric("Saldo vencido total", f"$ {df_contacto['Saldo vencido'].sum():,.2f}")
col3.metric("Días de atraso promedio", f"{df_contacto['Días de atraso'].mean():.1f} días")

# Histograma de días de atraso
st.subheader("📊 Distribución de Días de Atraso")
fig1 = px.histogram(df_contacto, x='Días de atraso', nbins=20, title="Histograma de días de atraso")
st.plotly_chart(fig1, use_container_width=True)

# Top clientes con más deuda
st.subheader("💸 Top Clientes con Mayor Saldo Vencido")
top_deudores = df_contacto[['ID Ally', 'Saldo vencido', 'Días de atraso']].sort_values(by='Saldo vencido', ascending=False).head(10)
st.dataframe(top_deudores)

# Gráfica de dispersión: Saldo vs Días de atraso
st.subheader("📈 Relación entre Saldo Vencido y Días de Atraso")
fig2 = px.scatter(df_contacto, x='Días de atraso', y='Saldo vencido',
                  title="Relación entre días de atraso y saldo vencido",
                  labels={'Días de atraso': 'Días de atraso', 'Saldo vencido': 'Saldo vencido'})
st.plotly_chart(fig2, use_container_width=True)

# Filtro por rango de atraso
st.subheader("🔍 Filtrado por Días de Atraso")
rango = st.slider("Selecciona rango de días de atraso", int(df_contacto['Días de atraso'].min()), int(df_contacto['Días de atraso'].max()), (30, 90))
df_filtrado = df_contacto[(df_contacto['Días de atraso'] >= rango[0]) & (df_contacto['Días de atraso'] <= rango[1])]
st.dataframe(df_filtrado[['ID Ally', 'Saldo vencido', 'Días de atraso']].head(20))

# Pie de página
st.markdown("___")
st.caption("Desarrollado por Alysse Consulting para análisis de cobranza.")
