import pandas as pd
import streamlit as st
import plotly.express as px
from models.data_loader import DataLoader


class KPIView:
    def __init__(self, data_path):
        self.data_path = data_path
        self.loader = DataLoader(self.data_path)


    def get_filtered_data(self, df):

        df['дата'] = pd.to_datetime(df['дата'])

        min_date = df['дата'].min().date()
        max_date = df['дата'].max().date()

        start_date = st.sidebar.date_input("📅 Начало периода", min_date, key="start_date_filter_kpi")
        end_date = st.sidebar.date_input("📅 Конец периода", max_date, key="end_date_filter_kpi")

        filtered_df = df[
            (df['дата'] >= pd.to_datetime(start_date)) &
            (df['дата'] <= pd.to_datetime(end_date))
        ]

        return filtered_df, start_date, end_date

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

        st.title("📊 KPI — Ключевые показатели")

        filtered_df, start_date, end_date = self.get_filtered_data(df)
        st.subheader(f"Данные за период: {start_date} — {end_date}")
        st.markdown("<div style='overflow-x: auto'>", unsafe_allow_html=True)
        st.dataframe(filtered_df)
        st.markdown("<div>", unsafe_allow_html=True)

        # KPI: Средний чек
        if 'сумма' in filtered_df.columns:
            avg_price = round(filtered_df['сумма'].mean(), 2)
            st.metric("💰 Средний чек", f"{avg_price} ₽")

        # KPI: Количество клиентов
        unique_clients = filtered_df['клиент'].nunique()
        st.metric("👥 Уникальных клиентов", unique_clients)

        # KPI: Количество услуг
        total_services = filtered_df.shape[0]
        st.metric("🧾 Всего услуг", total_services)

        # 📈 График активности по дням
        st.subheader("📈 Активность по датам")
        activity = filtered_df.groupby('дата').size().reset_index(name='количество')
        fig1 = px.line(activity, x='дата', y='количество', title='Количество услуг по датам',
                       color_discrete_sequence=['#4C5C68'])
        st.plotly_chart(fig1)

        # 🌀 Распределение по услугам
        st.subheader("🌀 Распределение по услугам")
        service_counts = filtered_df['услуга'].value_counts().reset_index()
        service_counts.columns = ['услуга', 'количество']
        fig2 = px.pie(service_counts, names='услуга', values='количество',
                      color_discrete_sequence=['#4C5C68', '#EEC07C'])
        st.plotly_chart(fig2)

        # 📊 Загрузка мастеров
        st.subheader("📊 Нагрузка по мастерам")
        master_counts = filtered_df['мастер'].value_counts().reset_index()
        master_counts.columns = ['мастер', 'количество']
        fig3 = px.bar(master_counts, x='мастер', y='количество',
                      color_discrete_sequence=['#4C5C68'])
        st.plotly_chart(fig3)
