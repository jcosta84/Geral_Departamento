import base64
import sys
import os
import re
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from sqlalchemy import text  # ✅ CORRETO
from database.db import engine  # ✅ engine SQLAlchemy (MySQL)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# -----------------------------
# Validação de e-mail
# -----------------------------
def validar_email(label, key="Email"):
    email = st.text_input(label, key=key)
    padrao = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    if email and not re.match(padrao, email):
        st.error("❌ Email inválido. Ex: nome@email.com")
        return email, False
    return email, True

# -----------------------------
# Mostrar PDF (preview)
# -----------------------------
def mostrar_pdf(pdf_bytes: bytes):
    b64 = base64.b64encode(pdf_bytes).decode("utf-8")
    pdf_html = f"""
        <iframe
            src="data:application/pdf;base64,{b64}"
            width="100%"
            height="600"
            style="border:none;"
        ></iframe>
    """
    st.markdown(pdf_html, unsafe_allow_html=True)

# -----------------------------
# Limpar formulário
# -----------------------------
def limpar_formulario():
    chaves = [
        "nome", "Unidade", "Localidade", "Morada", "CNI", "Nif",
        "Movel", "Telefone", "Email", "Data_Entrada", "Loja_Entrada",
        "Serviço", "Potencia", "Tipo_Ligação", "Formato_Medidor",
        "Estilo_contador", "Cliente",
        "Localização", "Referência", "Latitude", "Longitude",
        "pdf_file"
    ]
    for chave in chaves:
        st.session_state.pop(chave, None)

# -----------------------------
# Configuração da página
# -----------------------------
st.set_page_config(page_title="Contratação", layout="wide")

# -----------------------------
# Menu lateral
# -----------------------------
with st.sidebar:
    selected = option_menu(
        menu_title="Menu Principal",
        options=["Cadastro", "Consulta Processo"],
        menu_icon="cast",
        default_index=0
    )

