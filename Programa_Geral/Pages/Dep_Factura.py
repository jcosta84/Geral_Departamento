from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from database.db import engine  # Usar engine, não SessionLocal
import re
import io
import plotly.express as px

#def app():
    
# --- Criação de tabelas adicionais para cruzamentos durante o programa ---
#tabela Unidade
dados = [['10201000', 'Praia'],
         ['10202000', 'São Domingos'],
         ['10203000', 'Santa Catarina'],
         ['10204000', 'Tarrafal'],
         ['10205000', 'Calheta'],
         ['10206000', 'Santa Cruz'],
         ['10701000', 'Mosteiros'],
         ['10702000', 'São Filipe'],
         ['10801000', 'Maio'],
         ['10901000', 'Brava'],
         ['10101000', 'Mindelo'],
         ['10301000', 'SAL'],
         ['10401000', 'BOAVISTA'],
         ['10501000', 'VILA DA RIBEIRA BRAVA'],
         ['10601000', 'R.GRANDE - N.S.Rosário'],
         ['10602000', 'PORTO NOVO - S.João Baptista'],
         ['10603000', 'PAUL - S.António das Pombas'],
         ['10502000', 'Tarrafal S.Nicolau'],
         ['10000000', 'Electra SUL']
         ]
unidade = pd.DataFrame(dados, columns=['UC', 'Unidade'])
unidade['UC'] = unidade['UC'].astype(int)
unidade.set_index('UC', inplace=True)
#tabela Produto
dados2 = [['EB', 'Baixa Tensão'],
          ['EE', 'Baixa Tensão Especial'],
          ['EM', 'Media Tensão'],
          ['AG', 'Agua']
          ]
produto = pd.DataFrame(dados2, columns=['Prod', 'Produto'])
produto.set_index('Prod', inplace=True)
#tabela Tipo Factura
dados3 = [['11', 'Em Ciclo Leitura'],
          ['12', 'Em Ciclo Estimativa'],
          ['22', 'Baixa Voluntária'],
          ['23', 'Baixa por Dívida'],
          ['24', 'Alterações Contratuais'],
          ['28', 'Baixa Forçada'],
          ['29', 'Substit. Modif.'],
          ['30', 'Substituição'],
          ['33', 'Acerto de Cobrança'],
          ['39', 'Facturação Diversa'],
          ['99', 'Lig Relig CompPg']
          ]
tp_fact = pd.DataFrame(dados3, columns=['TP_FACT', 'Tipo_Factura'])
tp_fact['TP_FACT'] = tp_fact['TP_FACT'].astype(int)
tp_fact.set_index('TP_FACT', inplace=True)
#tabela Tipo Cliente
dados4 = [['72', 'Empresa Publica'],
          ['82', 'Colectivos'],
          ['93', 'Industriais'],
          ['94', 'Construção'],
          ['73', 'Estado-Patrimonio'],
          ['91', 'Domésticos'],
          ['92', 'Comércio, Industria, Agricul.'],
          ['21', 'Consumos Próprios'],
          ['31', 'Autarquias'],
          ['51', 'Instituições'],
          ['71', 'Estado-Tesouro'],
          ['XX', 'Clientes Senhas de Água'],
          ]
