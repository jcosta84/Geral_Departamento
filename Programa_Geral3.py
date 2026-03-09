import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
import json, os
from urllib.parse import quote_plus
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


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
            self.destroy()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")


# -------------------- Aplicativo principal -------------------
class MainApp(ctk.CTk):
    def __init__(self, user, nivel):
        super().__init__()
        self.geometry("1200x700")
        self.title(f"Menu Principal - {user}")
        self.user = user
        self.nivel = nivel
        self.frames = {}

        self.carregar_tabelas_auxiliares()
        self.build_ui()

    def carregar_tabelas_auxiliares(self):
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
        self.menu_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.menu_frame.pack(side="left", fill="y")
        self.menu_frame.pack_propagate(False)

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(side="right", expand=True, fill="both")

        ctk.CTkLabel(
            self.menu_frame,
            text=f"Menu Principal - {self.user}",
            font=("Arial", 16, "bold")
        ).pack(pady=(10, 20), padx=10)

        self.submenu_frames = {}
        self.menu_buttons = {}

        estrutura_menu = {
            "Home": [
                ("Página Inicial", "home")
            ],
            "DAC - Lojas": [
                ("Importação", "dac_import"),
                ("Dashboard", "dac_dashboard")
            ],
            "Dep. Facturação": [
                ("Importação", "fact_import"),
                ("Dashboard", "fact_dashboard"),
                ("Analise Maturidade", "fact_maturidade")
            ],
            "Dep. Gestão Contagem": [
                ("Importação", "cont_import"),
                ("Dashboard", "cont_dashboard")
            ],
            "Dep. Contratação": [
                ("Novo Contrato", "contrato_novo"),
                ("Consulta", "contrato_consulta")
            ],
            "Administração": [
                ("Utilizadores", "admin_users"),
                ("Permissões", "admin_perm")
            ],
            "Definição": [
                ("Conta", "def_conta"),
                ("Preferências", "def_pref")
            ]
        }

        for menu_principal, submenus in estrutura_menu.items():
            self.criar_menu_expansivel(menu_principal, submenus)

        self.abrir_submenu("home")

    def criar_menu_expansivel(self, titulo, submenus):
        btn_menu = ctk.CTkButton(
            self.menu_frame,
            text=f"▶ {titulo}",
            height=40,
            anchor="w",
            fg_color="#1f6aa5",
            hover_color="#144870",
            corner_radius=6,
            command=lambda t=titulo: self.toggle_submenu(t)
        )
        btn_menu.pack(fill="x", padx=10, pady=(2, 2))

        self.menu_buttons[titulo] = btn_menu

        submenu_frame = ctk.CTkFrame(self.menu_frame, fg_color="transparent")
        self.submenu_frames[titulo] = submenu_frame

        for nome_submenu, chave_submenu in submenus:
            btn_sub = ctk.CTkButton(
                submenu_frame,
                text=f"   {nome_submenu}",
                height=30,
                anchor="w",
                fg_color="transparent",
                hover_color="#3a3a3a",
                text_color="white",
                corner_radius=4,
                command=lambda c=chave_submenu: self.abrir_submenu(c)
            )
            btn_sub.pack(fill="x", padx=25, pady=2)

    def toggle_submenu(self, titulo):
        frame = self.submenu_frames[titulo]
        botao = self.menu_buttons[titulo]

        if frame.winfo_ismapped():
            frame.pack_forget()
            botao.configure(text=f"▶ {titulo}")
        else:
            frame.pack(fill="x", padx=5, pady=(0, 5))
            botao.configure(text=f"▼ {titulo}")

    def abrir_submenu(self, chave):
        for frame in self.content_frame.winfo_children():
            frame.destroy()

        if chave == "home":
            frame = HomeFrame(self.content_frame)

        elif chave == "dac_import":
            frame = DACFrame(self.content_frame, "Importação")

        elif chave == "dac_dashboard":
            frame = DACFrame(self.content_frame, "Dashboard")

        elif chave == "fact_import":
            frame = FacturaFrame(
                self.content_frame, engine,
                self.unidade, self.produto, self.tp_fact,
                self.tip_client, self.tarifa, self.regiao,
                secao_inicial="Importação"
            )

        elif chave == "fact_dashboard":
            frame = FacturaFrame(
                self.content_frame, engine,
                self.unidade, self.produto, self.tp_fact,
                self.tip_client, self.tarifa, self.regiao,
                secao_inicial="Dashboard"
            )

        elif chave == "fact_maturidade":
            frame = FacturaFrame(
                self.content_frame, engine,
                self.unidade, self.produto, self.tp_fact,
                self.tip_client, self.tarifa, self.regiao,
                secao_inicial="Analise Maturidade"
            )

        elif chave == "cont_import":
            frame = ContagemFrame(self.content_frame, "Importação")

        elif chave == "cont_dashboard":
            frame = ContagemFrame(self.content_frame, "Dashboard")

        elif chave == "contrato_novo":
            frame = ContratoFrame(self.content_frame, "Novo Contrato")

        elif chave == "contrato_consulta":
            frame = ContratoFrame(self.content_frame, "Consulta")

        elif chave == "admin_users":
            frame = AdminFrame(self.content_frame, "Utilizadores")

        elif chave == "admin_perm":
            frame = AdminFrame(self.content_frame, "Permissões")

        elif chave == "def_conta":
            frame = DefinicaoFrame(self.content_frame, "Conta")

        elif chave == "def_pref":
            frame = DefinicaoFrame(self.content_frame, "Preferências")

        else:
            frame = ctk.CTkFrame(self.content_frame)
            ctk.CTkLabel(frame, text=f"Submenu: {chave}").pack(pady=20)

        frame.pack(expand=True, fill="both")


