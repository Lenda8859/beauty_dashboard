import pandas as pd

from pandas import date_range
from unicodedata import category


class DataLoader:
    def __init__(self, filepath):
        self.raw = pd.read_excel(filepath, parse_dates=True)


    def load_and_filter(self, date_range=None, category_col=None, category_val=None):
        df = self.raw.copy()

        # Преобразуем колонку "дата" в формат datetime (даже если она уже была такой)
        if 'дата' in df.columns:
            df['дата'] = pd.to_datetime(df['дата'], errors='coerce')

        #  Фильтрация по дате
        if date_range and isinstance(date_range, tuple) and len(date_range) == 2:
            start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
            df = df[(df['дата'] >= start_date) & (df['дата'] <= end_date)]

        # Фильтрация по выбранным категориям
        if category_col and category_val:
            df = df[df[category_col] == category_val]

        return df