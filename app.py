from controllers.app_controller import AppController
import streamlit as st
file_path = "data/beauty.xlsx"

if __name__ == "__main__":
    # Центрируем контент на странице
    st.set_page_config(page_title="Beauty Dashboard", layout="centered")
    app = AppController(filepath=file_path)
    app.run()
