from datetime import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from sqlalchemy import text  # <-- faltava isto
from database.db import SessionLocal, engine  # ok

def app():

    st.set_page_config(page_title="Definição", layout="wide")

    st.title("Configuração de Conta")
    st.subheader("Alterar Senha da Conta")

    # ✅ Garante que a chave existe
    if "username" not in st.session_state:
        st.session_state["username"] = None

    # ✅ Lê com segurança
    username_logado = st.session_state.get("username")

    # ✅ Se não estiver logado, para a página
    if not username_logado:
        st.error("Utilizador não logado / sessão expirada. Faça login novamente.")
        st.stop()

    with st.form("alterar_senha_form"):
        senha_atual = st.text_input("Senha Atual", type="password")
        nova_senha = st.text_input("Nova Senha", type="password")
        confirmar_senha = st.text_input("Confirmar Nova Senha", type="password")
        submitted = st.form_submit_button("Alterar Senha")

    if submitted:
        session = SessionLocal()
        try:
            query = text("SELECT password FROM usuarios WHERE username = :username")
            result = session.execute(query, {"username": username_logado}).fetchone()

            if not result:
                st.error("Utilizador não encontrado.")
            elif result[0] != senha_atual:
                st.error("Senha atual incorreta.")
            elif nova_senha != confirmar_senha:
                st.error("A nova senha e a confirmação não coincidem.")
            else:
                update_query = text("UPDATE usuarios SET password = :nova WHERE username = :username")
                session.execute(update_query, {"nova": nova_senha, "username": username_logado})
                session.commit()
                st.success("Senha alterada com sucesso!")

        except Exception as e:
            st.error(f"Erro ao alterar a senha: {e}")
        finally:
            session.close()
