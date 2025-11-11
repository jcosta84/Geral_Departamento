import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from streamlit import connection
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, session
from streamlit_option_menu import option_menu
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import io
import json
from urllib.parse import quote_plus
import plotly.express as px
from datetime import datetime
from io import StringIO
import os


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
    query = "SELECT * FROM facturação"
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

#definir importação
def importar_contratos():
    query = "SELECT * FROM contratos"
    contratos2 = pd.read_sql(query, engine)
    #converter data
    contratos2['DT CONTRATO'] = pd.to_datetime(contratos2['DT CONTRATO'], format='%Y%m%d', errors='coerce').dt.strftime('%d-%m-%Y')
    contratos2['DT INICIO'] = pd.to_datetime(contratos2['DT INICIO'], format='%Y%m%d', errors='coerce').dt.strftime('%d-%m-%Y')
    contratos2['DT BAIXA'] = pd.to_datetime(contratos2['DT BAIXA'], format='%Y%m%d', errors='coerce').dt.strftime('%d-%m-%Y')
    
    return contratos2

def validar_login(username, password):
    session = SessionLocal()
    try:
        query = text("SELECT id, username FROM usuarios WHERE username = :username AND password = :password")
        result = session.execute(query, {"username": username, "password": password}).fetchone()
        return result  # None se inválido, ou tupla (id, username)
    finally:
        session.close()

def carregar_dados_usuario(id_usuario):
    session = SessionLocal()
    try:
        query = text("SELECT id, username, nivel FROM usuarios WHERE id = :id")
        result = session.execute(query, {"id": id_usuario}).fetchone()
        return result
    finally:
        session.close()

def atualizar_senha(id_usuario, nova_senha):
    session = SessionLocal()
    try:
        query = text("UPDATE usuarios SET password = :senha WHERE id = :id")
        session.execute(query, {"senha": nova_senha, "id": id_usuario})
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        st.error(f"Erro ao atualizar senha: {e}")
        return False
    finally:
        session.close()

# Pega o diretório onde este script (login.py) está salvo
base_dir = os.path.dirname(os.path.abspath(__file__))

# Monta o caminho absoluto do config.json
config_path = os.path.join(base_dir, "config", "config.json")

# Lê o arquivo config.json
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

#criar ligação a base de dados
server =   config["BD_SERVER"]
database = config["BD_NAME"]
user = config["BD_USER"]
password = config["BD_PASSWORD"]
driver = config["BD_DRIVER"]


#para situação de espaços no driver
driver_encoded = quote_plus(driver)

# String de conexão correta para SQLAlchemy + pyodbc
engine = create_engine(
    f"mssql+pyodbc://{user}:{password}@{server}/{database}?driver={driver_encoded}",
    fast_executemany=True
)

Session = sessionmaker(bind=engine)
session = Session()
SessionLocal = sessionmaker(bind=engine)

# Configuração da página
if "page_config_set" not in st.session_state:
    st.set_page_config(page_title="Login", layout="centered")
    st.session_state["page_config_set"] = True

# Criar um estado de sessão para login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Função para verificar login e obter nível de acesso
def check_login(username, password):
    query = f"""
        SELECT nivel FROM usuarios 
        WHERE username = '{username}' AND password = '{password}'
    """
    df = pd.read_sql(query, engine)
    if not df.empty:
        return df.iloc[0]["nivel"]
    return None

# Interface do login
if not st.session_state.logged_in:
    st.title("Tela de Login ao Sistema")

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Login"):
        nivel = check_login(username, password)
        if nivel:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.nivel = nivel
            st.session_state["page_config_set"] = False
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos!")

