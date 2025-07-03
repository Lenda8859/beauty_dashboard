import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from models.data_loader import DataLoader


class ClientsView:
    def __init__(self, data_path):
        self.loader = DataLoader(data_path)

    def get_filters(self, df):
        date_range = st.sidebar.date_input("Выберите период", [], key="date_range")
        category_col = "мастер"
        category_val = st.sidebar.selectbox("Выберите мастера", df[category_col].dropna().unique())
        return date_range, category_col, category_val

    def render(self, df):
        st.title("👥 Информация о клиентах")
        st.subheader("📊 Общая статистика")

        st.dataframe(df)

        if "Услуга" in df.columns:
            service_counts = df["услуга"].value_counts().reset_index()
            service_counts.columns = ["услуга", "количество"]
            fig_pie = px.pie(service_counts, names="услуга", values="количество", title="Распределение по услугам")
            st.plotly_chart(fig_pie)

        if "мастер" in df.columns:
            bar_data = df["мастер"].value_counts().reset_index()
            bar_data.columns = ["мастер", "количество"]
            fig_bar = px.bar(bar_data, x="мастер", y="количество", title="Количество клиентов по мастерам")
            st.plotly_chart(fig_bar)

        if "дата" in df.columns:
            line_data = df.groupby("дата").size().reset_index(name="клиенты")
            fig_line = px.line(line_data, x="дата", y="клиенты", title="Клиенты по датам")
            st.plotly_chart(fig_line)

