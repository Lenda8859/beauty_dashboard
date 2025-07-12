# # загрузка фильтрация данных
#
# import pandas as pd
#
#
# class DataLoader:
#     def __init__(self):
#         self.raw = pd.read_excel("D:/!Dasboard/Excel_fiels/beauty.xlsx")
#         self.raw["дата"] = pd.to_datetime(self.raw["дата"])
#         #self.raw = pd.read_csv("data/data.csv")
#
#     def load_and_filter(self, drange, cats, masters):
#         df = self.raw.copy()
#
#         # Фильтрация по категории
#         if cats:
#             df = df[df["категория"].isin(cats)]
#
#         # Фильтрация по мастеру
#         if masters:
#             df = df[df["мастер"].isin(masters)]
#
#         # Фильтрация по дате
#         if drange and len(drange) == 2:
#             start_date = pd.to_datetime(str(drange[0]))
#             end_date = pd.to_datetime(str(drange[1]))
#             df = df[(df["дата"] >= start_date) & (df["дата"] <= end_date)]
#         return df
#
