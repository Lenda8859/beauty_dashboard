#разметка стили подгрузка вкладок

import streamlit as st

def apply_styles():
    try:
        with open("assets/style.css", encoding="utf-8") as f:
            css = f"<style>{f.read()}</style>"
            st.markdown(css, unsafe_allow_html=True)
            print("✅ Стили загружены успешно.")
    except Exception as e:
        print("❌ Ошибка при загрузке CSS:", e)
