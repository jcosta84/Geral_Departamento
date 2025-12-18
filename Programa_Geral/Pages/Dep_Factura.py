from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from database.db import engine  # Usar engine, não SessionLocal
import re

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

# --- Configuração da página ---
st.set_page_config(page_title="Facturação", layout="wide")

