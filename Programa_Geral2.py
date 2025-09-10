import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
import json, os
from urllib.parse import quote_plus
import plotly.express as px
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import plotly.express as px
import plotly.graph_objects as go
from matplotlib.figure import Figure
from io import BytesIO
import csv

# -------------------- CONFIG DB -------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(BASE_DIR, 'config', 'config.json')

with open(config_path, 'r') as f:
    config = json.load(f)

server = config["BD_SERVER"]
database = config["BD_NAME"]
user = config["BD_USER"]
password = config["BD_PASSWORD"]
driver = config["BD_DRIVER"]

driver_encoded = quote_plus(driver)

engine = create_engine(
    f"mssql+pyodbc://{user}:{password}@{server}/{database}?driver={driver_encoded}",
    fast_executemany=True
)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# -------------------- Tela de login -------------------
class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x300")
        self.title("Login Sistema")
        self.user_logged = None
        self.nivel_logged = None
        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(self, text="Usuário").pack(pady=10)
        self.username = ctk.CTkEntry(self)
        self.username.pack()

        ctk.CTkLabel(self, text="Senha").pack(pady=10)
        self.password = ctk.CTkEntry(self, show="*")
        self.password.pack()

        self.login_btn = ctk.CTkButton(self, text="Entrar", command=self.login)
        self.login_btn.pack(pady=20)

    def login(self):
        user = self.username.get()
        pwd = self.password.get()
        query = text("SELECT nivel FROM usuarios WHERE username = :user AND password = :pwd")
        with engine.connect() as conn:
            result = conn.execute(query, {"user": user, "pwd": pwd}).fetchone()
        if result:
            messagebox.showinfo("Sucesso", f"Bem-vindo {user}!\nAcesso: {result.nivel}")
            self.user_logged = user
            self.nivel_logged = result.nivel
            #self.quit()
            self.destroy()  # <- fecha a janela de login corretamente
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")

