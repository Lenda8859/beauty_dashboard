import streamlit as st
from models.data_loader import DataLoader
from views.kpi import KPIView
from views.masters import MastersView
from views.clients import ClientsView
from views.reports import ReportsView

class AppController:
    def __init__(self, filepath):
        self.model = DataLoader(filepath)
        self.views = {
            "KPI": KPIView(filepath),
            "мастера": MastersView(filepath),
            "клиенты": ClientsView(filepath),
            "отчёты": ReportsView(filepath),
        }

    def run(self):
        page = st.sidebar.radio("Разделы", list(self.views.keys()))
        view = self.views[page]
        raw_df = self.model.raw

        try:
            if hasattr(view, "get_filters") and page != "мастера":
                date_range, category_col, category_val = view.get_filters(raw_df)
                df = self.model.load_and_filter(
                    date_range=date_range,
                    category_col=category_col,
                    category_val=category_val
                )
            else:
                df = raw_df

            if hasattr(view, "render"):
                view.render(df)
            else:
                st.warning("Нет метода render у текущей вкладки")

        except Exception as e:
            st.error(f"Ошибка контроллера: {e}")
