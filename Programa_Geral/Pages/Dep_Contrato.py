from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from database.db import SessionLocal, engine  # Usar engine, não SessionLocal
import re
from sqlalchemy import create_engine, text


#def app():
# --- Menu lateral ---
# --- Configuração da página ---
st.set_page_config(page_title="Gestão de Contagens", layout="wide")

# --- Menu lateral ---
with st.sidebar:
    selected = option_menu(
        menu_title="Menu Principal",
        options=["Cadastro", "Consulta Processo"],
        menu_icon="cast",
        default_index=0
    )

if selected == "Cadastro":
    st.header("Importação de Dados de Contagens")

    # --- formulario de cadastro ---
    with st.form("form_completo"):

        with st.expander("Parte 1 – Dados do Cliente", expanded=True):
            nome = st.text_input("Nome")
            nif = st.text_input("NIF")

        with st.expander("Parte 2 – Dados da Fatura"):
            valor = st.number_input("Valor", min_value=0.0)
            data = st.date_input("Data")

        submit = st.form_submit_button("Gravar")