tip_client = pd.DataFrame(dados4, columns=['TP_CLI', 'Tipo_Cliente'])
tip_client['TP_CLI'] = tip_client['TP_CLI'].astype(str)
tip_client.set_index('TP_CLI', inplace=True)
#tabela Tarifa
dados5 = [['A1', 'Tarifa Água I'],
            ['A2', 'Tarifa Água II'],
            ['A3', 'Tarifa Água III B'],
            ['A4', 'Tarifa Água III A'],
            ['A5', 'Tarifa Água II (Turismo)'],
            ['AD', 'ADA'],
            ['AP', 'Água Praia'],
            ['B4', 'Autotanques II'],
            ['CD', 'Central Dessalinizadora'],
            ['CP', 'Consumos Proprios'],
            ['R4', 'Autotanques I (Social)'],
            ['SA', 'Senhas de Água'],
            ['XX', 'Venda de Água Avulso'],
            ['AV', 'Avença'],
            ['CE', 'Caixa de Escada'],
            ['CP', 'Consumos Proprios'],
            ['D1', 'Tarifa D'],
            ['D11', 'Tarifa D'],
            ['D2', 'Tarifa D-S. Nicolau'],
            ['D3', 'Tarifa D-Social-S. Nicolau'],
            ['D4', 'Tarifa D - Maio'],
            ['D5', 'Tarifa D - Social - Maio'],
            ['DS', 'Tarifa D - Social'],
            ['IP', 'Iluminação Publica'],
            ['LM', 'Ligação Provisória - MONO'],
            ['LP', 'Ligação Provisória'],
            ['LT', 'Ligação Provisória - TRI'],
            ['LU', 'Ligação Provisória - MONO URG'],
            ['S1', 'Tarifa Social'],
            ['SF', 'Semáfores'],
            ['T1', 'Trabalhador Electra-S. Nicolau'],
            ['T2', 'Trab. Electra Is.RTC-S.Nicolau'],
            ['T3', 'Trabalhador Electra - Maio'],
            ['T4', 'Trab. Electra Is. RTC - Maio'],
            ['TB', 'Trabalhador Electra'],
            ['TI', 'Trab. Electra Isento RTC'],
            ['TU', 'Ligação Provisória - TRI URG'],
            ['AV', 'Tarifa Avença'],
            ['E1', 'Tarifa BTE 1'],
            ['E2', 'Tarifa BTE'],
            ['S1', 'Tarifa Social'],
            ['M1', 'Tarifa MT 1'],
            ['M2', 'Tarifa MT'],
            ['M3', 'Tarifa MT'],
            ['S1', 'Tarifa Social'],
            ['TBP', 'Trabalhador Partilhado'],
            ['TBB', 'Trab. Beneficiário']
          ]
tarifa = pd.DataFrame(dados5, columns=['COD_TARIFA', 'Tarifa'])
tarifa['COD_TARIFA'] = tarifa['COD_TARIFA'].astype(str)
tarifa.set_index('COD_TARIFA', inplace=True)
#tabela de mês de numero para texto
dados6 = [['1', 'Janeiro'],
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
          ['12', 'Dezembro'],

]
refmes = pd.DataFrame(dados6, columns=['Me', 'Mês'])
refmes.set_index('Me', inplace=True)
# definir roteiro qual unidade comercial usar
dados7 = [["Avenças PRAIA", "Praia"],
            ["GC REMOTA", "Praia"],
            ["MICRO PR", "Praia"],
            ["IP PRAIA REMOTA", "Praia"],
            ["IP PRAIA", "Praia"],
            ["MT", "Praia"],
            ["Praia GC I", "Praia"],
            ["Praia GC II", "Praia"],
            ["Praia GC III", "Praia"],
            ["Praia", "Praia"],
            ["Rural", "Praia"],
            ["ADS - S.Domingos", "São Domingos"],
            ["MICRO SD", "São Domingos"],
            ["Avenças S.DOMINGOS", "São Domingos"],
            ["MT S.DOMINGOS", "São Domingos"],
            ["Milho Branco", "São Domingos"],
            ["Praia Baixo e Praia Formosa", "São Domingos"],
            ["Roteiro IP S.DOMINGOS REMOTA", "São Domingos"],
            ["S.DOMINGOS GC", "São Domingos"],
            ["S.DOMINGOS", "São Domingos"],
            ["ADS - Assomada", "Santa Catarina"],
            ["MICRO AS", "Santa Catarina"],
            ["Assomada", "Santa Catarina"],
            ["GC Santa Catarina", "Santa Catarina"],
            ["Picos", "Santa Catarina"],
            ["Roteiro IP Santa Catarina", "Santa Catarina"],
            ["Rª da Barca", "Santa Catarina"],
            ["ADS - Tarrafal", "Tarrafal"],
            ["MICRO TA", "Tarrafal"],
            ["Roteiro IP TARRAFAL", "Tarrafal"],
            ["Tarrafal - CHÃO BOM", "Tarrafal"],
            ["Tarrafal - VILA", "Tarrafal"],
            ["Tarrafal-Rural", "Tarrafal"],
            ["ADS - Calheta", "Calheta"],
            ["MICRO CA", "Calheta"],
            ["CALHETA I", "Calheta"],
            ["CALHETA II", "Calheta"],
            ["Calheta GCI", "Calheta"],
            ["Calheta", "Calheta"],
            ["Flamengos", "Calheta"],
            ["MIGUEL GOMES", "Calheta"],
            ["PIZARRA", "Calheta"],
            ["RIBEIRA PILÃO BRANCO", "Calheta"],
            ["Roteiro IP CALHETA", "Calheta"],
            ["Veneza", "Calheta"],
            ["ADS - Santa Cruz", "Santa Cruz"],
            ["MICRO SC", "Santa Cruz"],
            ["ORGÃOS", "Santa Cruz"],
            ["Roteiro IP SANTA CRUZ", "Santa Cruz"],
            ["SANTA CRUZ GCI", "Santa Cruz"],
            ["SANTA CRUZ RP", "Santa Cruz"],
            ["SANTA CRUZ RURAL", "Santa Cruz"],
            ["SANTA CRUZ SA", "Santa Cruz"],
            ["VILA PEDRA BADEJO", "Santa Cruz"],
            ["IP MOSTEIROS", "Mosteiros"],
            ["MOSTEIROS GC", "Mosteiros"],
            ["MICRO MO", "Mosteiros"],
            ["Mosteiro-Rural", "Mosteiros"],
            ["Mosteiros", "Mosteiros"],
            ["MICRO MO", "Mosteiros"],
            ["CLIENTES BT", "São Filipe"],
            ["Clientes IP", "São Filipe"],
            ["CLIENTES MT", "São Filipe"],
            ["SAO FILIPE GC", "São Filipe"],
            ["MICRO SF", "São Filipe"],
            ["Barreiro-Rural", "Maio"],
            ["Calheta-Rural", "Maio"],
            ["Figueira da Horta/Seca-Rural", "Maio"],
            ["IP MAIO", "Maio"],
            ["MAIO GC", "Maio"],
            ["Morrinho-Rural", "Maio"],
            ["Morro-Rural", "Maio"],
            ["NORTE RURAL", "Maio"],
            ["Ribeira D.João-Rural", "Maio"],
            ["VILA P.Ingles", "Maio"],
            ["MICRO MA", "Maio"],
            ["BRAVA GC", "Brava"],
            ["IP BRAVA", "Brava"],
            ["MICRO BR", "Brava"],
            ["NSM Rural", "Brava"],
            ["SJB Rural", "Brava"],
            ["VN Sintra", "Brava"]
            ]
