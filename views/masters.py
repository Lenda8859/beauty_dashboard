import pandas as pd
import streamlit as st
import plotly.express as px
from models.data_loader import DataLoader

class MastersView:
    def __init__(self, data_path):
        self.data_path = data_path
        self.loader = DataLoader(self.data_path)

    def get_filters(self, df):
        masters = df['мастер'].dropna().unique()
        selected_master = st.sidebar.selectbox("Выберите мастера", masters)

        dates = pd.to_datetime(df['дата'].dropna())
        start_date = pd.to_datetime(
            st.sidebar.date_input("Начало периода", dates.min().date(), key="start_date_filter_master")
        )
        end_date = pd.to_datetime(
            st.sidebar.date_input("Конец периода", dates.max().date(), key="end_date_filter_master")
        )

        return selected_master, start_date, end_date

    def render(self, df):
        st.title("🧑‍🎨 Аналитика по мастерам")

        # Получаем фильтры
        selected_master, start_date, end_date = self.get_filters(df)

        # Приводим данные к нужному типу
        df['дата'] = pd.to_datetime(df['дата'])
        df['мастер'] = df['мастер'].astype(str).str.strip()
        selected_master = str(selected_master).strip()

        # Фильтрация
        filtered_df = df[
            (df['мастер'] == selected_master) &
            (df['дата'] >= start_date) &
            (df['дата'] <= end_date)
        ]

        st.subheader(f"📅 Период: {start_date.date()} — {end_date.date()}")
        st.dataframe(filtered_df)

        # 1. Круговая диаграмма — распределение по услугам
        if 'Услуга' in filtered_df.columns:
            st.subheader("🌀 Услуги мастера")
            pie_data = filtered_df['Услуга'].value_counts().rename_axis('Услуга').reset_index(name='количество')
            fig_pie = px.pie(pie_data, names='Услуга', values='количество',
                             color_discrete_sequence=['#4C5C68', '#EEC07C'])
            st.plotly_chart(fig_pie)

        # 2. Линейный график — количество клиентов по дням
        st.subheader("📈 Загрузка по датам")
        line_data = filtered_df.groupby('дата').size().reset_index(name='количество')
        fig_line = px.line(line_data, x='дата', y='количество',
                           color_discrete_sequence=['#4C5C68'])
        st.plotly_chart(fig_line)

        # 3. Гистограмма — частота по услугам
        if 'услуга' in filtered_df.columns:
            st.subheader("📊 Частота по услугам")
            bar_data = filtered_df['услуга'].value_counts().reset_index()
            bar_data.columns = ['услуга', 'количество']
            fig_bar = px.bar(bar_data, x='услуга', y='количество',
                             color_discrete_sequence=['#4C5C68'])
            st.plotly_chart(fig_bar)