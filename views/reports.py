import pandas as pd
import streamlit as st
import plotly.express as px
from models.data_loader import DataLoader


class ReportsView:
    def __init__(self, data_path):
        self.data_path = data_path
        self.loader = DataLoader(self.data_path)

    def render(self, df):
        st.title("📄 Общий отчёт")

        df['дата'] = pd.to_datetime(df['дата'])
        st.dataframe(df)

        # 📊 Общее количество услуг по мастерам
        st.subheader("👨‍🔧 Услуги по мастерам")
        master_summary = df['мастер'].value_counts().reset_index()
        master_summary.columns = ['мастер', 'количество']
        fig1 = px.bar(master_summary, x='мастер', y='количество',
                      color_discrete_sequence=['#4C5C68'])
        st.plotly_chart(fig1)

        # 🌀 Услуги по категориям
        st.subheader("🌀 Популярность услуг")
        service_summary = df['услуга'].value_counts().reset_index()
        service_summary.columns = ['услуга', 'количество']
        fig2 = px.pie(service_summary, names='услуга', values='количество',
                      color_discrete_sequence=['#4C5C68', '#EEC07C'])
        st.plotly_chart(fig2)

        # 📈 Динамика количества клиентов
        st.subheader("📈 Количество клиентов по датам")
        client_daily = df.groupby('дата')['клиент'].nunique().reset_index()
        client_daily.columns = ['дата', 'Уникальных клиентов']
        fig3 = px.line(client_daily, x='дата', y='Уникальных клиентов',
                       color_discrete_sequence=['#4C5C68'])
        st.plotly_chart(fig3)

        # 💸 Средний чек по датам
        if 'сумма' in df.columns:
            st.subheader("💸 Средний чек по датам")
            avg_price_by_date = df.groupby('дата')['сумма'].mean().reset_index()
            fig4 = px.line(avg_price_by_date, x='дата', y='сумма',
                           title='Средний чек по датам', color_discrete_sequence=['#EEC07C'])
            st.plotly_chart(fig4)