uc = pd.DataFrame(dados7, columns=['Roteiro', 'Unidade'])
# criar tabela de função
dados8 = [
        ["11", "Ativa"],
        ["12", "Ativa"],
        ["21", "Agua"],
        ["41", "Ativa"],
        ["49", "Reativa"],
        ["61", "Ativa"],
        ["69", "Reativa"],
        ["71", "Ponta"],
    ]
funcao = pd.DataFrame(dados8, columns=['Função', 'Descrição'])
# converter na função a coluna para formato inteiro
funcao['Função'] = funcao['Função'].astype(int)
# criar tabela de regiao
dados9 = [['Praia', 'SUL'],
         ['São Domingos', 'SUL'],
         ['Santa Catarina', 'SUL'],
         ['Tarrafal', 'SUL'],
         ['Calheta', 'SUL'],
         ['Santa Cruz', 'SUL'],
         ['Mosteiros', 'SUL'],
         ['São Filipe', 'SUL'],
         ['Maio', 'SUL'],
         ['Brava', 'SUL'],
         ['Mindelo', 'NORTE'],
         ['SAL', 'NORTE'],
         ['BOAVISTA', 'NORTE'],
         ['VILA DA RIBEIRA BRAVA', 'NORTE'],
         ['R.GRANDE - N.S.Rosário', 'NORTE'],
         ['PORTO NOVO - S.João Baptista', 'NORTE'],
         ['PAUL - S.António das Pombas', 'NORTE'],
         ['Tarrafal S.Nicolau', 'NORTE'],
         ['EDEC']
         ]
regiao = pd.DataFrame(dados9, columns=['Unidade', 'Regiao'])
regiao.set_index('Unidade', inplace=True)
# criar tabela de estado de contrato
dados10 = [['0', 'Sem Contrato'],
           ['10', 'React. Pendente OS'],
           ['11', 'Pendente, Inspec, Não Aprovada'],
           ['12', 'Contrato em Vigor'],
           ['13', 'Reactivada de Inspecção'],
           ['14', 'Contrato Novo Ainda não Facturado'],
           ['15', 'Contrato Novo Pendente de OS'], 
           ['17', 'Pend. Suspensão por Inspecção'],
           ['18', 'Suspenso por Inspecção'],
           ['19', 'Pend. Bai. Inspec não Aprovada'],
           ['21', 'Rescisão Voluntaria'],
           ['25', 'Baixa por Dívida'],
           ['27', 'Baixa Forçada'],
           ['28', 'Baixa por Inspec. não Aprovada']]
