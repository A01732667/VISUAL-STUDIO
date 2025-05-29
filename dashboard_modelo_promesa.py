
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix

st.set_page_config(page_title="Modelo: Promesa de Pago", layout="wide")
st.title("🤖 Dashboard de Machine Learning - Predicción de Promesa de Pago")

@st.cache_data
def load_and_process_data():
    xls = pd.ExcelFile("BASE.xlsx")
    df = xls.parse('Sheet1')

    # Preprocesamiento
    df = df.rename(columns=lambda x: x.strip())
    df = df[df["Promesa_de_Pago"].notna()]
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].fillna("Desconocido")
    for col in df.select_dtypes(include=["float64", "int64"]).columns:
        df[col] = df[col].fillna(-1)
    if "ID Ally" in df.columns:
        df = df.drop(columns=["ID Ally"], errors='ignore')

    # Label Encoding
    le = LabelEncoder()

    # Codificar variables categóricas (asegurando uniformidad de tipo)
    le = LabelEncoder()
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str)  # Asegura que todos los valores sean strings
        df[col] = le.fit_transform(df[col])


    X = df.drop(columns=["Promesa_de_Pago"])
    y = df["Promesa_de_Pago"]

    return train_test_split(X, y, test_size=0.2, random_state=42)

X_train, X_test, y_train, y_test = load_and_process_data()

# Entrenar modelo
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Métricas y matriz de confusión
report_dict = classification_report(y_test, y_pred, output_dict=True)
conf_matrix = confusion_matrix(y_test, y_pred)

# Métricas clave
st.subheader("📈 Métricas del Modelo")
col1, col2, col3 = st.columns(3)
col1.metric("Accuracy", f"{report_dict['accuracy']*100:.2f}%")
col2.metric("Precision (Pago)", f"{report_dict['1']['precision']*100:.2f}%")
col3.metric("Recall (Pago)", f"{report_dict['1']['recall']*100:.2f}%")

# Matriz de Confusión
st.subheader("🔀 Matriz de Confusión")
fig, ax = plt.subplots()
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues",
            xticklabels=["No Pago", "Pago"], yticklabels=["No Pago", "Pago"], ax=ax)
ax.set_xlabel("Predicción")
ax.set_ylabel("Real")
st.pyplot(fig)

# Importancia de variables
st.subheader("🔍 Importancia de Variables")
importances = model.feature_importances_
features = X_train.columns
importance_df = pd.DataFrame({"Feature": features, "Importance": importances}).sort_values(by="Importance", ascending=False)
fig2 = px.bar(importance_df.head(15), x='Importance', y='Feature', orientation='h', title="Top 15 Características más Relevantes")
st.plotly_chart(fig2, use_container_width=True)

# Mostrar muestra de predicciones
st.subheader("🧾 Ejemplos de Predicciones")
sample_df = X_test.copy()
sample_df["Real"] = y_test
sample_df["Predicho"] = y_pred
st.dataframe(sample_df.head(20))
