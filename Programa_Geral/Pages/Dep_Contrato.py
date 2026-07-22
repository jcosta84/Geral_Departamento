import base64
import sys
import os
import re

# Caminho da pasta principal do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from sqlalchemy import text
from database.db import engine

def app():

    def validar_email(label, key="Email"):
        email = st.text_input(label, key=key)
        padrao = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if email and not re.match(padrao, email):
            st.error("❌ Email inválido. Ex: nome@email.com")
            return email, False
        return email, True

    def mostrar_pdf(pdf_bytes: bytes):
        b64 = base64.b64encode(pdf_bytes).decode("utf-8")
        pdf_html = f"""
            <iframe
                src="data:application/pdf;base64,{b64}"
                width="100%"
                height="600"
                style="border:none;">
            </iframe>
        """
        st.markdown(pdf_html, unsafe_allow_html=True)

    def idx(lista, valor, default=0):
        try:
            return lista.index(valor)
        except Exception:
            return default

    def guardar_processo(dados):
        sql = text("""
            INSERT INTO processos_clientes (
                intencao, loja_entrada, unidade_comercial, nome_cliente,
                localidade, identificador, cni, nif, telefone, movel,
                movel2, email, nia, nivel_tarifario, cil, tipo_servico,
                tipo_ligacao, tipo_cliente, entrada_processo, produto,
                operador, tem_divida, latitude, longitude, uc_cliente,
                marca_aparelho, numero_serie, data_instalacao, tipo_baixa,
                motivo_baixa, servico_baixado, nome_pdf, ficheiro_pdf
            )
            VALUES (
                :intencao, :loja_entrada, :unidade_comercial, :nome_cliente,
                :localidade, :identificador, :cni, :nif, :telefone, :movel,
                :movel2, :email, :nia, :nivel_tarifario, :cil, :tipo_servico,
                :tipo_ligacao, :tipo_cliente, :entrada_processo, :produto,
                :operador, :tem_divida, :latitude, :longitude, :uc_cliente,
                :marca_aparelho, :numero_serie, :data_instalacao, :tipo_baixa,
                :motivo_baixa, :servico_baixado, :nome_pdf, :ficheiro_pdf
            )
        """)

        with engine.begin() as conn:
            conn.execute(sql, dados)

    def buscar_cils_mysql():
        sql = text("""
            SELECT cil
            FROM processos_clientes
            WHERE cil IS NOT NULL
            ORDER BY cil
        """)

        try:
            with engine.connect() as conn:
                resultado = conn.execute(sql).fetchall()

            return [linha._mapping["cil"] for linha in resultado]

        except Exception as e:
            st.error(f"Erro ao carregar CILs do MySQL: {e}")
            return []


    def buscar_cliente_mysql(cil):
        sql = text("""
            SELECT
                cil,
                tipo_cliente,
                uc,
                localidade,
                produto,
                marca_aparelho,
                numero_serie,
                data_instalacao
            FROM clientes
            WHERE cil = :cil
            LIMIT 1
        """)

        try:
            with engine.connect() as conn:
                resultado = conn.execute(sql, {"cil": cil}).fetchone()

            if resultado:
                return dict(resultado._mapping)

            return None

        except Exception as e:
            st.error(f"Erro ao buscar cliente no MySQL: {e}")
            return None

    # =========================
    # LISTAS
    # =========================
    lojas = [
        "Selecionar", "Loja Palmarejo", "Loja ASA", "Loja Plateau",
        "Loja Fazenda", "Loja A. São Filipe", "Loja S. Domingos",
        "Loja Assomada", "Loja Santa Cruz", "Loja Calheta",
        "Loja Tarrafal", "Loja São Filipe (Fogo)", "Loja Mosteiro",
        "Loja Brava", "Loja Maio", "BackOffice Área Contratação"
    ]

    ucs = [
        "Selecionar", "Praia", "São Domingos", "Santa Catarina",
        "Tarrafal", "Calheta", "Santa Cruz", "Mosteiros",
        "São Filipe", "Maio", "Brava"
    ]

    niveis = ["Selecionar", "Nível 1", "Nível 2"]

    tip_clien = [
        "Selecionar", "Empresa Publica", "Colectivos", "Industriais",
        "Construção", "Estado-Patrimonio", "Domésticos",
        "Comércio, Industria, Agricul.", "Consumos Próprios",
        "Autarquias", "Instituições", "Estado-Tesouro",
        "Clientes Senhas de Água"
    ]

    servicos = ["Selecionar", "Pré Pago", "Pós Pago"]
    entr_proc = ["Selecionar", "Processo", "Nota"]
    produtos = ["Selecionar", "Água", "Baixa Tensão", "Baixa Tensão Especial", "Média Tensão"]
    ligacoes = ["Selecionar", "Estaleiro", "Definitivo"]

    tip_baixa = [
        "Selecionar", "Baixa Voluntária", "Baixa Forçada",
        "Baixa por Divida", "Baixa por Inspeção não Aprovada",
        "Rescisão Voluntária"
    ]

   
    st.set_page_config(page_title="Contratação", layout="wide")

    with st.sidebar:
        selected = option_menu(
            menu_title="Sub-Menu",
            options=["Cadastro", "Consulta Processo"],
            menu_icon="cast",
            default_index=0
        )

    # =========================
    # CADASTRO
    # =========================
    if selected == "Cadastro":

        st.header("Cadastro de Processos")

        intencao = st.selectbox(
            "Selecione a intenção",
            ["Novas Ligações", "Mudança de Nome", "Baixa de Serviço"]
        )

        # =====================================================
        # NOVAS LIGAÇÕES
        # =====================================================
        if intencao == "Novas Ligações":

            with st.form("form_novas_ligacoes"):

                tab1, tab2 = st.tabs(["📋 Dados do Cliente", "📄 Informações Adicionais"])

                with tab1:
                    loja_entrada = st.selectbox("Loja de entrada", lojas)
                    uc = st.selectbox("Unidade Comercial", ucs)
                    nome = st.text_input("Nome do cliente")
                    localidade = st.text_input("Localidade")
                    identificador = st.text_input("CNI ou Passaporte")
                    nif = st.text_input("NIF")
                    telefone = st.text_input("Telefone")
                    movel = st.text_input("Movel")
                    movel2 = st.text_input("Movel 2 (opcional)")
                    email, email_ok = validar_email("Email", key="email_nova")
                    nia = st.text_input("NIA (TARIFA SOCIAL)")
                    nivel_tarifario = st.selectbox("Nível tarifário (TARIFA SOCIAL)", niveis)

                with tab2:
                    tipo_servico = st.selectbox("Tipo de serviço", servicos)
                    tipo_ligacao = st.selectbox("Tipo de ligação", ligacoes)
                    tip_cliente = st.selectbox("Tipo de cliente", tip_clien)
                    entrada_processo = st.selectbox("Entrada do processo", entr_proc)
                    produto = st.selectbox("Produto", produtos)
                    operador = st.text_input("Operador responsável Entrada do Processo")

                    tem_divida = st.radio(
                        "TEM DÍVIDA? *",
                        ["Sim", "Não"],
                        index=None,
                        horizontal=True
                    )

                    st.markdown("### Coordenadas Geográficas")

                    col1, col2 = st.columns(2)

                    with col1:
                        latitude = st.number_input(
                            "Latitude (°)",
                            min_value=-90.0,
                            max_value=90.0,
                            format="%.6f"
                        )

                    with col2:
                        longitude = st.number_input(
                            "Longitude (°)",
                            min_value=-180.0,
                            max_value=180.0,
                            format="%.6f"
                        )

                    if latitude != 0.0 or longitude != 0.0:
                        st.map(pd.DataFrame({"lat": [latitude], "lon": [longitude]}), zoom=14)

                    uploaded_pdf = st.file_uploader(
                        "Carregar Processo do Cliente (PDF)",
                        type=["pdf"],
                        key="pdf_nova"
                    )

                    if uploaded_pdf:
                        pdf_preview = uploaded_pdf.getvalue()
                        st.success(f"PDF carregado: {uploaded_pdf.name}")
                        mostrar_pdf(pdf_preview)

                guardar = st.form_submit_button("💾 Guardar Nova Ligação")

                if guardar:
                    if not email_ok:
                        st.error("Corrija o email antes de gravar.")
                        st.stop()

                    pdf_nome = uploaded_pdf.name if uploaded_pdf else None
                    pdf_bytes = uploaded_pdf.getvalue() if uploaded_pdf else None

                    dados = {
                        "intencao": "Novas Ligações",
                        "loja_entrada": loja_entrada,
                        "unidade_comercial": uc,
                        "nome_cliente": nome,
                        "localidade": localidade,
                        "identificador": identificador,
                        "cni": None,
                        "nif": nif,
                        "telefone": telefone,
                        "movel": movel,
                        "movel2": movel2,
                        "email": email,
                        "nia": nia,
                        "nivel_tarifario": nivel_tarifario,
                        "cil": None,
                        "tipo_servico": tipo_servico,
                        "tipo_ligacao": tipo_ligacao,
                        "tipo_cliente": tip_cliente,
                        "entrada_processo": entrada_processo,
                        "produto": produto,
                        "operador": operador,
                        "tem_divida": tem_divida,
                        "latitude": latitude,
                        "longitude": longitude,
                        "uc_cliente": None,
                        "marca_aparelho": None,
                        "numero_serie": None,
                        "data_instalacao": None,
                        "tipo_baixa": None,
                        "motivo_baixa": None,
                        "servico_baixado": None,
                        "nome_pdf": pdf_nome,
                        "ficheiro_pdf": pdf_bytes
                    }

                    try:
                        guardar_processo(dados)
                        st.success("✅ Nova ligação gravada com sucesso!")
                    except Exception as e:
                        st.error(f"❌ Erro ao gravar no MySQL: {e}")

        # =====================================================
        # MUDANÇA DE NOME
        # =====================================================
        elif intencao == "Mudança de Nome":

            tab1, tab2 = st.tabs(["📋 Dados do Requisitante", "📄 Dados do Contrato"])

            with tab1:
                with st.form("form_requisitante_mudanca"):

                    loja_entrada = st.selectbox("Loja de entrada", lojas)
                    nome = st.text_input("Nome do cliente Requisitante")
                    cni = st.text_input("CNI ou Passaporte do cliente Requisitante")
                    nif = st.text_input("NIF do cliente Requisitante")
                    movel = st.text_input("Movel do cliente Requisitante")
                    movel2 = st.text_input("Movel 2 do cliente Requisitante (opcional)")
                    telefone = st.text_input("Telefone do cliente Requisitante")
                    email, email_ok = validar_email("Email do cliente Requisitante", key="email_mudanca")

                    guardar_requisitante = st.form_submit_button("Guardar Dados do Requisitante")

                    if guardar_requisitante:
                        st.success("Dados do requisitante preenchidos.")

            with tab2:

                lista_cils = buscar_cils_mysql()

                cil = st.selectbox(
                    "🔍 Pesquisar ou selecionar CIL",
                    options=lista_cils,
                    index=None,
                    placeholder="Digite para pesquisar...",
                    key="cil_mudanca_nome"
                )

                if cil:
                    cliente = buscar_cliente_mysql(cil)

                    if not cliente:
                        st.warning("Cliente não encontrado na base de dados.")
                        st.stop()

                    st.markdown("### Dados encontrados")

                    with st.form("form_mudanca_nome"):

                        st.text_input("Tipo de Cliente", value=cliente["tipo_cliente"], disabled=True)
                        st.text_input("UC", value=cliente["uc"], disabled=True)
                        st.text_input("Localidade", value=cliente["localidade"], disabled=True)
                        st.text_input("Produto", value=cliente["produto"], disabled=True)
                        st.text_input("Marca do Aparelho", value=cliente["marca_aparelho"], disabled=True)
                        st.text_input("Número de Série", value=cliente["numero_serie"], disabled=True)
                        st.text_input("Data de Instalação", value=cliente["data_instalacao"], disabled=True)

                        uploaded_pdf = st.file_uploader(
                            "Carregar Processo do Cliente (PDF)",
                            type=["pdf"],
                            key="pdf_mudanca"
                        )

                        if uploaded_pdf:
                            pdf_preview = uploaded_pdf.getvalue()
                            st.success(f"PDF carregado: {uploaded_pdf.name}")
                            mostrar_pdf(pdf_preview)

                        guardar_mudanca = st.form_submit_button("💾 Guardar Mudança de Nome")

                        if guardar_mudanca:
                            pdf_nome = uploaded_pdf.name if uploaded_pdf else None
                            pdf_bytes = uploaded_pdf.getvalue() if uploaded_pdf else None

                            dados = {
                                "intencao": "Mudança de Nome",
                                "loja_entrada": loja_entrada,
                                "unidade_comercial": None,
                                "nome_cliente": nome,
                                "localidade": cliente["localidade"],
                                "identificador": None,
                                "cni": cni,
                                "nif": nif,
                                "telefone": telefone,
                                "movel": movel,
                                "movel2": movel2,
                                "email": email,
                                "nia": None,
                                "nivel_tarifario": None,
                                "cil": cil,
                                "tipo_servico": None,
                                "tipo_ligacao": None,
                                "tipo_cliente": cliente["tipo_cliente"],
                                "entrada_processo": None,
                                "produto": cliente["produto"],
                                "operador": None,
                                "tem_divida": None,
                                "latitude": None,
                                "longitude": None,
                                "uc_cliente": cliente["uc"],
                                "marca_aparelho": cliente["marca_aparelho"],
                                "numero_serie": cliente["numero_serie"],
                                "data_instalacao": cliente["data_instalacao"],
                                "tipo_baixa": None,
                                "motivo_baixa": None,
                                "servico_baixado": None,
                                "nome_pdf": pdf_nome,
                                "ficheiro_pdf": pdf_bytes
                            }

                            try:
                                guardar_processo(dados)
                                st.success("✅ Mudança de nome gravada com sucesso!")
                            except Exception as e:
                                st.error(f"❌ Erro ao gravar no MySQL: {e}")

        # =====================================================
        # BAIXA DE SERVIÇO
        # =====================================================
        elif intencao == "Baixa de Serviço":

            st.subheader("Formulário: Baixa de Serviço")

            loja_entrada = st.selectbox("Loja de entrada", lojas, key="loja_baixa")
            nome = st.text_input("Nome do Requisitante", key="nome_baixa")
            cni = st.text_input("CNI ou Passaporte do Requisitante", key="cni_baixa")
            nif = st.text_input("NIF do Requisitante", key="nif_baixa")
            movel = st.text_input("Movel do Requisitante", key="movel_baixa")
            telefone = st.text_input("Telefone do Requisitante", key="telefone_baixa")
            email, email_ok = validar_email("Email do Requisitante", key="email_baixa")

            servico_baixa = st.selectbox("Serviço a ser baixado", servicos, key="servico_baixa")

            lista_cils = buscar_cils_mysql()

            cil = st.selectbox(
                "🔍 Pesquisar ou selecionar CIL",
                options=lista_cils,
                index=None,
                placeholder="Digite para pesquisar...",
                key="cil_baixa_servico"
            )

            tipo_baixa = st.selectbox("Tipo de Baixa", tip_baixa, key="tipo_baixa")

            with st.form("form_baixa_servico"):

                motivo_baixa = st.text_area("Motivo da baixa do serviço")
                operador = st.text_input("Operador responsável")

                uploaded_pdf = st.file_uploader(
                    "Carregar Documento de Baixa (PDF)",
                    type=["pdf"],
                    key="pdf_baixa"
                )

                if uploaded_pdf:
                    pdf_preview = uploaded_pdf.getvalue()
                    st.success(f"PDF carregado: {uploaded_pdf.name}")
                    mostrar_pdf(pdf_preview)

                guardar_baixa = st.form_submit_button("💾 Guardar Baixa de Serviço")

                if guardar_baixa:
                    if not email_ok:
                        st.error("Corrija o email antes de gravar.")
                        st.stop()

                    pdf_nome = uploaded_pdf.name if uploaded_pdf else None
                    pdf_bytes = uploaded_pdf.getvalue() if uploaded_pdf else None

                    dados = {
                        "intencao": "Baixa de Serviço",
                        "loja_entrada": loja_entrada,
                        "unidade_comercial": None,
                        "nome_cliente": nome,
                        "localidade": None,
                        "identificador": None,
                        "cni": cni,
                        "nif": nif,
                        "telefone": telefone,
                        "movel": movel,
                        "movel2": None,
                        "email": email,
                        "nia": None,
                        "nivel_tarifario": None,
                        "cil": cil,
                        "tipo_servico": None,
                        "tipo_ligacao": None,
                        "tipo_cliente": None,
                        "entrada_processo": None,
                        "produto": None,
                        "operador": operador,
                        "tem_divida": None,
                        "latitude": None,
                        "longitude": None,
                        "uc_cliente": None,
                        "marca_aparelho": None,
                        "numero_serie": None,
                        "data_instalacao": None,
                        "tipo_baixa": tipo_baixa,
                        "motivo_baixa": motivo_baixa,
                        "servico_baixado": servico_baixa,
                        "nome_pdf": pdf_nome,
                        "ficheiro_pdf": pdf_bytes
                    }

                    try:
                        guardar_processo(dados)
                        st.success("✅ Baixa de serviço gravada com sucesso!")
                    except Exception as e:
                        st.error(f"❌ Erro ao gravar no MySQL: {e}")

    # =========================
    # CONSULTA PROCESSO
    # =========================
    elif selected == "Consulta Processo":

        st.header("Consulta de Processos")

        with st.form("form_pesquisa_processos"):
            pesquisa_global = st.text_input(
                "🔎 Pesquisa Geral",
                placeholder="Digite ID, CNI, Nome ou CIL"
            )

            col1, col2 = st.columns(2)

            with col1:
                pesquisa_id = st.text_input("ID")
                pesquisa_cni = st.text_input("CNI")

            with col2:
                pesquisa_nome = st.text_input("Nome do Cliente")
                pesquisa_cil = st.text_input("CIL")

            pesquisar = st.form_submit_button("🔍 Pesquisar")

        if pesquisar:
            try:
                query = """
                    SELECT *
                    FROM processos_clientes
                    WHERE 1=1
                """

                params = {}

                if pesquisa_global.strip():
                    query += """
                        AND (
                            CAST(id AS CHAR) LIKE %(global)s
                            OR cni LIKE %(global)s
                            OR nome_cliente LIKE %(global)s
                            OR cil LIKE %(global)s
                        )
                    """
                    params["global"] = f"%{pesquisa_global.strip()}%"

                if pesquisa_id.strip():
                    query += " AND id = %(id)s"
                    params["id"] = pesquisa_id.strip()

                if pesquisa_cni.strip():
                    query += " AND cni LIKE %(cni)s"
                    params["cni"] = f"%{pesquisa_cni.strip()}%"

                if pesquisa_nome.strip():
                    query += " AND nome_cliente LIKE %(nome)s"
                    params["nome"] = f"%{pesquisa_nome.strip()}%"

                if pesquisa_cil.strip():
                    query += " AND cil LIKE %(cil)s"
                    params["cil"] = f"%{pesquisa_cil.strip()}%"

                query += " ORDER BY id DESC"

                if not params:
                    st.warning("Informe pelo menos um critério de pesquisa.")
                    st.stop()

                seleid = pd.read_sql(query, engine, params=params)

                if seleid.empty:
                    st.warning("Nenhum processo encontrado.")
                    st.stop()

                st.success(f"{len(seleid)} processo(s) encontrado(s).")

                seleid["label"] = (
                    "ID: " + seleid["id"].astype(str)
                    + " | " + seleid["intencao"].fillna("").astype(str)
                    + " | " + seleid["nome_cliente"].fillna("").astype(str)
                    + " | CIL: " + seleid["cil"].fillna("").astype(str)
                )

                escolha = st.selectbox(
                    "Escolha o processo",
                    seleid["label"].tolist()
                )

                id_sel = int(escolha.split("|")[0].replace("ID:", "").strip())
                row = seleid.loc[seleid["id"] == id_sel].iloc[0]

                with st.expander("📋 Dados do Processo", expanded=True):
                    st.text_input("Intenção", value=str(row.get("intencao", "") or ""), disabled=True)
                    st.text_input("Loja de Entrada", value=str(row.get("loja_entrada", "") or ""), disabled=True)
                    st.text_input("Nome Cliente/Requisitante", value=str(row.get("nome_cliente", "") or ""), disabled=True)
                    st.text_input("CNI", value=str(row.get("cni", "") or ""), disabled=True)
                    st.text_input("NIF", value=str(row.get("nif", "") or ""), disabled=True)
                    st.text_input("Telefone", value=str(row.get("telefone", "") or ""), disabled=True)
                    st.text_input("Móvel", value=str(row.get("movel", "") or ""), disabled=True)
                    st.text_input("Email", value=str(row.get("email", "") or ""), disabled=True)
                    st.text_input("CIL", value=str(row.get("cil", "") or ""), disabled=True)

                with st.expander("📄 Dados Técnicos", expanded=False):
                    st.text_input("Unidade Comercial", value=str(row.get("unidade_comercial", "") or ""), disabled=True)
                    st.text_input("UC Cliente", value=str(row.get("uc_cliente", "") or ""), disabled=True)
                    st.text_input("Localidade", value=str(row.get("localidade", "") or ""), disabled=True)
                    st.text_input("Tipo Cliente", value=str(row.get("tipo_cliente", "") or ""), disabled=True)
                    st.text_input("Produto", value=str(row.get("produto", "") or ""), disabled=True)
                    st.text_input("Tipo Serviço", value=str(row.get("tipo_servico", "") or ""), disabled=True)
                    st.text_input("Tipo Ligação", value=str(row.get("tipo_ligacao", "") or ""), disabled=True)
                    st.text_input("Entrada Processo", value=str(row.get("entrada_processo", "") or ""), disabled=True)
                    st.text_input("Operador", value=str(row.get("operador", "") or ""), disabled=True)

                with st.expander("📍 Coordenadas", expanded=False):
                    lat = float(row.get("latitude", 0.0) or 0.0)
                    lon = float(row.get("longitude", 0.0) or 0.0)

                    st.number_input("Latitude", value=lat, min_value=-90.0, max_value=90.0, format="%.6f", disabled=True)
                    st.number_input("Longitude", value=lon, min_value=-180.0, max_value=180.0, format="%.6f", disabled=True)

                    if lat != 0.0 or lon != 0.0:
                        st.map(pd.DataFrame({"lat": [lat], "lon": [lon]}), zoom=14)

                with st.expander("📄 Documento PDF", expanded=False):
                    pdf_bytes = row.get("ficheiro_pdf")
                    pdf_nome = row.get("nome_pdf") or "documento.pdf"

                    if pdf_bytes:
                        st.download_button(
                            "⬇️ Baixar PDF",
                            data=pdf_bytes,
                            file_name=pdf_nome,
                            mime="application/pdf"
                        )
                        mostrar_pdf(pdf_bytes)
                    else:
                        st.info("Este processo não possui PDF.")

            except Exception as e:
                st.error(f"Erro ao consultar processos: {e}")


if __name__ == "__main__":
    app()