est_contr = pd.DataFrame(dados10, columns=['EST CONTR', 'Estado Contrato'])
#est_contr.set_index('EST CONTR', inplace=True)

#lista uc's
local = pd.DataFrame({"UCS": ["Praia", "São Domingos", "Santa Catarina", "Tarrafal", "Calheta", "Santa Cruz", "São Filipe", "Mosteiros", "Maio", "Brava"]})
produtos = pd.DataFrame({"Prod": ["Baixa Tensão", "Baixa Tensão Especial", "Media Tensão"]})

#criar cabeçalho Facturação
colunas = ['BOA IND', 'EMP ID', 'UC', 'Prod', 'DT_PROC', 'DT_FACT', 'NR_FACT', 'CLI_ID', 'CLI_CONTA', 'CIL',
           'TP_FACT', 'TP_CLI', 'COD_TARIFA', 'VAL_TOT', 'CONCEITO', 'QTDE', 'VALOR']

#criar cabeçalho contros
colunas2 = [
    "EMP ID", "UC", "USR ID", "NIP", "PORTA", "CIL", "SIS ABAST", "CGV",
    "CLI CONTA", "TP_CLI", "CAE ID", "TP USO", "NOME", "MORADA", "LOCALIDADE",
    "COD LOCAL", "Prod", "COD TARIFA", "SEQ CONTR", "EST CONTR",
    "DT CONTRATO", "DT INICIO", "DT BAIXA", "OBS", "REF", ""
]


#definir importação e tratamento do script facturação
def tratar_factura():
    query = "SELECT * FROM facturacao"
    factura2 = pd.read_sql(query, engine)
    #filtrar consumo
    factura2 = factura2.loc[factura2['CONCEITO'] == 'X30']
    #remover duplicado
    factura2 = factura2.drop_duplicates(subset='NR_FACT')
    #alterar formato para str
    factura2['CIL'] = factura2['CIL'].astype(str)
    factura2['CLI_ID'] = factura2['CLI_ID'].astype(str)
    factura2['CLI_CONTA'] = factura2['CLI_CONTA'].astype(str)
    factura2['DT_PROC'] = factura2['DT_PROC'].astype(str)
    factura2['DT_PROC'] = pd.to_datetime(factura2['DT_PROC'])
    factura2['DT_PROC'] = factura2['DT_PROC'].dt.date
    factura2['DT_FACT'] = factura2['DT_FACT'].astype(str)
    factura2['DT_FACT'] = pd.to_datetime(factura2['DT_FACT'])
    factura2['Ano'] = factura2['DT_FACT'].dt.year
    factura2['Me'] = factura2['DT_FACT'].dt.month
    factura2['Me'] = factura2['Me'].astype(str)
    factura2['Ano'] = factura2['Ano'].astype(str)
    factura2['DT_FACT'] = factura2['DT_FACT'].dt.date
    factura3 = pd.merge(factura2, refmes, on='Me', how='left')
    factura3 = factura3[['Ano', 'Regiao', 'Unidade', 'CIL', 'CLI_ID', 'CLI_CONTA', 'Tipo_Cliente','Produto', 'Tipo_Factura', 'NR_FACT',  'Mês',
                            'DT_PROC', 'DT_FACT', 'Tarifa', 'VAL_TOT', 'CONCEITO', 'QTDE', 'VALOR']]

    #alterar nome das colunas
    factura3 = factura3.rename(columns={'CLI_ID': 'Cliente'})
    factura3 = factura3.rename(columns={'CLI_CONTA': 'Cliente Conta'})
    factura3 = factura3.rename(columns={'Tipo_Cliente': 'Tipo Cliente'})
    factura3 = factura3.rename(columns={'Tipo_Factura': 'Tipo Factura'})
    factura3 = factura3.rename(columns={'NR_FACT': 'Nº Factura'})
    factura3 = factura3.rename(columns={'DT_PROC': 'Data Processamento'})
    factura3 = factura3.rename(columns={'DT_FACT': 'Data Facturação'})
    factura3 = factura3.rename(columns={'VAL_TOT': 'Valor Facturado'})
    factura3 = factura3.rename(columns={'QTDE': 'Kwh'})
    factura3 = factura3.rename(columns={'VALOR': 'Valor Cons (ECV)'})    
    
    return factura3

#criar dados se para maturidade
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
    
# --- Configuração da página ---
st.set_page_config(page_title="Facturação", layout="wide")

# --- Menu lateral ---
with st.sidebar:
    selected = option_menu(
        menu_title="Menu Principal",
        options=["Importação", "Dashboard", "Analise Maturidade"],
        menu_icon="cast",
        default_index=0
    )

