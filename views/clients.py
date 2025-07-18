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
        # Стилизация под мобильные устройства
        st.markdown("""
                             <style>
                            .block-container {
                            padding: 1rem 1 rem;
                                        }
                            .css-1d391kg {  /* nf,kbws */
                            font-size: 16px !important; }
                            .stButton button {
                            font-size: 18px !important:
                            padding: 10px 20px;
                                }
                            </style>
                        """, unsafe_allow_html=True)

        st.title("👥 Информация о клиентах")

        st.subheader("📊 Общая статистика")
        st.markdown("<div style='overflow-x: auto'>", unsafe_allow_html=True)
        st.dataframe(df)
        st.markdown("<div>", unsafe_allow_html=True)



        if "Услуга" in df.columns:
            service_counts = df["услуга"].value_counts().reset_index()
            service_counts.columns = ["услуга", "количество"]
            fig_pie = px.pie(service_counts, names="услуга", values="количество", title="Распределение по услугам")
            st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

        if "мастер" in df.columns:
            bar_data = df["мастер"].value_counts().reset_index()
            bar_data.columns = ["мастер", "количество"]
            fig_bar = px.bar(bar_data, x="мастер", y="количество", title="Количество клиентов по мастерам")
            st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

        if "дата" in df.columns:
            line_data = df.groupby("дата").size().reset_index(name="клиенты")
            fig_line = px.line(line_data, x="дата", y="клиенты", title="Клиенты по датам")
            st.plotly_chart(fig_line, use_container_width=True, config={"displayModeBar": False})