# -------------------- Frames -------------------
class HomeFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Bem-vindo à Home", font=("Arial", 20, "bold")).pack(pady=30)


class DACFrame(ctk.CTkFrame):
    def __init__(self, master, secao="Importação"):
        super().__init__(master)
        ctk.CTkLabel(self, text="DAC - Lojas", font=("Arial", 20, "bold")).pack(pady=20)
        ctk.CTkLabel(self, text=f"Submenu selecionado: {secao}", font=("Arial", 14)).pack(pady=10)


class FacturaFrame(ctk.CTkFrame):
    def __init__(self, master, engine, unidade, produto, tp_fact, tip_client, tarifa, regiao, secao_inicial="Importação"):
        super().__init__(master)
        self.engine = engine
        self.unidade = unidade
        self.produto = produto
        self.tp_fact = tp_fact
        self.tip_client = tip_client
        self.tarifa = tarifa
        self.regiao = regiao

        self.df = None
        self.df_processado = None
        self.secao_inicial = secao_inicial

        ctk.CTkLabel(
            self,
            text="Departamento de Facturação",
            font=("Arial", 20, "bold")
        ).pack(pady=15)

        self.secao_frame = ctk.CTkFrame(self)
        self.secao_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.mostrar_secao(self.secao_inicial)

    def limpar_secao(self):
        for widget in self.secao_frame.winfo_children():
            widget.destroy()

    def mostrar_secao(self, selecao):
        self.limpar_secao()

        if selecao == "Importação":
            frame_import = ctk.CTkFrame(self.secao_frame)
            frame_import.pack(pady=20)

            self.import_button = ctk.CTkButton(
                frame_import,
                text="Importar TXT",
                command=self.importar_facturacao
            )
            self.import_button.pack(pady=10)

            self.save_button = ctk.CTkButton(
                frame_import,
                text="Salvar no Banco",
                command=self.salvar_no_banco,
                state="disabled" if self.df_processado is None else "normal"
            )
            self.save_button.pack(pady=10)

            self.load_button = ctk.CTkButton(
                frame_import,
                text="Carregar Dados do Banco",
                command=self.carregar_dados_do_banco
            )
            self.load_button.pack(pady=10)

        elif selecao == "Dashboard":
            if self.df_processado is None:
                aviso_frame = ctk.CTkFrame(self.secao_frame)
                aviso_frame.pack(expand=True)

                ctk.CTkLabel(
                    aviso_frame,
                    text="Importe ou carregue primeiro os dados para visualizar o dashboard.",
                    font=("Arial", 14)
                ).pack(pady=20)

                ctk.CTkButton(
                    aviso_frame,
                    text="Carregar Dados do Banco",
                    command=self.carregar_e_abrir_dashboard
                ).pack(pady=10)
                return

            dados = self.df_processado.copy()
            dados["DT_FACT"] = pd.to_datetime(dados["DT_FACT"], errors="coerce")
            dados["Ano"] = dados["DT_FACT"].dt.year
            dados["Mês"] = dados["DT_FACT"].dt.month

            filtro_frame = ctk.CTkFrame(self.secao_frame)
            filtro_frame.pack(pady=10, padx=10, fill="x")

            self.regiao_var = ctk.StringVar(value="")
            self.ano_var = ctk.StringVar(value="")
            self.mes_var = ctk.StringVar(value="")

            lista_regiao = [""] + sorted(dados["Regiao"].dropna().astype(str).unique().tolist())
            lista_ano = [""] + sorted(dados["Ano"].dropna().astype(int).astype(str).unique().tolist())
            lista_mes = [""] + sorted(dados["Mês"].dropna().astype(int).astype(str).unique().tolist())

            ctk.CTkLabel(filtro_frame, text="Região:").grid(row=0, column=0, padx=5, pady=8)
            regiao_box = ctk.CTkComboBox(filtro_frame, variable=self.regiao_var, values=lista_regiao, width=160)
            regiao_box.grid(row=0, column=1, padx=5, pady=8)

            ctk.CTkLabel(filtro_frame, text="Ano:").grid(row=0, column=2, padx=5, pady=8)
            ano_box = ctk.CTkComboBox(filtro_frame, variable=self.ano_var, values=lista_ano, width=120)
            ano_box.grid(row=0, column=3, padx=5, pady=8)

            ctk.CTkLabel(filtro_frame, text="Mês:").grid(row=0, column=4, padx=5, pady=8)
            mes_box = ctk.CTkComboBox(filtro_frame, variable=self.mes_var, values=lista_mes, width=120)
            mes_box.grid(row=0, column=5, padx=5, pady=8)

            chart_frame = ctk.CTkFrame(self.secao_frame)
            chart_frame.pack(pady=10, padx=10, expand=True, fill="both")

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

                for widget in chart_frame.winfo_children():
                    widget.destroy()

                tab_unidade = filtrado.pivot_table(
                    index="Unidade", values=["VAL_TOT", "QTDE"], aggfunc="sum", fill_value=0
                )
                tab_cliente = filtrado.pivot_table(
                    index="Tipo_Cliente", values=["VAL_TOT", "QTDE"], aggfunc="sum", fill_value=0
                )
                tab_produto = filtrado.pivot_table(
                    index="Produto", values=["VAL_TOT", "QTDE"], aggfunc="sum", fill_value=0
                )

                fig1 = Figure(figsize=(4, 3), dpi=100)
                ax1 = fig1.add_subplot(111)
                tab_unidade["VAL_TOT"].plot(kind="bar", ax=ax1)
                ax1.set_title("Facturação por Unidade")
                ax1.set_ylabel("Valor Total")
                ax1.tick_params(axis='x', rotation=45)

                canvas1 = FigureCanvasTkAgg(fig1, master=chart_frame)
                canvas1.draw()
                canvas1.get_tk_widget().pack(side="left", expand=True, fill="both", padx=5, pady=5)

                fig2 = Figure(figsize=(4, 3), dpi=100)
                ax2 = fig2.add_subplot(111)
                tab_cliente["VAL_TOT"].plot(kind="bar", ax=ax2)
                ax2.set_title("Facturação por Tipo Cliente")
                ax2.set_ylabel("Valor Total")
                ax2.tick_params(axis='x', rotation=45)

                canvas2 = FigureCanvasTkAgg(fig2, master=chart_frame)
                canvas2.draw()
                canvas2.get_tk_widget().pack(side="left", expand=True, fill="both", padx=5, pady=5)

                fig3 = Figure(figsize=(4, 3), dpi=100)
                ax3 = fig3.add_subplot(111)
                tab_produto["VAL_TOT"].plot(kind="bar", ax=ax3)
                ax3.set_title("Facturação por Produto")
                ax3.set_ylabel("Valor Total")
                ax3.tick_params(axis='x', rotation=45)

                canvas3 = FigureCanvasTkAgg(fig3, master=chart_frame)
                canvas3.draw()
                canvas3.get_tk_widget().pack(side="left", expand=True, fill="both", padx=5, pady=5)

            btn_aplicar = ctk.CTkButton(
                filtro_frame,
                text="Aplicar Filtros",
                command=aplicar_filtros
            )
            btn_aplicar.grid(row=0, column=6, padx=10, pady=8)

        elif selecao == "Analise Maturidade":
            frame_mat = ctk.CTkFrame(self.secao_frame)
            frame_mat.pack(expand=True, fill="both", pady=20, padx=20)

            ctk.CTkLabel(
                frame_mat,
                text="[MATURIDADE DE CONSUMO AQUI]",
                font=("Arial", 16)
            ).pack(pady=20)

    def carregar_e_abrir_dashboard(self):
        self.carregar_dados_do_banco()
        if self.df_processado is not None:
            self.mostrar_secao("Dashboard")

    def importar_facturacao(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                colunas = [
                    'BOA IND', 'EMP ID', 'UC', 'Prod', 'DT_PROC', 'DT_FACT', 'NR_FACT', 'CLI_ID',
                    'CLI_CONTA', 'CIL', 'TP_FACT', 'TP_CLI', 'COD_TARIFA', 'VAL_TOT',
                    'CONCEITO', 'QTDE', 'VALOR'
                ]
                self.df = pd.read_csv(file_path, sep="\t", names=colunas)

                self.df['UC'] = self.df['UC'].astype(int)
                self.df['TP_FACT'] = self.df['TP_FACT'].astype(str)
                self.df['TP_CLI'] = self.df['TP_CLI'].astype(str)
                self.df['COD_TARIFA'] = self.df['COD_TARIFA'].astype(str)

                factuc = pd.merge(self.df, self.unidade, left_on='UC', right_index=True, how='left')
                prodfact = pd.merge(factuc, self.produto, left_on='Prod', right_index=True, how='left')
                tpfact = pd.merge(prodfact, self.tp_fact, left_on='TP_FACT', right_index=True, how='left')
                clifact = pd.merge(tpfact, self.tip_client, left_on='TP_CLI', right_index=True, how='left')
                confact = pd.merge(clifact, self.tarifa, left_on='COD_TARIFA', right_index=True, how='left')
                regfact = pd.merge(confact, self.regiao, left_on='Unidade', right_index=True, how='left')

                self.df_processado = regfact[
                    ['Regiao', 'Unidade', 'CIL', 'CLI_ID', 'CLI_CONTA', 'Tipo_Cliente',
                     'Produto', 'Tipo_Factura', 'NR_FACT', 'DT_PROC', 'DT_FACT', 'Tarifa',
                     'VAL_TOT', 'CONCEITO', 'QTDE', 'VALOR']
                ]

                messagebox.showinfo(
                    "Importado",
                    f"{len(self.df_processado)} linhas importadas e processadas com sucesso!"
                )

                if hasattr(self, "save_button"):
                    self.save_button.configure(state="normal")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao importar/processar: {e}")
                if hasattr(self, "save_button"):
                    self.save_button.configure(state="disabled")
                self.df_processado = None

    def salvar_no_banco(self):
        if self.df_processado is not None:
            try:
                self.df_processado.to_sql("facturação", con=self.engine, if_exists="append", index=False)
                messagebox.showinfo("Sucesso", "Dados inseridos com sucesso no banco!")
                if hasattr(self, "save_button"):
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
    def __init__(self, master, secao="Importação"):
        super().__init__(master)
        ctk.CTkLabel(self, text="Departamento de Contagem", font=("Arial", 20, "bold")).pack(pady=20)
        ctk.CTkLabel(self, text=f"Submenu selecionado: {secao}", font=("Arial", 14)).pack(pady=10)


class ContratoFrame(ctk.CTkFrame):
    def __init__(self, master, secao="Novo Contrato"):
        super().__init__(master)
        ctk.CTkLabel(self, text="Departamento de Contratação", font=("Arial", 20, "bold")).pack(pady=20)
        ctk.CTkLabel(self, text=f"Submenu selecionado: {secao}", font=("Arial", 14)).pack(pady=10)


class AdminFrame(ctk.CTkFrame):
    def __init__(self, master, secao="Utilizadores"):
        super().__init__(master)
        ctk.CTkLabel(self, text="Administração do Sistema", font=("Arial", 20, "bold")).pack(pady=20)
        ctk.CTkLabel(self, text=f"Submenu selecionado: {secao}", font=("Arial", 14)).pack(pady=10)


class DefinicaoFrame(ctk.CTkFrame):
    def __init__(self, master, secao="Conta"):
        super().__init__(master)
        ctk.CTkLabel(self, text="Definições de Conta", font=("Arial", 20, "bold")).pack(pady=20)
        ctk.CTkLabel(self, text=f"Submenu selecionado: {secao}", font=("Arial", 14)).pack(pady=10)


# -------------------- Executar -------------------
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    login = LoginApp()
    login.mainloop()

    if login.user_logged and login.nivel_logged:
        app = MainApp(login.user_logged, login.nivel_logged)
        app.mainloop()