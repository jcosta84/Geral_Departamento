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

    st.set_page_config(
        page_title="Gestão de Contagens",
        layout="wide"
    )

        
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

    

    # --- Configuração da página ---
    st.set_page_config(page_title="Gestão de Contagens", layout="wide")

    # --- Menu lateral ---
    with st.sidebar:
        selected = option_menu(
            menu_title="Sub-Menu",
            options=["Importação", "Tratamento Itinerarios", "Analise Leituras"],
            menu_icon="cast",
            default_index=0
        )

    # --- Importação ---
    if selected == "Importação":
        st.header("Importação de Dados de Contagens")

        # Consultar dados existentes
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
        st.markdown("---")

        #lista de contadores de leitura remota
        query = "SELECT * FROM contador"
        contador = pd.read_sql(query, engine)
        upload_file = st.file_uploader("Importar Contadores", type="xlsx")
        if upload_file:
            contadores = pd.read_excel(upload_file, engine="openpyxl")
        #carregar na base de dados
        if st.button("Guardar Contadores"):
            try:
                contadores.to_sql("contador", con=engine, if_exists='replace', index=False)
                st.success("Informação carregada com sucesso!")
            except Exception as e:
                st.error(f'Ocorreu um erro na importação')
        st.markdown("---")
        
        #periodo
        query = "SELECT * FROM periodo"
        periodo = pd.read_sql(query, engine)
        upload_file = st.file_uploader("Importar Periodo", type="xlsx")
        if upload_file:

            periodos = pd.read_excel(upload_file, engine="openpyxl")
        #carregar na base de dados
        if st.button("Carregar Periodo"):
            try:
                periodos.to_sql("periodo", con=engine, if_exists='replace', index=False)
                st.success("Informação carregada com sucesso!")
            except Exception as e:
                st.error(f'Ocorreu um erro na importação')
        st.markdown("---")
        
        #leitura remota
        query = "SELECT * FROM imtt"
        remota = pd.read_sql(query, engine)
        upload_file = st.file_uploader("Importar Leituras", type="xlsx")
        if upload_file:
            
            leituras = pd.read_excel(upload_file, engine="openpyxl")
        #carregar na base de dados
        if st.button("Carregar Leitura"):
            try:
                leituras.to_sql('imtt', con=engine, if_exists='append', index=False)
                st.success("Informação carregada com sucesso!")
            except Exception as e:
                st.error(f'Ocorreu um erro na importação')
        st.markdown("---")

    # --- Tratamento Itinerários ---
    elif selected == "Tratamento Itinerarios":
        st.header("Tratamento de Itinerarios de Contagens")

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
        leitura2 = leitura2.loc[:,['Ano', 'Mês', 'Descrição', 'Customer Name', 'Metering Points No.', 'Meter No.', 'Power Utility', 'Total_kwh']]
        #junção de contador + função + cil
        leitura2['CIL/Contador/Função/Ano/Mês'] = leitura2['Metering Points No.'].astype(str) + '-' + leitura2['Meter No.'].astype(str) + '-' + leitura2['Descrição'] + '-' + leitura2['Ano'] + '-' + leitura2['Mês']
        #alterar ordem de apresentação
        leitura2 = leitura2.loc[:,['CIL/Contador/Função/Ano/Mês', 'Total_kwh']]

        #junção de contador + função + cil
        geralit2['CIL/Contador/Função/Ano/Mês'] = geralit2['CIL'].astype(str) + '-' + geralit2['Número'].astype(str) + '-' + geralit2['Descrição'] + '-' + geralit2['Ano'] + '-' + geralit2['Mês']

        #cruzar leitura remota e itinerario
        leitre = pd.merge(geralit2, leitura2, on='CIL/Contador/Função/Ano/Mês', how='left')

        #alterar ordem
        leitre = leitre.loc[:,['Ano', 'Mês', 'Descrição','Unidade','Nr. Roteiro', 'Roteiro', 'Ciclo', 'Itinerário', 'Zona', 'Rua', 'Cliente', 'Ponto de Medida', 'CIL',
                                            'Número', 'Marca', 'Função', 'Anterior', 'Total_kwh', 'Anomalia']]
        
            
        with col1:
            #carregar na base de dados
            if st.button("Carregar Leitura"):
                try:
                    leitre.to_sql('base_remota', con=engine, if_exists='append', index=False)
                    st.success("Informação carregada com sucesso!")
                except Exception as e:
                    st.error(f"Erro: {str(e)}")

                                            
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

        #reomear colunas
        gerit = gerit.rename(columns={'Total_kwh': 'Atual',
                                        'Zona':'Zona ', 
                                        'Rua':' Rua ',
                                        'Cliente':' Cliente'})
        #alterar ordem
        gerit = gerit.loc[:,['Nr. Roteiro', 'Roteiro', 'Ciclo', 'Itinerário', 'Zona ', ' Rua ', ' Cliente', 'Ponto de Medida', 'CIL',
                                            'Número', 'Marca', 'Função', 'Anterior', 'Atual', 'Anomalia']]
        
        gerit.set_index('Nr. Roteiro', inplace=True)
        st.dataframe(gerit, use_container_width=True)

        # --- FUNÇÃO PARA LIMPAR O NOME ---
        def limpar_texto(texto):
            return re.sub(r'[\\/*?:"<>|]', "_", str(texto))


        # Verificar se o DataFrame tem linhas
        if gerit.empty:
            st.error("⚠️ Nenhum dado encontrado no roteiro. Verifique o ficheiro carregado.")
        else:
            primeira_linha = gerit.iloc[0]

            nome_roteiro = limpar_texto(primeira_linha['Roteiro'])
            nome_itinerario = limpar_texto(primeira_linha['Itinerário'])

            nome_arquivo = f"Roteiro_{nome_roteiro}_Itinerario_{nome_itinerario}.csv"

            #opção de download dos dados em excel
            @st.cache_data
            def convert_df(df):
                #conversão do dado
                return df.to_csv(sep=';', decimal=',', index=False).encode('utf-8-sig')
            
            csv = convert_df(gerit)

            st.download_button(
                label="Download Itinerarios",
                data=csv,
                file_name=nome_arquivo,
                mime='text/csv'
            )

    # --- Análise de Leituras ---
    elif selected == "Analise Leituras":
        st.header("Análise de Leituras de Contagens")

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

if __name__ == "__main__":
    app()