# --- Importação ---
if selected == "Importação":
    st.header("Importação de Dados de Contagens")

    #query importar facturação
    query = "SELECT * FROM facturacao"
    upload_file = st.file_uploader("Importar Facturação", type=["txt"])
    if upload_file:
        st.markdown("---")
        content = upload_file.read().decode("utf-8")
        factura = pd.read_csv(io.StringIO(content), sep='\t', names=colunas)
        factuc = pd.merge(factura, unidade, on='UC', how='left')
        prodfact = pd.merge(factuc, produto, on='Prod', how='left')
        tpfact = pd.merge(prodfact, tp_fact, on='TP_FACT', how='left')
        tpfact['TP_CLI'] = tpfact['TP_CLI'].astype(str)
        clifact = pd.merge(tpfact, tip_client, on='TP_CLI', how='left')
        confact = pd.merge(clifact, tarifa, on='COD_TARIFA', how='left')
        regfact = pd.merge(confact, regiao, on='Unidade', how='left')

        #organizar estrutura
        regfact = regfact[['Regiao', 'Unidade', 'CIL', 'CLI_ID', 'CLI_CONTA', 'Tipo_Cliente','Produto', 'Tipo_Factura', 'NR_FACT', 'DT_PROC', 'DT_FACT', 'Tarifa', 
                            'VAL_TOT', 'CONCEITO', 'QTDE', 'VALOR']]
        
        #filtar conceito x30 na tabela
        regfact = regfact.loc[regfact['CONCEITO'] == 'X30']
        
        #função de carregar factura na base de dados    
        if st.button("Guardar Facturação"):
            try:
                with engine.begin() as conn:
                    regfact.to_sql(
                        "facturacao",
                        con=conn,
                        if_exists="append",
                        index=False,
                        chunksize=10000  # insere em blocos de 10 mil linhas
                    )
                st.success("Dados inseridos com sucesso!")
            except Exception as e:
                st.error(f"Erro ao inserir dados: {e}")

