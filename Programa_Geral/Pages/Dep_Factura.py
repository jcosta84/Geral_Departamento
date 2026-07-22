from datetime import datetime
import sys
import os
import io
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from sqlalchemy import text, bindparam

from database.db import engine


def app():

    st.set_page_config(page_title="Facturação", layout="wide")

    # =========================
    # TABELAS AUXILIARES
    # =========================

    dados6 = [
        ['1', 'Janeiro'],
        ['2', 'Fevereiro'],
        ['3', 'Março'],
        ['4', 'Abril'],
        ['5', 'Maio'],
        ['6', 'Junho'],
        ['7', 'Julho'],
        ['8', 'Agosto'],
        ['9', 'Setembro'],
        ['10', 'Outubro'],
        ['11', 'Novembro'],
        ['12', 'Dezembro']
    ]

    refmes = pd.DataFrame(dados6, columns=['Me', 'Mês'])
    refmes.set_index('Me', inplace=True)

    colunas = [
        'BOA IND', 'EMP ID', 'UC', 'Prod', 'DT_PROC', 'DT_FACT', 'NR_FACT',
        'CLI_ID', 'CLI_CONTA', 'CIL', 'TP_FACT', 'TP_CLI', 'COD_TARIFA',
        'VAL_TOT', 'CONCEITO', 'QTDE', 'VALOR'
    ]

    # =========================
    # FUNÇÕES
    # =========================

    def carregar_filtros_facturacao():
        query = """
            SELECT DISTINCT
                Regiao,
                YEAR(DT_FACT) AS Ano,
                MONTH(DT_FACT) AS Mes
            FROM facturacao
            WHERE CONCEITO = 'X30'
            ORDER BY Regiao, Ano, Mes
        """
        return pd.read_sql(query, engine)

    def tratar_factura_filtrada(regioes, anos, meses):
        query = text("""
            SELECT *
            FROM facturacao
            WHERE CONCEITO = 'X30'
            AND Regiao IN :regioes
            AND YEAR(DT_FACT) IN :anos
            AND MONTH(DT_FACT) IN :meses
        """)

        query = query.bindparams(
            bindparam("regioes", expanding=True),
            bindparam("anos", expanding=True),
            bindparam("meses", expanding=True)
        )

        params = {
            "regioes": regioes,
            "anos": anos,
            "meses": meses
        }

        factura2 = pd.read_sql(query, engine, params=params)

        if factura2.empty:
            return factura2

        factura2 = factura2.drop_duplicates(subset='NR_FACT')

        factura2['CIL'] = factura2['CIL'].astype(str)
        factura2['CLI_ID'] = factura2['CLI_ID'].astype(str)
        factura2['CLI_CONTA'] = factura2['CLI_CONTA'].astype(str)

        factura2['DT_PROC'] = pd.to_datetime(
            factura2['DT_PROC'],
            errors='coerce'
        ).dt.date

        factura2['DT_FACT'] = pd.to_datetime(
            factura2['DT_FACT'],
            errors='coerce'
        )

        factura2['Ano'] = factura2['DT_FACT'].dt.year.astype(str)
        factura2['Me'] = factura2['DT_FACT'].dt.month.astype(str)
        factura2['DT_FACT'] = factura2['DT_FACT'].dt.date

        factura3 = pd.merge(factura2, refmes, on='Me', how='left')

        factura3 = factura3.rename(columns={
            'CLI_ID': 'Cliente',
            'CLI_CONTA': 'Cliente Conta',
            'Tipo_Cliente': 'Tipo Cliente',
            'Tipo_Factura': 'Tipo Factura',
            'NR_FACT': 'Nº Factura',
            'DT_PROC': 'Data Processamento',
            'DT_FACT': 'Data Facturação',
            'VAL_TOT': 'Valor Facturado',
            'QTDE': 'Kwh',
            'VALOR': 'Valor Cons (ECV)'
        })

        factura3 = factura3[[
            'Ano', 'Regiao', 'Unidade', 'CIL', 'Cliente',
            'Cliente Conta', 'Tipo Cliente', 'Produto',
            'Tipo Factura', 'Nº Factura', 'Mês',
            'Data Processamento', 'Data Facturação',
            'Tarifa', 'Valor Facturado', 'CONCEITO',
            'Kwh', 'Valor Cons (ECV)'
        ]]

        return factura3

    def importar_contratos():
        query = "SELECT * FROM contratos"
        contratos2 = pd.read_sql(query, engine)

        contratos2['DT_Contrato'] = pd.to_datetime(
            contratos2['DT_Contrato'],
            format='%Y%m%d',
            errors='coerce'
        ).dt.strftime('%d-%m-%Y')

        contratos2['DT_Inicio'] = pd.to_datetime(
            contratos2['DT_Inicio'],
            format='%Y%m%d',
            errors='coerce'
        ).dt.strftime('%d-%m-%Y')

        contratos2['DT_Baixa'] = pd.to_datetime(
            contratos2['DT_Baixa'],
            format='%Y%m%d',
            errors='coerce'
        ).dt.strftime('%d-%m-%Y')

        return contratos2

    def classificar_maturidade(media):
        if media == 0:
            return "0"
        elif 1 <= media <= 20:
            return "1 a 20"
        elif 21 <= media <= 30:
            return "21 a 30"
        elif 31 <= media <= 40:
            return "31 a 40"
        elif 41 <= media <= 60:
            return "41 a 60"
        elif 61 <= media <= 100:
            return "61 a 100"
        elif 101 <= media <= 200:
            return "101 a 200"
        elif 201 <= media <= 300:
            return "201 a 300"
        elif 301 <= media <= 400:
            return "301 a 400"
        elif 401 <= media <= 500:
            return "401 a 500"
        elif 501 <= media <= 1000:
            return "501 a 1000"
        elif 1001 <= media <= 5000:
            return "1001 a 5000"
        elif 5001 <= media <= 20000:
            return "5001 a 20000"
        elif media > 20000:
            return "> 20000"
        else:
            return "Valor inválido"

    @st.cache_data
    def convert_df(df):
        return df.to_csv(
            sep=';',
            decimal=',',
            index=False
        ).encode('utf-8-sig')

    # =========================
    # MENU
    # =========================

    with st.sidebar:
        selected = option_menu(
            menu_title="Sub-Menu",
            options=["Importação", "Dashboard", "Analise Maturidade"],
            menu_icon="cast",
            default_index=0
        )

    # =========================
    # IMPORTAÇÃO
    # =========================

    if selected == "Importação":
        st.header("Importação de Script Facturação")

        upload_file = st.file_uploader("Importar Facturação", type=["txt"])

        if upload_file:
            content = upload_file.read().decode("utf-8")
            factura = pd.read_csv(
                io.StringIO(content),
                sep='\t',
                names=colunas
            )

            st.dataframe(factura, use_container_width=True)

            if st.button("Guardar Facturação"):
                try:
                    with engine.begin() as conn:
                        factura.to_sql(
                            "facturacao",
                            con=conn,
                            if_exists="append",
                            index=False,
                            chunksize=10000
                        )

                    st.success("Dados inseridos com sucesso!")

                except Exception as e:
                    st.error(f"Erro ao inserir dados: {e}")

    # =========================
    # DASHBOARD
    # =========================

    if selected == "Dashboard":
        st.title("Dashboard")

        filtros = carregar_filtros_facturacao()

        if filtros.empty:
            st.warning("Não existem dados de facturação na base de dados.")
            st.stop()

        col1, col2, col3 = st.columns(3)

        with col1:
            reg = st.multiselect(
                "Definir Região:",
                options=sorted(filtros['Regiao'].dropna().unique())
            )

        with col2:
            an = st.multiselect(
                "Definir Ano:",
                options=sorted(filtros['Ano'].dropna().unique())
            )

        with col3:
            me = st.multiselect(
                "Definir Mês:",
                options=sorted(filtros['Mes'].dropna().unique())
            )

        if not reg or not an or not me:
            st.warning("Defina Região, Ano e Mês para carregar os dados.")
            st.stop()

        geral_selection3 = tratar_factura_filtrada(reg, an, me)

        if geral_selection3.empty:
            st.warning("Nenhum dado encontrado para os filtros selecionados.")
            st.stop()

        tabdinamica = geral_selection3.pivot_table(
            index=['Unidade'],
            values=['Valor Facturado', 'Kwh'],
            aggfunc='sum',
            fill_value=0
        )

        tabdinamica2 = geral_selection3.pivot_table(
            index=['Tipo Cliente'],
            values=['Valor Facturado', 'Kwh'],
            aggfunc='sum',
            fill_value=0
        )

        tabdinamica3 = geral_selection3.pivot_table(
            index=['Produto'],
            values=['Valor Facturado', 'Kwh'],
            aggfunc='sum',
            fill_value=0
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.header("Facturação Por Unidade")
            st.dataframe(tabdinamica, use_container_width=True)

        with col2:
            st.header("Facturação Por Tipo Cliente")
            st.dataframe(tabdinamica2, use_container_width=True)

        with col3:
            st.header("Facturação Por Produto")
            st.dataframe(tabdinamica3, use_container_width=True)

        fig_ucval = px.bar(
            tabdinamica,
            x=tabdinamica.index,
            y='Valor Facturado',
            title="Gráfico Valor Facturado Por Unidade",
            template="plotly_white"
        )

        fig_ucquant = px.bar(
            tabdinamica,
            x=tabdinamica.index,
            y='Kwh',
            title="Gráfico Consumo Por Unidade",
            template="plotly_white"
        )

        st.header("Gráfico Unidade Comercial")

        left_column, right_column = st.columns(2)
        left_column.plotly_chart(fig_ucval, use_container_width=True)
        right_column.plotly_chart(fig_ucquant, use_container_width=True)

        st.markdown("---")

        fig_tipval = px.bar(
            tabdinamica2,
            x=tabdinamica2.index,
            y='Valor Facturado',
            title="Gráfico Valor Facturado Por Tipo Cliente",
            template="plotly_white"
        )

        fig_tipquant = px.bar(
            tabdinamica2,
            x=tabdinamica2.index,
            y='Kwh',
            title="Gráfico Consumo Por Tipo Cliente",
            template="plotly_white"
        )

        st.header("Gráfico Tipo de Cliente")

        left_column, right_column = st.columns(2)
        left_column.plotly_chart(fig_tipval, use_container_width=True)
        right_column.plotly_chart(fig_tipquant, use_container_width=True)

        st.markdown("---")

        fig_proval = px.bar(
            tabdinamica3,
            x=tabdinamica3.index,
            y='Valor Facturado',
            title="Gráfico Valor Facturado Por Produto",
            template="plotly_white"
        )

        fig_proquant = px.bar(
            tabdinamica3,
            x=tabdinamica3.index,
            y='Kwh',
            title="Gráfico Consumo Por Produto",
            template="plotly_white"
        )

        st.header("Gráfico Produto")

        left_column, right_column = st.columns(2)
        left_column.plotly_chart(fig_proval, use_container_width=True)
        right_column.plotly_chart(fig_proquant, use_container_width=True)

        st.markdown("---")
        st.header("Quadro Facturação")

        quadro = geral_selection3[[
            'Unidade', 'CIL', 'Cliente', 'Cliente Conta',
            'Tipo Cliente', 'Produto', 'Tipo Factura',
            'Nº Factura', 'Data Processamento',
            'Data Facturação', 'Tarifa',
            'Valor Facturado', 'CONCEITO',
            'Kwh', 'Valor Cons (ECV)'
        ]]

        st.dataframe(quadro, use_container_width=True, hide_index=True)

        csv = convert_df(quadro)

        st.download_button(
            label="Download Facturação",
            data=csv,
            file_name='Script Facturação Tratado.csv',
            mime='text/csv'
        )

    # =========================
    # ANÁLISE MATURIDADE
    # =========================

    if selected == "Analise Maturidade":
        st.title("Análise de Maturidade de Clientes")

        filtros = carregar_filtros_facturacao()

        if filtros.empty:
            st.warning("Não existem dados de facturação na base de dados.")
            st.stop()

        col1, col2, col3 = st.columns(3)

        with col1:
            reg = st.multiselect(
                "Definir Região:",
                options=sorted(filtros['Regiao'].dropna().unique())
            )

        with col2:
            an = st.multiselect(
                "Definir Ano:",
                options=sorted(filtros['Ano'].dropna().unique())
            )

        with col3:
            me = st.multiselect(
                "Definir Mês:",
                options=sorted(filtros['Mes'].dropna().unique())
            )

        if not reg or not an or not me:
            st.warning("Defina Região, Ano e Mês para carregar os dados.")
            st.stop()

        facturas_maturidade = tratar_factura_filtrada(reg, an, me)

        if facturas_maturidade.empty:
            st.warning("Nenhum dado encontrado para os filtros selecionados.")
            st.stop()

        contratos_geral = importar_contratos()

        tab_di = pd.pivot_table(
            facturas_maturidade,
            index=['CIL', 'Cliente Conta'],
            columns='Mês',
            values='Kwh',
            aggfunc='sum',
            fill_value=0
        )

        tab_di['Media Consumo Geral'] = tab_di.sum(axis=1)

        tab_di["Maturidade de consumo"] = tab_di[
            "Media Consumo Geral"
        ].apply(classificar_maturidade)

        tab_di = tab_di.reset_index()

        tab_di['CIL Conta'] = (
            tab_di['CIL'].astype(str) +
            ' - ' +
            tab_di['Cliente Conta'].astype(str)
        )

        contratos_geral['CIL Conta'] = (
            contratos_geral['CIL'].astype(str) +
            ' - ' +
            contratos_geral['CLI_Conta'].astype(str)
        )

        contratos_geral = contratos_geral[[
            "CIL Conta", "Regiao", "Unidade", "NIP", "Porta", "CGV",
            "Tipo_Cliente", "Nome", "Morada", "Localidade",
            "Produto", "Cod_Tarifa", "Seq_Contrato",
            "Estado_Contrato", "DT_Contrato", "DT_Inicio", "DT_Baixa"
        ]]

        contdi = pd.merge(
            tab_di,
            contratos_geral,
            on='CIL Conta',
            how='left'
        )

        tabdicont = pd.pivot_table(
            contdi,
            index=['Maturidade de consumo'],
            values='CIL',
            aggfunc='count',
            fill_value=0
        )

        tabdicont2 = pd.pivot_table(
            contdi,
            index=['Maturidade de consumo'],
            values='Media Consumo Geral',
            aggfunc='sum',
            fill_value=0
        )

        tb_ge = pd.merge(
            tabdicont,
            tabdicont2,
            on='Maturidade de consumo',
            how='left'
        )

        col1, col2 = st.columns(2)

        with col1:
            st.header("Resumo por Maturidade")
            st.dataframe(tb_ge, use_container_width=True)

        with col2:
            matu = st.multiselect(
                "Definir Maturidade:",
                options=sorted(contdi['Maturidade de consumo'].dropna().unique())
            )

        if matu:
            geral_mat = contdi.query(
                "`Maturidade de consumo` == @matu"
            )
        else:
            geral_mat = contdi

        st.header("Quadro de Maturidade")
        st.dataframe(geral_mat, use_container_width=True)

        csv = convert_df(geral_mat)

        st.download_button(
            label="Download Análise Maturidade",
            data=csv,
            file_name='Script Facturação Por Maturidade.csv',
            mime='text/csv'
        )

if __name__ == "__main__":
    app()