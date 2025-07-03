import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Streamlit: Пример графика")

# Пример данных
df = pd.DataFrame({
    "Категория": ["A", "B", "C", "D"],
    "Значение": [100, 200, 300, 400]
})

fig = px.bar(df, x="Категория", y="Значение", title="Streamlit: Гистограмма")

st.plotly_chart(fig)