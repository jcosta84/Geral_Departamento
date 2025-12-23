from datetime import datetime
import sys
import os

import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from database.db import engine

# =========================================================
# CONFIGURAÇÃO INICIAL (SEMPRE PRIMEIRO)
# =========================================================
st.set_page_config(page_title="Sistema", layout="wide")

# =========================================================
# PATHS E IMPORTS
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# Pages (a pasta Pages TEM __init__.py)
from Pages import (
    Home,
    DAC_Lojas,
    Dep_Factura,
    Dep_Gest_Contagens,
    Dep_Contrato,
    Admin,
    Definicao
)

# =========================================================
# CSS — OCULTAR APENAS "EMPRESA / PAGES"
# =========================================================
hide_streamlit_style = """
<style>
/* Esconder menu automático "Empresa / Pages" */
div[data-testid="stSidebarNav"] {
    display: none !important;
}

/* Opcional */
header[data-testid="stHeader"] {
    display: none !important;
}

footer {
    display: none !important;
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("username", None)
st.session_state.setdefault("nivel", None)

# =========================================================
# FUNÇÃO LOGIN (mantida como tens atualmente)
# =========================================================
def check_login(username, password):
    query = f"""
        SELECT nivel FROM usuarios
        WHERE username = '{username}' AND password = '{password}'
    """
    df = pd.read_sql(query, engine)
    if not df.empty:
        return df.iloc[0]["nivel"]
    return None

# =========================================================
# TELA DE LOGIN
# =========================================================
if not st.session_state["logged_in"]:
    st.title("Tela de Login ao Sistema")

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Login"):
        nivel = check_login(username, password)
        if nivel:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["nivel"] = nivel
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos!")

# =========================================================
# APLICAÇÃO PRINCIPAL
# =========================================================
else:
    nivel = st.session_state["nivel"]

    # ---------------- MENU POR NÍVEL ----------------
    if nivel == "admin":
        menu_opcoes = ["Home", "Lojas", "Facturação", "Contagem", "Contratação", "Administração"]
    elif nivel == "gerente":
        menu_opcoes = ["Home", "Lojas", "Facturação", "Contagem", "Contratação", "Definição"]
    elif nivel == "factura":
        menu_opcoes = ["Home", "Facturação", "Definição"]
    elif nivel == "contagem":
        menu_opcoes = ["Home", "Contagem", "Definição"]
    elif nivel == "contrato":
        menu_opcoes = ["Home", "Contratação", "Definição"]
    elif nivel == "usuario":
        menu_opcoes = ["Home", "Lojas", "Definição"]
    else:
        menu_opcoes = ["Home"]

    # ---------------- SIDEBAR ----------------
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state['username']}")
        st.caption(f"Nível de acesso: {st.session_state['nivel']}")
        st.divider()

        selected = option_menu(
            menu_title="Menu Principal",
            options=menu_opcoes,
            menu_icon="cast",
            default_index=0,
            orientation="vertical"
        )

        st.divider()

        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()

    # ---------------- CONTEÚDO ----------------
    if selected == "Home":
        Home.app()
    elif selected == "Lojas":
        DAC_Lojas.app()
    elif selected == "Facturação":
        Dep_Factura.app()
    elif selected == "Contagem":
        Dep_Gest_Contagens.app()
    elif selected == "Contratação":
        Dep_Contrato.app()
    elif selected == "Administração":
        Admin.app()
    elif selected == "Definição":
        Definicao.app()
