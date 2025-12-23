from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from database.db import engine  # Usar engine, não SessionLocal
import re

def app():
    st.title("DAC Lojas")

    # Exemplo de uso do engine para uma consulta simples
    with engine.connect() as connection:
        result = connection.execute("SELECT nome_loja, endereco FROM lojas LIMIT 5")
        lojas = pd.DataFrame(result.fetchall(), columns=result.keys())

    st.subheader("Lojas Cadastradas")
    st.dataframe(lojas)

    # Formulário para adicionar nova loja
    st.subheader("Adicionar Nova Loja")
    with st.form("adicionar_loja_form"):
        nome_loja = st.text_input("Nome da Loja")
        endereco = st.text_input("Endereço")
        submitted = st.form_submit_button("Adicionar Loja")

        if submitted:
            if nome_loja and endereco:
                with engine.connect() as connection:
                    connection.execute(
                        "INSERT INTO lojas (nome_loja, endereco) VALUES (%s, %s)",
                        (nome_loja, endereco)
                    )
                st.success(f"Loja '{nome_loja}' adicionada com sucesso!")
            else:
                st.error("Por favor, preencha todos os campos.")