# Interface após login
if st.session_state.logged_in:
    st.set_page_config(page_title="Tratamento De Script's", layout="wide")
    
    # Sidebar com saudação
    st.sidebar.title(f"Bem-vindo, {st.session_state.username}!")
    st.sidebar.markdown(f"**Nível de acesso:** {st.session_state.nivel}")
    #'admin', 'gerente', 'factura', 'usuario', 'contagem', 'contrato'
    # Menu de opções conforme o nível de acesso
    if st.session_state.nivel == "admin":
        menu_opcoes = ["Home", "DAC - Lojas","Dep. Facturação", "Dep. Gestão Contagem", "Dep. Contratação","Administração"]
    elif st.session_state.nivel == "gerente":
        menu_opcoes = ["Home", "DAC - Lojas","Dep. Facturação", "Dep. Gestão Contagem", "Dep. Contratação", "Definição"]
    elif st.session_state.nivel == "factura":
        menu_opcoes = ["Home", "Dep. Facturação", "Definição"]
    elif st.session_state.nivel == "contagem":
        menu_opcoes = ["Home", "Dep. Gestão Contagem", "Definição"]
    elif st.session_state.nivel == "contrato":
        menu_opcoes = ["Home", "Dep. Contratação", "Definição"]
    elif st.session_state.nivel == "usuario":
        menu_opcoes = ["Home", "DAC - Lojas", "Definição"]
    else:
        menu_opcoes = ["Home"]

    # Menu lateral
    with st.sidebar:
        selected = option_menu(
            menu_title="Menu Principal",
            options=menu_opcoes,
            menu_icon="cast",
            default_index=0
        )

        # Páginas conforme menu
    if selected == "Home":
        st.title("Home")
        st.write("Bem-vindo à sua dashboard!")
        


    elif selected == "DAC - Lojas":
        st.title("DAC - Lojas")
        st.write("Área exclusiva para lojas.")
    
    elif selected == "Dep. Facturação":
        st.title("Dep. Facturação")
        #st.title("Facturação")
        menu = st.radio(
        "Seleção", ["Importação", "Dashboard", "Analise Maturidade"], horizontal=True
        )
        st.markdown("---")
        #campo de importação

        if menu == "Importação":
            st.title("Importação")

            #query importar facturação
            query = "SELECT * FROM facturação"
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
                                "facturação",
                                con=conn,
                                if_exists="append",
                                index=False,
                                chunksize=10000  # insere em blocos de 10 mil linhas
                            )
                        st.success("Dados inseridos com sucesso!")
                    except Exception as e:
                        st.error(f"Erro ao inserir dados: {e}")
                
        
        #campo de Dashboard
        if menu == "Dashboard":
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
    
        #campo de Analise Matiridade
        if menu == "Analise Maturidade":
            st.title("Analise Maturidade")
            facturas_maturidade = tratar_factura()
            contratos_geral = importar_contratos()
                        
            col1, col2, col3 = st.columns(3)

            #col1
            with col1:
                #filtrar região
                reg = st.multiselect(
                    "Definir Região: ",
                    options=facturas_maturidade['Regiao'].unique(),
                )

                geral_mat = facturas_maturidade.query(
                    "`Regiao` == @reg"
                )
            
            #col2
            with col2:
                #filtar ano
                an = st.multiselect(
                    "Definir Ano: ",
                    options=geral_mat['Ano'].unique(),

                )
                geral_mat2 = geral_mat.query(
                    "`Ano` == @an"
                )
            
            tab_di = pd.pivot_table(
                geral_mat2,
                index=['CIL', 'Cliente Conta'],
                columns='Mês',
                values='Kwh',
                aggfunc='sum',
                fill_value=0
            )
            #coluna de soma total na tabela dinamica
            tab_di['Media Consumo Geral'] = tab_di.sum(axis=1)
            #função se tendo em consideração a coluna de soma total
            tab_di["Maturidade de consumo"] = tab_di["Media Consumo Geral"].apply(classificar_maturidade)
            tab_di = tab_di.reset_index()
            
            #concatenação cil e conta
            tab_di['CIL Conta'] = tab_di['CIL'] + ' - ' + tab_di['Cliente Conta']
            contratos_geral['CIL Conta'] = contratos_geral['CIL'] + ' - ' + contratos_geral['CLI CONTA']
            contratos_geral = contratos_geral[["CIL Conta", "Regiao","Unidade", "NIP", "PORTA", "CGV", 
                                               "Tipo_Cliente", "NOME", "MORADA", "LOCALIDADE", "Produto", "COD TARIFA", "SEQ CONTR", 
                                               "Estado Contrato", "DT CONTRATO", "DT INICIO", "DT BAIXA"]]
            
            contdi = pd.merge(tab_di, contratos_geral, on='CIL Conta', how='left')
            contdi.set_index('CIL Conta', inplace=True)

            #definir botão de download numa coluna
            col1, col2 = st.columns(2)
            with col1:
                #opção de download dos dados em excel
                @st.cache_data
                def convert_df(df):
                    #conversão do dado
                    return df.to_csv(sep=';', decimal=',', index=False).encode('utf-8-sig')
                
                csv = convert_df(contdi)

                st.download_button(
                    label="Download Facturação",
                    data=csv,
                    file_name='Script Facturação Tratado.csv',
                    mime='text/csv'
                )

            #tabela dinamica numa coluna
            left_column, midle_column = st.columns(2)
            with col1:

                #criação de tabela dinamica para maturidade
                #quantidade de locais
                tabdicont = pd.pivot_table(
                    contdi,
                    index=['Maturidade de consumo'],
                    values='CIL',
                    aggfunc='count',
                    fill_value=0
                )

                #valor total consumido
                tabdicont2 = pd.pivot_table(
                    contdi,
                    index=['Maturidade de consumo'],
                    values='Media Consumo Geral',
                    aggfunc='sum',
                    fill_value=0
                )
                #merge duas tabelas de forma apresentar as informações de quantidade de consumo
                tb_ge = pd.merge(tabdicont, tabdicont2, on='Maturidade de consumo', how='left')
                #apresentar as duas tabelas
                st.dataframe(tb_ge)
            
            with col2:
                #definir filro para as maturidades
                #filtrar região
                matu = st.multiselect(
                    "Definir Maturidade: ",
                    options=contdi['Maturidade de consumo'].unique(),
                )

                geral_mat = contdi.query(
                    "`Maturidade de consumo` == @matu"
                )
                geral_mat.set_index('CIL', inplace=True)
                        
            #tabela filtrada            
            st.dataframe(geral_mat)

            #opção de download dos dados em excel
            @st.cache_data
            def convert_df(df):
                #conversão do dado
                return df.to_csv(sep=';', decimal=',', index=False).encode('utf-8-sig')
            
            csv = convert_df(geral_mat)

            st.download_button(
                label="Download Analise Maturidade",
                data=csv,
                file_name='Script Facturação Por Maturidade.csv',
                mime='text/csv'
            )
         


    elif selected == "Dep. Gestão Contagem":
        st.title("Dep. Gestão Contagens")
        
        menu = st.radio(
        "Seleção", ["Importação", "Tratamento Itinerarios", "Analise Leituras"], horizontal=True
        )

        st.markdown("---")

        #campo de importação
        if menu == "Importação":
            
            #consultar itinerarios
            query = "SELECT * FROM itinerarios"
            itinerarios2 = pd.read_sql(query, engine)
            left_column, middle_column,right_column = st.columns(3)
            with left_column:
                #definir estrutura de data
                min_date = datetime(2020, 1, 1)
                max_date = datetime(2070, 12, 31)
                default_start = datetime(2020, 1, 1)
                default_end = datetime(2070, 12, 31)           
                #configurar data a se usada
                dados = st.date_input("Definir Data: ", 
                                    value=(default_start),
                                    min_value=min_date,
                                    max_value=max_date)
                data = pd.DataFrame({"Datas": [dados]})

            st.markdown("---")

            #carregar itinerarios
            upload_file = st.file_uploader("Importar Itinerarios", type="xlsx")
            if upload_file:
                st.markdown("---")
                itinerario = pd.read_excel(upload_file, engine="openpyxl")
                itdata = pd.concat([data, itinerario], axis=1)
                itdata["Datas"] = itdata["Datas"].ffill()
                unidata = pd.merge(itdata, uc, on='Roteiro', how='left')
                unidata = unidata.loc[:,['Datas', 'Unidade','Nr. Roteiro', 'Roteiro', 'Ciclo', 'Itinerário', 'Zona', 'Rua', 'Cliente', 'Ponto de Medida', 'CIL',
                                                'Número', 'Marca', 'Função', 'Anterior', 'Atual', 'Anomalia']]
            
            #função de carregar it na base de dados    
            if st.button("Guardar Itinerarios"):
                try:
                    unidata.to_sql("itinerarios", con=engine, if_exists="append", index=False)
                    st.success("Dados inseridos com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao inserir dados: {e}")
            
            #lista de contadores de leitura remota
            query = "SELECT * FROM contador"
            contador = pd.read_sql(query, engine)
            upload_file = st.file_uploader("Importar Contadores", type="xlsx")
            if upload_file:
                st.markdown("---")
                contadores = pd.read_excel(upload_file, engine="openpyxl")
            #carregar na base de dados
            if st.button("Guardar Contadores"):
                try:
                    contadores.to_sql("contador", con=engine, if_exists='replace', index=False)
                    st.success("Informação carregada com sucesso!")
                except Exception as e:
                    st.error(f'Ocorreu um erro na importação')
            
            #periodo
            query = "SELECT * FROM periodo"
            periodo = pd.read_sql(query, engine)
            upload_file = st.file_uploader("Importar Periodo", type="xlsx")
            if upload_file:
                st.markdown("---")
                periodos = pd.read_excel(upload_file, engine="openpyxl")
            #carregar na base de dados
            if st.button("Carregar Periodo"):
                try:
                    periodos.to_sql("periodo", con=engine, if_exists='replace', index=False)
                    st.success("Informação carregada com sucesso!")
                except Exception as e:
                    st.error(f'Ocorreu um erro na importação')
            
            #leitura remota
            query = "SELECT * FROM imtt"
            remota = pd.read_sql(query, engine)
            upload_file = st.file_uploader("Importar Leituras", type="xlsx")
            if upload_file:
                st.markdown("---")
                leituras = pd.read_excel(upload_file, engine="openpyxl")
            #carregar na base de dados
            if st.button("Carregar Leitura"):
                try:
                    leituras.to_sql('imtt', con=engine, if_exists='append', index=False)
                    st.success("Informação carregada com sucesso!")
                except Exception as e:
                    st.error(f'Ocorreu um erro na importação')

        #menu para tratar os dados de itinerarios e lançamento de leituras remotas       
        if menu == "Tratamento Itinerarios":
            #st.title("Tratamento Itinerarios")

            #importar itinerarios
            query = "SELECT * FROM itinerarios"
            it = pd.read_sql(query, engine)
                        
            # alterar codigo de função para descrição do codigo
            itfun = pd.merge(it, funcao, on='Função', how='left')
            itfun['Datas'] = pd.to_datetime(itfun['Datas'])
            itfun['Ano'] = itfun['Datas'].dt.year
            itfun['Me'] = itfun['Datas'].dt.month
            itfun['Me'] = itfun['Me'].astype(str)
            itfun['Ano'] = itfun['Ano'].astype(str)
            itfun['Datas'] = itfun['Datas'].dt.date
            itfun2 = pd.merge(itfun, refmes, on='Me', how='left')

            #alterar ordem de apresentação
            itfun2 = itfun2.loc[:,['Ano', 'Mês', 'Descrição','Unidade','Nr. Roteiro', 'Roteiro', 'Ciclo', 'Itinerário', 'Zona', 'Rua', 'Cliente', 'Ponto de Medida', 'CIL',
                                                'Número', 'Marca', 'Função', 'Anterior', 'Atual', 'Anomalia']]

            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader("Definir Periodo de Leitura")
                #filtrar Ano
                ano = st.multiselect(
                    "Definir Ano: ",
                    options=itfun2['Ano'].unique(),
                )

                geralit = itfun2.query(
                    "`Ano` == @ano"
                )

                #filtrar Mês
                mes = st.multiselect(
                    "Definir Mês: ",
                    options=geralit['Mês'].unique(),
                )

                geralit2 = geralit.query(
                    "`Mês` == @mes"
                )

            
            #leitura remota
            query = "SELECT * FROM imtt"
            leitura = pd.read_sql(query, engine)
            leitura['Data Time'] = pd.to_datetime(leitura['Data Time'])
            leitura['Ano'] = leitura['Data Time'].dt.year
            leitura['Me'] = leitura['Data Time'].dt.month
            leitura['Me'] = leitura['Me'].astype(str)
            leitura['Ano'] = leitura['Ano'].astype(str)
            leitura['Data Time'] = leitura['Data Time'].dt.date
            leitura2 = pd.merge(leitura, refmes, on='Me', how='left')

            #alterar ordem de apresentação
            leitura2 = leitura2.loc[:,['Ano', 'Mês', 'Descrição', 'Customer Name', 'Metering Points No.', 'Meter No.', 'Power Utility', 'Activeenergy(+)total(kWh)']]
            #junção de contador + função + cil
            leitura2['CIL/Contador/Função/Ano/Mês'] = leitura2['Metering Points No.'].astype(str) + '-' + leitura2['Meter No.'].astype(str) + '-' + leitura2['Descrição'] + '-' + leitura2['Ano'] + '-' + leitura2['Mês']
            #alterar ordem de apresentação
            leitura2 = leitura2.loc[:,['CIL/Contador/Função/Ano/Mês', 'Activeenergy(+)total(kWh)']]
 
            #junção de contador + função + cil
            geralit2['CIL/Contador/Função/Ano/Mês'] = geralit2['CIL'].astype(str) + '-' + geralit2['Número'].astype(str) + '-' + geralit2['Descrição'] + '-' + geralit2['Ano'] + '-' + geralit2['Mês']

            #cruzar leitura remota e itinerario
            leitre = pd.merge(geralit2, leitura2, on='CIL/Contador/Função/Ano/Mês', how='left')

            #alterar ordem
            leitre = leitre.loc[:,['Ano', 'Mês', 'Descrição','Unidade','Nr. Roteiro', 'Roteiro', 'Ciclo', 'Itinerário', 'Zona', 'Rua', 'Cliente', 'Ponto de Medida', 'CIL',
                                                'Número', 'Marca', 'Função', 'Anterior', 'Activeenergy(+)total(kWh)', 'Anomalia']]
            
            #reomear colunas
            leitre = leitre.rename(columns={'Activeenergy(+)total(kWh)': 'Atual',
                                            'Zona':'Zona ', 
                                            'Rua':' Rua ',
                                            'Cliente':' Cliente'})
            
            with col1:
                #carregar na base de dados
                if st.button("Carregar Leitura"):
                    try:
                        leitre.to_sql('base_remota', con=engine, if_exists='replace', index=False)
                        st.success("Informação carregada com sucesso!")
                    except Exception as e:
                        st.error(f'Ocorreu um erro na importação')

                                                
            #definir coluna para filtragem
            with col2:
                st.subheader("Definir Unidade E Roteiro")
                #filtrar Roteiro e itinerario
                unidade = st.multiselect(
                    "Definir Unidade: ",
                    options=leitre['Unidade'].unique(),

                )
                un = leitre.query(
                    "`Unidade` == @unidade"
                )

                roteiro = st.multiselect(
                    "Definir Roteiro: ",
                    options=un['Roteiro'].unique(),
                    
                )
                rot = un.query(
                    "`Roteiro` == @roteiro"
                )

                iti = st.multiselect(
                    "Definir Itinerario: ",
                    options=rot['Itinerário'].unique(),

                )
                gerit = rot.query(
                    "`Itinerário` == @iti"
                )

                                

            st.markdown("---")

            #alterar ordem
            gerit = gerit.loc[:,['Nr. Roteiro', 'Roteiro', 'Ciclo', 'Itinerário', 'Zona ', ' Rua ', ' Cliente', 'Ponto de Medida', 'CIL',
                                                'Número', 'Marca', 'Função', 'Anterior', 'Atual', 'Anomalia']]
            
            gerit.set_index('Nr. Roteiro', inplace=True)
            st.dataframe(gerit, use_container_width=True)

            #opção de download dos dados em excel
            @st.cache_data
            def convert_df(df):
                #conversão do dado
                return df.to_csv(sep=';', decimal=',', index=False).encode('utf-8-sig')
            
            csv = convert_df(gerit)

            st.download_button(
                label="Download Itinerarios",
                data=csv,
                file_name='Itinerario.csv',
                mime='text/csv'
            )


        if menu == "Analise Leituras":
            st.title("Analise")
            # === Leitura das tabelas do banco ===
            try:
                base = pd.read_sql("SELECT * FROM base_remota", engine)
                contador2 = pd.read_sql("SELECT * FROM contador", engine)
                periodo2 = pd.read_sql("SELECT * FROM periodo", engine)
            except Exception as e:
                st.error(f"Erro ao carregar dados do banco: {e}")
                st.stop()

            # --- Verificar se as tabelas têm dados ---
            if base.empty or contador2.empty or periodo2.empty:
                st.warning("Uma ou mais tabelas estão vazias. Verifique o banco de dados.")
                st.stop()

            # === Definir tipo de contador remoto ===
            if 'Nº Contador' in contador2.columns:
                contador2.loc[contador2['Nº Contador'] >= 0, "Tipo Contador"] = "Leitura Remota"
            else:
                st.error("A coluna 'Nº Contador' não foi encontrada em 'contador'.")
                st.write("Colunas disponíveis:", contador2.columns.tolist())
                st.stop()

            # === Criar coluna de diferença de leitura ===
            if {'Atual', 'Anterior'}.issubset(base.columns):
                base['Diferença'] = base['Atual'] - base['Anterior']
                base.loc[base['Diferença'] < 0, "Analise Leitura"] = "Volta de Contador"
                base.loc[base['Diferença'] == 0, "Analise Leitura"] = "Contador Parado"
                base.loc[base['Diferença'] > 0, "Analise Leitura"] = "Local Com Consumo"
            else:
                st.error("As colunas 'Atual' e 'Anterior' não existem em 'base_remota'.")
                st.write("Colunas disponíveis:", base.columns.tolist())
                st.stop()

            # === Junção contador + base ===
            if {'CIL', 'Número'}.issubset(base.columns):
                base['CIL/Contador'] = base['CIL'].astype(str) + '-' + base['Número'].astype(str)
            else:
                st.error("A tabela 'base_remota' não contém colunas 'CIL' e 'Número'.")
                st.stop()

            if {'CIL', 'Nº Contador'}.issubset(contador2.columns):
                contador2['CIL/Contador'] = contador2['CIL'].astype(str) + '-' + contador2['Nº Contador'].astype(str)
            else:
                st.error("A tabela 'contador' não contém colunas 'CIL' e 'Nº Contador'.")
                st.stop()

            contador2 = contador2.loc[:, ['CIL/Contador', 'Tipo Contador']]
            contador_geral = pd.merge(base, contador2, on='CIL/Contador', how='left')

            # === Ajustar ordem e juntar com período ===
            colunas_base = [
                'Unidade', 'Analise Leitura', 'Tipo Contador', 'Diferença',
                'Nr. Roteiro', 'Roteiro', 'Ciclo', 'Itinerário', 'Zona ', ' Rua ',
                ' Cliente', 'Ponto de Medida', 'CIL', 'Número', 'Marca', 'Função',
                'Anterior', 'Atual', 'Anomalia'
            ]
            contador_geral = contador_geral[[c for c in colunas_base if c in contador_geral.columns]]

            cont_geral = pd.merge(contador_geral, periodo2, on='CIL', how='left')
            colunas_final = [
                'Tipo Contador', 'Diferença', 'periodo', 'Analise Leitura', 'Unidade',
                'Nr. Roteiro', 'Roteiro', 'Ciclo', 'Itinerário', 'Zona ', ' Rua ', ' Cliente',
                'Ponto de Medida', 'CIL', 'Número', 'Marca', 'Função', 'Anterior', 'Atual', 'Anomalia'
            ]
            cont_geral = cont_geral[[c for c in colunas_final if c in cont_geral.columns]]

            # === Filtros laterais ===
            st.sidebar.header("Definir Tipo de Leitura:")
            tp_leit = st.sidebar.multiselect(
                "Definir Contador",
                options=cont_geral['Tipo Contador'].dropna().unique()
            )
            geral_selection = cont_geral.query("`Tipo Contador` == @tp_leit") if tp_leit else cont_geral

            st.sidebar.header("Definir Período:")
            pe_leit = st.sidebar.multiselect(
                "Definir Formato de Leitura",
                options=cont_geral['periodo'].dropna().unique()
            )
            geral_selection2 = geral_selection.query("`periodo` == @pe_leit") if pe_leit else geral_selection

            st.sidebar.header("Definir Leitura:")
            dif_leit = st.sidebar.multiselect(
                "Definir Formato de Leitura",
                options=cont_geral['Analise Leitura'].dropna().unique()
            )
            geral_selection3 = geral_selection2.query("`Analise Leitura` == @dif_leit") if dif_leit else geral_selection2

            # === Organizar resultado final ===
            colunas_saida = [
                'Unidade', 'Nr. Roteiro', 'Roteiro', 'Ciclo', 'Itinerário', 'Zona ', ' Rua ', ' Cliente',
                'Ponto de Medida', 'CIL', 'Número', 'Marca', 'Função', 'Anterior', 'Atual', 'Anomalia'
            ]
            geral_selection3 = geral_selection3[[c for c in colunas_saida if c in geral_selection3.columns]]

            if not geral_selection3.empty:
                geral_selection3.set_index('Unidade', inplace=True)
                st.dataframe(geral_selection3)
            else:
                st.info("Nenhum registro encontrado com os filtros selecionados.")

            # === Download ===
            @st.cache_data
            def convert_df(df):
                return df.to_csv(sep=';', decimal=',', index=False).encode('utf-8-sig')

            if not geral_selection3.empty:
                csv = convert_df(geral_selection3)
                st.download_button(
                    label="📥 Download Análise",
                    data=csv,
                    file_name='Analise_de_Leitura.csv',
                    mime='text/csv'
                )
 

    elif selected == "Dep. Contratação":
        st.title("Dep. Contratação")
        st.write("Área para Contratação.")

        #query importar contratos
        query = "SELECT * FROM contratos"
        arquivo = st.file_uploader("Importar Contratos", type=["txt"])
        if arquivo is not None:   # <- mesma indentação que a linha acima
            df = pd.read_csv(
                arquivo,
                sep="\t",
                header=None,
                names=colunas2,
                dtype=str,
                encoding="utf-8-sig",
                engine="python",
                on_bad_lines="warn"
    )
            df['UC'] = df['UC'].astype(int)
            st.success("Arquivo carregado com sucesso!")
            contest = pd.merge(df, est_contr, on='EST CONTR', how='left')
            contrtp = pd.merge(contest, tip_client, on='TP_CLI', how='left')
            contruc = pd.merge(contrtp, unidade, on='UC', how='left')
            contreg = pd.merge(contruc, regiao, on='Unidade', how='left')
            contrpro = pd.merge(contreg, produto, on='Prod', how='left')
            contrpro = contrpro[["EMP ID", "Regiao","Unidade", "USR ID", "NIP", "PORTA", "CIL", "SIS ABAST", "CGV",
                                        "CLI CONTA", "Tipo_Cliente", "CAE ID", "TP USO", "NOME", "MORADA", "LOCALIDADE",
                                        "COD LOCAL", "Produto", "COD TARIFA", "SEQ CONTR", "Estado Contrato",
                                        "DT CONTRATO", "DT INICIO", "DT BAIXA"]]
            
            #função de carregar contratos na base de dados    
            if st.button("Guardar Facturação"):
                try:
                    contrpro.to_sql("contratos", con=engine, if_exists="replace", index=False)
                    st.success("Dados inseridos com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao inserir dados: {e}")


    elif selected == "Administração":
        st.title("Painel Administrativo")
        
        st.subheader("📋 Lista de Usuários")

        # Consulta todos os usuários
        df_usuarios = pd.read_sql("SELECT id, username, nivel FROM usuarios", engine)
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


    elif selected == "Definição":
        st.title("Configuração de Conta")

        

        
               


    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
