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


def app():
    # --- Configuração da página ---
    st.set_page_config(page_title="Administração", layout="wide")

    st.subheader("📋 Lista de Usuários")

    # Consulta todos os usuários
    df_usuarios = pd.read_sql("SELECT id, username, password, nivel FROM usuarios", engine)
    st.dataframe(df_usuarios, hide_index=True)
    st.markdown("---")
    st.subheader("➕ Criar Novo Usuário")
    with st.form("form_criar_usuario"):
        novo_user = st.text_input("Nome de usuário")
        nova_senha = st.text_input("Senha", type="password")
        novo_nivel = st.selectbox("Nível de acesso", ["admin", "gerente", "usuario", "contrato", "factura", "contagem"])
        submitted = st.form_submit_button("Criar")
        if submitted:
            try:
                query = text("""
                    INSERT INTO usuarios (username, password, nivel) 
                    VALUES (:username, :password, :nivel)
                """)
                session = SessionLocal()
                try:
                    session.execute(query, {"username": novo_user, "password": nova_senha, "nivel": novo_nivel})
                    session.commit()
                    st.success(f"Usuário '{novo_user}' criado com sucesso!")
                except Exception as e:
                    session.rollback()
                    st.error(f"Erro ao criar usuário: {e}")
                finally:
                    session.close()
                st.success(f"Usuário '{novo_user}' criado com sucesso!")
                #st.experimental_rerun()
            except Exception as e:
                st.error(f"Erro ao criar usuário: {e}")
    st.markdown("---")
    st.subheader("✏️ Editar ou Excluir Usuário")

    # Selecionar usuário para edição
    user_ids = df_usuarios["id"].tolist()
    user_map = {f"{row['username']} ({row['nivel']})": row["id"] for _, row in df_usuarios.iterrows()}

    selecionado = st.selectbox("Selecionar usuário", list(user_map.keys()))
    id_selecionado = user_map[selecionado]

    # Buscar dados do usuário selecionado
    dados_user = df_usuarios[df_usuarios["id"] == id_selecionado].iloc[0]

    with st.form("form_editar_usuario"):
        novo_username = st.text_input("Novo nome de usuário", value=dados_user["username"])
        nova_senha_edit = st.text_input("Nova senha (deixe em branco para não alterar)", type="password")
        novo_nivel_edit = st.selectbox("Novo nível", ["admin", "gerente", "usuario", "contrato", "factura", "contagem"], index=["admin", "gerente", "usuario", "contrato", "factura", "contagem"].index(dados_user["nivel"]))
        
        col1, col2 = st.columns(2)
        with col1:
            atualizar = st.form_submit_button("Atualizar")
        with col2:
            deletar = st.form_submit_button("Excluir", type="primary")

        if atualizar:
            try:
                if nova_senha_edit:
                    update_query = f"""
                        UPDATE usuarios 
                        SET username = '{novo_username}', password = '{nova_senha_edit}', nivel = '{novo_nivel_edit}'
                        WHERE id = {id_selecionado}
                    """
                else:
                    update_query = f"""
                        UPDATE usuarios 
                        SET username = '{novo_username}', nivel = '{novo_nivel_edit}'
                        WHERE id = {id_selecionado}
                    """
                session = SessionLocal()
                try:
                    session.execute(text(update_query))
                    session.commit()
                    st.success("Usuário atualizado com sucesso!")
                except Exception as e:
                    session.rollback()
                    st.error(f"Erro ao atualizar: {e}")
                finally:
                    session.close()
                    st.success("Usuário atualizado com sucesso!")
                    #st.experimental_rerun()
            except Exception as e:
                st.error(f"Erro ao atualizar: {e}")

        if deletar:
            try:
                session = SessionLocal()
                try:
                    session.execute(text(f"DELETE FROM usuarios WHERE id = {id_selecionado}"))
                    session.commit()
                    st.success("Usuário excluído com sucesso!")
                except Exception as e:
                    session.rollback()
                    st.error(f"Erro ao excluir: {e}")
                finally:
                    session.close()
                    st.success("Usuário excluído com sucesso!")
                    #st.experimental_rerun()
            except Exception as e:
                st.error(f"Erro ao excluir: {e}")