# =============================
# CADASTRO
# =============================
if selected == "Cadastro":
    st.header("Cadastro de Contratos")

    with st.form("form_completo"):

        with st.expander("Parte 1 – Dados do Cliente", expanded=True):
            nome = st.text_input("Nome", key="nome")
            Unidade = st.text_input("Unidade", key="Unidade")
            Localidade = st.text_input("Localidade", key="Localidade")
            Morada = st.text_input("Morada", key="Morada")
            CNI = st.text_input("CNI", key="CNI")

            Nif = st.number_input("NIF", min_value=0, step=1, format="%d", key="Nif")
            Movel = st.number_input("Móvel", min_value=0, step=1, format="%d", key="Movel")
            Telefone = st.number_input("Telefone", min_value=0, step=1, format="%d", key="Telefone")

            Email, email_ok = validar_email("Email", key="Email")

            Data_Entrada = st.date_input("Data de Entrada", key="Data_Entrada")
            Loja_Entrada = st.text_input("Loja de Entrada", key="Loja_Entrada")

        with st.expander("Parte 2 – Tipo de Ligação", expanded=False):
            Serviço = st.selectbox("Serviço", ["Pós-Pago", "Pré-Pago"], key="Serviço")
            Potencia = st.selectbox(
                "Potência",
                ["1100 Kva", "2200 Kva", "3300 Kva", "6600 Kva", "9900 Kva", "13200 Kva", "16500 Kva", "19800 Kva"],
                key="Potencia"
            )
            Tipo_Ligação = st.selectbox("Tipo de Ligação", ["Monofásica", "Bifásica", "Trifásica"], key="Tipo_Ligação")
            Formato_Medidor = st.selectbox("Formato do Contador", ["Normal", "Remota"], key="Formato_Medidor")
            Estilo_contador = st.selectbox("Contador", ["Normal", "Bidirecional"], key="Estilo_contador")
            Cliente = st.selectbox("Cliente", ["Normal", "Micro Produtor"], key="Cliente")

        with st.expander("Parte 3 – Indicação de Local", expanded=False):
            Localização = st.text_input("Localização", key="Localização")
            Referência = st.text_input("Referência", key="Referência")

            Latitude = st.number_input("Latitude", min_value=-90.0, max_value=90.0, format="%.6f", key="Latitude")
            Longitude = st.number_input("Longitude", min_value=-180.0, max_value=180.0, format="%.6f", key="Longitude")

            st.divider()

            if Latitude != 0.0 or Longitude != 0.0:
                st.markdown("### 📍 Pré-visualização do ponto")
                df_map = pd.DataFrame({"lat": [Latitude], "lon": [Longitude]})
                st.map(df_map, zoom=14)

        with st.expander("📄 Documento (PDF)", expanded=False):
            pdf_file = st.file_uploader(
                "Carregar PDF",
                type=["pdf"],
                accept_multiple_files=False,
                key="pdf_file"
            )

            if pdf_file is not None:
                pdf_bytes_preview = pdf_file.getvalue()
                st.success(f"PDF carregado: {pdf_file.name} ({len(pdf_bytes_preview)/1024:.1f} KB)")

                st.download_button(
                    "⬇️ Baixar este PDF",
                    data=pdf_bytes_preview,
                    file_name=pdf_file.name,
                    mime="application/pdf"
                )

                st.markdown("### 👀 Pré-visualização")
                mostrar_pdf(pdf_bytes_preview)

        col1, col2 = st.columns(2)
        submit = col1.form_submit_button("💾 Gravar")
        limpar = col2.form_submit_button("🧹 Limpar")

    # -----------------------------
    # Ações após submit/limpar
    # -----------------------------
    if submit:
        if not email_ok:
            st.error("Corrija os erros antes de gravar.")
            st.stop()

        # PDF (se existir)
        pdf_nome = None
        pdf_mime = None
        pdf_bytes = None

        if st.session_state.get("pdf_file") is not None:
            pdf_obj = st.session_state["pdf_file"]
            pdf_nome = pdf_obj.name
            pdf_mime = getattr(pdf_obj, "type", None) or "application/pdf"
            pdf_bytes = pdf_obj.getvalue()

        # Converter NIF/Móvel/Telefone para texto (evita perder zeros)
        nif_str = str(Nif) if Nif is not None else None
        movel_str = str(Movel) if Movel is not None else None
        telefone_str = str(Telefone) if Telefone is not None else None

        sql = text("""
            INSERT INTO processos (
                nome, unidade, localidade, morada, cni,
                nif, movel, telefone, email, data_entrada, loja_entrada,
                servico, potencia, tipo_ligacao, formato_medidor, estilo_contador, cliente_tipo,
                localizacao, referencia, latitude, longitude,
                pdf_nome, pdf_mime, pdf_bytes
            )
            VALUES (
                :nome, :unidade, :localidade, :morada, :cni,
                :nif, :movel, :telefone, :email, :data_entrada, :loja_entrada,
                :servico, :potencia, :tipo_ligacao, :formato_medidor, :estilo_contador, :cliente_tipo,
                :localizacao, :referencia, :latitude, :longitude,
                :pdf_nome, :pdf_mime, :pdf_bytes
            )
        """)

        params = {
            "nome": nome,
            "unidade": Unidade,
            "localidade": Localidade,
            "morada": Morada,
            "cni": CNI,

            "nif": nif_str,
            "movel": movel_str,
            "telefone": telefone_str,
            "email": Email,
            "data_entrada": Data_Entrada,
            "loja_entrada": Loja_Entrada,

            "servico": Serviço,
            "potencia": Potencia,
            "tipo_ligacao": Tipo_Ligação,
            "formato_medidor": Formato_Medidor,
            "estilo_contador": Estilo_contador,
            "cliente_tipo": Cliente,

            "localizacao": Localização,
            "referencia": Referência,
            "latitude": Latitude,
            "longitude": Longitude,

            "pdf_nome": pdf_nome,
            "pdf_mime": pdf_mime,
            "pdf_bytes": pdf_bytes
        }

        try:
            with engine.begin() as conn:
                conn.execute(sql, params)

            st.success("✅ Dados gravados com sucesso!")
            limpar_formulario()
            st.rerun()

        except Exception as e:
            st.error(f"❌ Erro ao gravar no MySQL: {e}")
            st.stop()

    if limpar:
        limpar_formulario()
        st.rerun()

# =============================
# CONSULTA
# =============================
elif selected == "Consulta Processo":
    st.header("Consulta de Processos")

    try:
        df = pd.read_sql("SELECT * FROM processos ORDER BY id DESC", engine)
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao consultar processos: {e}")