# -------------------- Aplicativo principal -------------------
class MainApp(ctk.CTk):
    def __init__(self, user, nivel):
        super().__init__()
        self.geometry("1000x700")
        self.title(f"Menu Principal - {user}")
        self.user = user
        self.nivel = nivel
        self.frames = {}
        
        # Carregar tabelas auxiliares para merges
        self.carregar_tabelas_auxiliares()
        
        self.build_ui()

    def carregar_tabelas_auxiliares(self):
        # Dados de exemplo, substitua pelos seus dados reais ou carregue do banco/arquivo
        dados_unidade = [
            [10201000, "Praia"],
            [10202000, "São Domingos"],
            [10203000, "Santa Catarina"],
            [10204000, "Tarrafal"],
            [10205000, "Calheta"],
            [10206000, "Santa Cruz"],
            [10701000, "Mosteiros"],
            [10702000, "São Filipe"],
            [10801000, "Maio"],
            [10901000, "Brava"],
            [10101000, "Mindelo"],
            [10301000, "SAL"],
            [10401000, "BOAVISTA"],
            [10501000, "VILA DA RIBEIRA BRAVA"],
            [10601000, "R.GRANDE - N.S.Rosário"],
            [10602000, "PORTO NOVO - S.João Baptista"],
            [10603000, "PAUL - S.António das Pombas"],
            [10502000, "Tarrafal S.Nicolau"],
            [10000000, "Electra SUL"]
        ]
        self.unidade = pd.DataFrame(dados_unidade, columns=['UC', 'Unidade']).set_index('UC')

        dados_produto = [
            ['EB', 'Baixa Tensão'],
            ['EE', 'Baixa Tensão Especial'],
            ['EM', 'Media Tensão'],
            ['AG', 'Agua']
        ]
        self.produto = pd.DataFrame(dados_produto, columns=['Prod', 'Produto']).set_index('Prod')

        dados_tp_fact = [
            ['11', 'Em Ciclo Leitura'],
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
        self.tp_fact = pd.DataFrame(dados_tp_fact, columns=['TP_FACT', 'Tipo_Factura']).set_index('TP_FACT')

        dados_tip_client = [
            ['A', 'Cliente Residencial'],
            ['B', 'Cliente Comercial'],
            ['C', 'Cliente Industrial']
        ]
        self.tip_client = pd.DataFrame(dados_tip_client, columns=['TP_CLI', 'Tipo_Cliente']).set_index('TP_CLI')

        dados_tarifa = [
            ['01', 'Tarifa Normal'],
            ['02', 'Tarifa Reduzida']
        ]
        self.tarifa = pd.DataFrame(dados_tarifa, columns=['COD_TARIFA', 'Tarifa']).set_index('COD_TARIFA')

        dados_regiao = [
            ['Praia', 'Região Sul'],
            ['São Domingos', 'Região Norte'],
            ['Santa Catarina', 'Região Centro']
        ]
        self.regiao = pd.DataFrame(dados_regiao, columns=['Unidade', 'Regiao']).set_index('Unidade')

    def build_ui(self):
        self.menu_frame = ctk.CTkFrame(self, width=200)
        self.menu_frame.pack(side="left", fill="y")

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(side="right", expand=True, fill="both")

        self.menu_options = {
            "Home": HomeFrame,
            "DAC - Lojas": DACFrame,
            "Dep. Facturação": FacturaFrame,
            "Dep. Gestão Contagem": ContagemFrame,
            "Dep. Contratação": ContratoFrame,
            "Administração": AdminFrame,
            "Definição": DefinicaoFrame
        }

        for name in self.menu_options:
            ctk.CTkButton(self.menu_frame, text=name, command=lambda n=name: self.show_frame(n)).pack(pady=5, fill='x')

        self.show_frame("Home")

    def show_frame(self, name):
        for frame in self.content_frame.winfo_children():
            frame.destroy()
        frame_class = self.menu_options.get(name)
        if frame_class:
            if frame_class == FacturaFrame:
                frame = frame_class(
                    self.content_frame,
                    engine,
                    self.unidade,
                    self.produto,
                    self.tp_fact,
                    self.tip_client,
                    self.tarifa,
                    self.regiao
                )
            else:
                frame = frame_class(self.content_frame)
            frame.pack(expand=True, fill="both")

# -------------------- Home FRAMES -------------------
class HomeFrame(ctk.CTkFrame):
    def __init__(self, master): 
        super().__init__(master)
        ctk.CTkLabel(self, text="Bem-vindo à Home").pack(pady=20)

class DACFrame(ctk.CTkFrame):
    def __init__(self, master): 
        super().__init__(master)
        ctk.CTkLabel(self, text="DAC - Lojas").pack(pady=20)

class FacturaFrame(ctk.CTkFrame):
    def __init__(self, master, engine, unidade, produto, tp_fact, tip_client, tarifa, regiao):
        super().__init__(master)
        self.engine = engine
        self.unidade = unidade
        self.produto = produto
        self.tp_fact = tp_fact
        self.tip_client = tip_client
        self.tarifa = tarifa
        self.regiao = regiao

        ctk.CTkLabel(self, text="Departamento de Facturação", font=("Arial", 20)).pack(pady=10)

        self.menu_opcao = ctk.StringVar(value="Importação")

        self.radio_frame = ctk.CTkFrame(self)
        self.radio_frame.pack(pady=10)

        for opcao in ["Importação", "Dashboard", "Analise Maturidade"]:
            ctk.CTkRadioButton(
                self.radio_frame, text=opcao, variable=self.menu_opcao, value=opcao,
                command=self.mostrar_secao
            ).pack(side="left", padx=10)

        self.secao_frame = ctk.CTkFrame(self)
        self.secao_frame.pack(fill="both", expand=True)

        self.df = None  # Dados brutos importados
        self.df_processado = None  # Dados após merges e processamento
        self.mostrar_secao()

    def mostrar_secao(self):
        for widget in self.secao_frame.winfo_children():
            widget.destroy()

        selecao = self.menu_opcao.get()

        if selecao == "Importação":
            self.import_button = ctk.CTkButton(self.secao_frame, text="Importar TXT", command=self.importar_facturacao)
            self.import_button.pack(pady=10)

            self.save_button = ctk.CTkButton(self.secao_frame, text="Salvar no Banco", command=self.salvar_no_banco, state="disabled")
            self.save_button.pack(pady=10)

        elif selecao == "Dashboard":
            if self.df_processado is None:
                ctk.CTkLabel(self.secao_frame, text="Importe primeiro os dados para visualizar o dashboard.").pack(pady=20)
                return

            dados = self.df_processado.copy()

            # Adiciona colunas Ano e Mês
            dados["Ano"] = pd.to_datetime(dados["DT_FACT"]).dt.year
            dados["Mês"] = pd.to_datetime(dados["DT_FACT"]).dt.month

            # Filtros
            filtro_frame = ctk.CTkFrame(self.secao_frame)
            filtro_frame.pack(pady=10)

            self.regiao_var = ctk.StringVar()
            self.ano_var = ctk.StringVar()
            self.mes_var = ctk.StringVar()

            ctk.CTkLabel(filtro_frame, text="Região:").grid(row=0, column=0, padx=5)
            regiao_box = ctk.CTkComboBox(filtro_frame, variable=self.regiao_var, values=sorted(dados["Regiao"].dropna().unique().astype(str)))
            regiao_box.grid(row=0, column=1, padx=5)

            ctk.CTkLabel(filtro_frame, text="Ano:").grid(row=0, column=2, padx=5)
            ano_box = ctk.CTkComboBox(filtro_frame, variable=self.ano_var, values=sorted(dados["Ano"].dropna().unique().astype(str)))
            ano_box.grid(row=0, column=3, padx=5)

            ctk.CTkLabel(filtro_frame, text="Mês:").grid(row=0, column=4, padx=5)
            mes_box = ctk.CTkComboBox(filtro_frame, variable=self.mes_var, values=sorted(dados["Mês"].dropna().unique().astype(str)))
            mes_box.grid(row=0, column=5, padx=5)

            def aplicar_filtros():
                filtrado = dados.copy()
                if self.regiao_var.get():
                    filtrado = filtrado[filtrado["Regiao"] == self.regiao_var.get()]
                if self.ano_var.get():
                    filtrado = filtrado[filtrado["Ano"] == int(self.ano_var.get())]
                if self.mes_var.get():
                    filtrado = filtrado[filtrado["Mês"] == int(self.mes_var.get())]

                if filtrado.empty:
                    messagebox.showwarning("Nenhum dado", "Nenhum dado disponível para os filtros selecionados.")
                    return

                # Pivot Tabelas
                tab_unidade = filtrado.pivot_table(index="Unidade", values=["VAL_TOT", "QTDE"], aggfunc="sum", fill_value=0)
                tab_cliente = filtrado.pivot_table(index="Tipo_Cliente", values=["VAL_TOT", "QTDE"], aggfunc="sum", fill_value=0)
                tab_produto = filtrado.pivot_table(index="Produto", values=["VAL_TOT", "QTDE"], aggfunc="sum", fill_value=0)

                def plotar_grafico(tab, titulo, cor, coluna):
                    fig = px.bar(tab, x=tab.index, y=coluna, title=titulo, color_discrete_sequence=[cor])
                    fig.update_layout(template="plotly_white", plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False))
                    return fig

                from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

                # Limpar área anterior se necessário
                for widget in self.secao_frame.winfo_children():
                    if isinstance(widget, ctk.CTkFrame) and widget != filtro_frame:
                        widget.destroy()

                chart_frame = ctk.CTkFrame(self.secao_frame)
                chart_frame.pack(pady=10, expand=True, fill="both")

                # Unidade
                fig1 = plotar_grafico(tab_unidade, "Facturação por Unidade", "#5F9EA0", "VAL_TOT")
                canvas1 = FigureCanvasTkAgg(fig1, master=chart_frame)
                canvas1.draw()
                canvas1.get_tk_widget().pack(side="left", expand=True, fill="both")

                # Tipo Cliente
                fig2 = plotar_grafico(tab_cliente, "Facturação por Tipo Cliente", "#B22222", "VAL_TOT")
                canvas2 = FigureCanvasTkAgg(fig2, master=chart_frame)
                canvas2.draw()
                canvas2.get_tk_widget().pack(side="left", expand=True, fill="both")

                # Produto
                fig3 = plotar_grafico(tab_produto, "Facturação por Produto", "#4682B4", "VAL_TOT")
                canvas3 = FigureCanvasTkAgg(fig3, master=chart_frame)
                canvas3.draw()
                canvas3.get_tk_widget().pack(side="left", expand=True, fill="both")

            btn_aplicar = ctk.CTkButton(filtro_frame, text="Aplicar Filtros", command=aplicar_filtros)
            btn_aplicar.grid(row=0, column=6, padx=10)

        elif selecao == "Analise Maturidade":
            ctk.CTkLabel(self.secao_frame, text="[MATURIDADE DE CONSUMO AQUI]").pack(pady=20)

    def importar_facturacao(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                colunas = ['BOA IND', 'EMP ID', 'UC', 'Prod', 'DT_PROC', 'DT_FACT', 'NR_FACT', 'CLI_ID', 'CLI_CONTA', 'CIL',
                           'TP_FACT', 'TP_CLI', 'COD_TARIFA', 'VAL_TOT', 'CONCEITO', 'QTDE', 'VALOR']
                self.df = pd.read_csv(file_path, sep="\t", names=colunas)

                # Ajuste tipos para merge
                self.df['UC'] = self.df['UC'].astype(int)
                self.df['TP_FACT'] = self.df['TP_FACT'].astype(int)
                self.df['TP_CLI'] = self.df['TP_CLI'].astype(str)
                self.df['COD_TARIFA'] = self.df['COD_TARIFA'].astype(str)

                # Fazer merges
                factuc = pd.merge(self.df, self.unidade, left_on='UC', right_index=True, how='left')
                prodfact = pd.merge(factuc, self.produto, left_on='Prod', right_index=True, how='left')
                tpfact = pd.merge(prodfact, self.tp_fact, left_on='TP_FACT', right_index=True, how='left')
                clifact = pd.merge(tpfact, self.tip_client, left_on='TP_CLI', right_index=True, how='left')
                confact = pd.merge(clifact, self.tarifa, left_on='COD_TARIFA', right_index=True, how='left')
                regfact = pd.merge(confact, self.regiao, left_on='Unidade', right_index=True, how='left')

                # Organizar colunas finais (ajuste conforme necessário)
                self.df_processado = regfact[['Regiao', 'Unidade', 'CIL', 'CLI_ID', 'CLI_CONTA', 'Tipo_Cliente',
                                             'Produto', 'Tipo_Factura', 'NR_FACT', 'DT_PROC', 'DT_FACT', 'Tarifa',
                                             'VAL_TOT', 'CONCEITO', 'QTDE', 'VALOR']]

                messagebox.showinfo("Importado", f"{len(self.df_processado)} linhas importadas e processadas com sucesso!")
                self.save_button.configure(state="normal")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao importar/processar: {e}")
                self.save_button.configure(state="disabled")
                self.df_processado = None

    def salvar_no_banco(self):
        if self.df_processado is not None:
            try:
                self.df_processado.to_sql("facturação", con=self.engine, if_exists="append", index=False)
                messagebox.showinfo("Sucesso", "Dados inseridos com sucesso no banco!")
                self.save_button.configure(state="disabled")
                self.df_processado = None
            except Exception as e:
                messagebox.showerror("Erro ao salvar", str(e))
        else:
            messagebox.showwarning("Aviso", "Não há dados para salvar. Importe primeiro um arquivo.")

    def carregar_dados_do_banco(self):
        try:
            query = "SELECT * FROM facturação"
            self.df_processado = pd.read_sql(query, self.engine)
            messagebox.showinfo("Sucesso", f"{len(self.df_processado)} linhas carregadas do banco de dados.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados do banco: {e}")
            self.df_processado = None
    
class ContagemFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Departamento de Contagem").pack(pady=20)

class ContratoFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Departamento de Contratação").pack(pady=20)

class AdminFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Administração do Sistema").pack(pady=20)

class DefinicaoFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Definições de Conta").pack(pady=20)

# -------------------- Executar -------------------
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")

    login = LoginApp()
    login.mainloop()  # Espera até o login ser encerrado

    if login.user_logged and login.nivel_logged:
        app = MainApp(login.user_logged, login.nivel_logged)
        app.mainloop()