#campo de Dashboard
if selected == "Dashboard":
    st.title("Dashboard")
    facturas_tratadas = tratar_factura()

    #dividir em colunas
    col1, col2, col3 = st.columns(3)

    #col1
    with col1:
        #filtrar região
        reg = st.multiselect(
            "Definir Região: ",
            options=facturas_tratadas['Regiao'].unique(),
        )

        geral_selection = facturas_tratadas.query(
            "`Regiao` == @reg"
        )
    
    #col2
    with col2:
        #filtar ano
        an = st.multiselect(
            "Definir Ano: ",
            options=geral_selection['Ano'].unique(),

        )
        geral_selection2 = geral_selection.query(
            "`Ano` == @an"
        )

    #col3
    with col3:
        #filtrar mês
        me = st.multiselect(
            "Definir Mês",
            options=geral_selection2['Mês'].unique(),

        )
        geral_selection3 = geral_selection2.query(
            "`Mês` == @me"
        )
    
    #criação de tabela dinamica por unidade
    tabdinamica = geral_selection3.pivot_table(
        index=['Unidade'],
        values=['Valor Facturado', 'Kwh'],
        aggfunc='sum',
        fill_value=0
    )
                
    #criação de tabela dinamica por Tipo Cliente
    tabdinamica2 = geral_selection3.pivot_table(
        index=['Tipo Cliente'],
        values=['Valor Facturado', 'Kwh'],
        aggfunc='sum',
        fill_value=0
    )

        #criação de tabela dinamica por Produto
    tabdinamica3 = geral_selection3.pivot_table(
        index=['Produto'],
        values=['Valor Facturado', 'Kwh'],
        aggfunc='sum',
        fill_value=0
    )

    #criação de graficos por Unidade coemrcial
    #grafico UC Facturado
    fig_ucval = px.bar(
        tabdinamica,
        x=tabdinamica.index,
        y=['Valor Facturado'],
        orientation="v",
        title="<b>Grafico Valor Facturado Por Unidade</b>",
        color_discrete_sequence=["#5F9EA0"],
        template="plotly_white",
    )
    fig_ucval.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))

    )

    #grafico UC Kwh
    fig_ucquant = px.bar(
        tabdinamica,
        x=tabdinamica.index,
        y=['Kwh'],
        orientation="v",
        title="<b>Grafico Consumo Por Unidade</b>",
        color_discrete_sequence=["#B22222"],                
        template="plotly_white",
    )
    fig_ucquant.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )


    #criação de graficos por Tipo Cliente
    #grafico tipo cliente Facturado
    fig_tipval = px.bar(
        tabdinamica2,
        x=tabdinamica2.index,
        y=['Valor Facturado'],
        orientation="v",
        title="<b>Grafico Valor Facturado Tipo Cliente</b>",
        color_discrete_sequence=["#5F9EA0"],
        template="plotly_white",
    )
    fig_tipval.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))

    )

    #grafico tipo cliente Kwh
    fig_tipquant = px.bar(
        tabdinamica2,
        x=tabdinamica2.index,
        y=['Kwh'],
        orientation="v",
        title="<b>Grafico Consumo Tipo Cliente</b>",
        color_discrete_sequence=["#B22222"],                
        template="plotly_white",
    )
    fig_tipquant.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )

    #criação de graficos por Produto
    #grafico produto Facturado
    fig_proval = px.bar(
        tabdinamica3,
        x=tabdinamica3.index,
        y=['Valor Facturado'],
        orientation="v",
        title="<b>Grafico Valor Facturado Produto</b>",
        color_discrete_sequence=["#5F9EA0"],
        template="plotly_white",
    )
    fig_proval.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))

    )

    #grafico tipo cliente Kwh
    fig_proquant = px.bar(
        tabdinamica3,
        x=tabdinamica3.index,
        y=['Kwh'],
        orientation="v",
        title="<b>Grafico Consumo Produto</b>",
        color_discrete_sequence=["#B22222"],                
        template="plotly_white",
    )
    fig_proquant.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )
    
    #apresentar tabela dinamica na frame
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Facturação Por Unidade")
        st.dataframe(tabdinamica, column_config={"Unidade": st.column_config.TextColumn("Unidade", width="medium"),
                                                    "Kwh": st.column_config.NumberColumn("Kwh", width="small"),
                                                    "Valor Facturado": st.column_config.NumberColumn("Valor Facturado", width="medium")})
    
    with col2:
        st.header("Facturação Por Tipo Cliente")
        st.dataframe(tabdinamica2, column_config={"Tipo Cliente": st.column_config.TextColumn("Tipo Cliente", width="medium"),
                                                    "Kwh": st.column_config.NumberColumn("Kwh", width="small"),
                                                    "Valor Facturado": st.column_config.NumberColumn("Valor Facturado", width="medium")})
    
    with col3:
        st.header("Facturação Por Produto")
        st.dataframe(tabdinamica3, column_config={"Produto": st.column_config.TextColumn("Produto", width="medium"),
                                                        "Kwh": st.column_config.NumberColumn("Kwh", width="small"),
                                                    "Valor Facturado": st.column_config.NumberColumn("Valor Facturado", width="medium")})
    
        #graficos po unidade comercial
    st.header("Grafico Unidade Comercial")

    #apresentar os graficos em colunas
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_ucval, use_container_width=True)
    right_column.plotly_chart(fig_ucquant, use_container_width=True)

    st.markdown("---")
    #graficos por tipo cliente
    st.header("Grafico Tipo de Cliente")

    #apresentar os graficos em colunas
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_tipval, use_container_width=True)
    right_column.plotly_chart(fig_tipquant, use_container_width=True)

    st.markdown("---")
    #graficos por Produto
    st.header("Grafico Produto")

    #apresentar os graficos em colunas
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_proval, use_container_width=True)
    right_column.plotly_chart(fig_proquant, use_container_width=True)

    st.markdown("---")
    st.header("Quadro Facturação")
    #organizar
    geral_selection3 = geral_selection3[['Unidade', 'CIL', 'Cliente', 'Cliente Conta', 'Tipo Cliente','Produto', 'Tipo Factura', 'Nº Factura', 
                                            'Data Processamento', 'Data Facturação', 'Tarifa', 'Valor Facturado', 'CONCEITO', 'Kwh', 'Valor Cons (ECV)']]
                
    st.dataframe(geral_selection3, use_container_width=True, hide_index=True)

    #opção de download dos dados em excel
    @st.cache_data
    def convert_df(df):
        #conversão do dado
        return df.to_csv(sep=';', decimal=',', index=False).encode('utf-8-sig')
    
    csv = convert_df(geral_selection3)

    st.download_button(
        label="Download Facturação",
        data=csv,
        file_name='Script Facturação Tratado.csv',
        mime='text/csv'
    )
    #st.dataframe(facturas_tratadas, use_container_width=True, hide_index=True)