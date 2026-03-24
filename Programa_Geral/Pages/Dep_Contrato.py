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

def app():

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
    def idx(lista, valor, default=0):
        """Devolve o index do valor na lista; se não existir, devolve default."""
        try:
            return lista.index(valor)
        except Exception:
            return default

    # =============================
    # Listas para selectbox (as mesmas que usas no cadastro)
    servicos = ["Pós-Pago", "Pré-Pago"]
    potencias = ["1100 Kva", "2200 Kva", "3300 Kva", "6600 Kva", "9900 Kva", "13200 Kva", "16500 Kva", "19800 Kva"]
    tipos = ["Monofásica", "Bifásica", "Trifásica"]
    formatos = ["Normal", "Remota"]
    estilos = ["Normal", "Bidirecional"]
    clientes = ["Normal", "Micro Produtor"]
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

            if df.empty:
                st.warning("Não existem processos cadastrados.")
                st.stop()

            # --------- manter valores no session_state ---------
            if "pesquisa_proc" not in st.session_state:
                st.session_state["pesquisa_proc"] = ""
            if "id_sel_proc" not in st.session_state:
                st.session_state["id_sel_proc"] = None

            # ✅ campo fica sempre e mantém o que foi digitado
            pesquisa = st.text_input(
                "Pesquisar por ID, CNI ou Nome",
                placeholder="Digite o ID, CNI ou Nome do cliente",
                key="pesquisa_proc"
            )

            # --------- FILTRO DINÂMICO ---------
            if pesquisa:
                seleid = df[
                    df["id"].astype(str).str.contains(pesquisa, case=False, na=False)
                    | df["cni"].astype(str).str.contains(pesquisa, case=False, na=False)
                    | df["nome"].astype(str).str.contains(pesquisa, case=False, na=False)
                ].copy()
            else:
                seleid = df.copy()

            if seleid.empty:
                st.warning("Nenhum processo encontrado.")
                st.stop()

            # --------- label do selectbox ---------
            seleid["label"] = (
                "ID: " + seleid["id"].astype(str)
                + " | " + seleid["nome"].fillna("").astype(str)
                + " | CNI: " + seleid["cni"].fillna("").astype(str)
            )

            labels = seleid["label"].tolist()

            # ✅ manter a seleção anterior se ainda existir no filtro
            if st.session_state["id_sel_proc"] is not None:
                mask = seleid["id"] == st.session_state["id_sel_proc"]
                if mask.any():
                    id_atual = int(st.session_state["id_sel_proc"])
                    label_atual = seleid.loc[seleid["id"] == id_atual, "label"].iloc[0]
                    index_atual = labels.index(label_atual)
                else:
                    index_atual = 0
            else:
                index_atual = 0

            escolha = st.selectbox(
                "Escolha o processo",
                labels,
                index=index_atual
            )

            # guardar id selecionado
            id_sel = int(escolha.split("|")[0].replace("ID:", "").strip())
            st.session_state["id_sel_proc"] = id_sel

            # pegar a linha selecionada
            row = seleid.loc[seleid["id"] == id_sel].iloc[0]

            def idx(lista, valor, default=0):
                try:
                    return lista.index(valor)
                except Exception:
                    return default

            # --------- FORM (consulta) ---------
            with st.form("form_completo_consulta"):

                with st.expander("Parte 1 – Dados do Cliente", expanded=True):
                    st.text_input("Nome", value=str(row.get("nome", "") or ""), disabled=True)
                    st.text_input("Unidade", value=str(row.get("unidade", "") or ""), disabled=True)
                    st.text_input("Localidade", value=str(row.get("localidade", "") or ""), disabled=True)
                    st.text_input("Morada", value=str(row.get("morada", "") or ""), disabled=True)
                    st.text_input("CNI", value=str(row.get("cni", "") or ""), disabled=True)

                    st.number_input("NIF", value=int(row.get("nif", 0) or 0), min_value=0, step=1, format="%d", disabled=True)
                    st.number_input("Móvel", value=int(row.get("movel", 0) or 0), min_value=0, step=1, format="%d", disabled=True)
                    st.number_input("Telefone", value=int(row.get("telefone", 0) or 0), min_value=0, step=1, format="%d", disabled=True)

                    st.text_input("Email", value=str(row.get("email", "") or ""), disabled=True)
                    st.date_input("Data de Entrada", value=row.get("data_entrada"), disabled=True)
                    st.text_input("Loja de Entrada", value=str(row.get("loja_entrada", "") or ""), disabled=True)

                with st.expander("Parte 2 – Tipo de Ligação", expanded=False):
                    st.selectbox("Serviço", servicos, index=idx(servicos, row.get("servico")), disabled=True)
                    st.selectbox("Potência", potencias, index=idx(potencias, row.get("potencia")), disabled=True)
                    st.selectbox("Tipo de Ligação", tipos, index=idx(tipos, row.get("tipo_ligacao")), disabled=True)
                    st.selectbox("Formato do Contador", formatos, index=idx(formatos, row.get("formato_medidor")), disabled=True)
                    st.selectbox("Contador", estilos, index=idx(estilos, row.get("estilo_contador")), disabled=True)
                    st.selectbox("Cliente", clientes, index=idx(clientes, row.get("cliente_tipo")), disabled=True)

                with st.expander("Parte 3 – Indicação de Local", expanded=False):
                    st.text_input("Localização", value=str(row.get("localizacao", "") or ""), disabled=True)
                    st.text_input("Referência", value=str(row.get("referencia", "") or ""), disabled=True)

                    lat = float(row.get("latitude", 0.0) or 0.0)
                    lon = float(row.get("longitude", 0.0) or 0.0)

                    st.number_input("Latitude", value=lat, min_value=-90.0, max_value=90.0, format="%.6f", disabled=True)
                    st.number_input("Longitude", value=lon, min_value=-180.0, max_value=180.0, format="%.6f", disabled=True)

                    st.divider()
                    if lat != 0.0 or lon != 0.0:
                        st.map(pd.DataFrame({"lat": [lat], "lon": [lon]}), zoom=14)

                with st.expander("📄 Documento (PDF)", expanded=False):
                    pdf_bytes = row.get("pdf_bytes")
                    pdf_nome = row.get("pdf_nome", "documento.pdf")
                    pdf_mime = row.get("pdf_mime", "application/pdf")

                    if pdf_bytes:
                        st.download_button("⬇️ Baixar PDF", data=pdf_bytes, file_name=pdf_nome, mime=pdf_mime)
                        mostrar_pdf(pdf_bytes)
                    else:
                        st.info("Este processo não possui PDF.")

                c1, c2 = st.columns(2)
                fechar = c1.form_submit_button("✅ Fechar")
                editar = c2.form_submit_button("✏️ Editar")

            if fechar:
                st.info("Fechado.")
            if editar:
                st.info("Modo edição.")

        except Exception as e:
            st.error(f"Erro ao consultar processos: {e}")
