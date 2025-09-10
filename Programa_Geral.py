import customtkinter as ctk
import pandas as pd



#-------------------------- departamento facturação ---------------------
class depfactFrame(ctk.CTkFrame):
    def __init__(self, master, width = 200, height = 200, corner_radius = None, border_width = None, bg_color = "transparent", fg_color = None, border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
 
        # Criar menu horizontal com CTkSegmentedButton
        self.menu_selector = ctk.CTkSegmentedButton(
            self,
            values=["Importação", "Dashboard", "Analise Maturidade"],
            command=self.mudar_secao
        )
        self.menu_selector.pack(pady=20)
        self.menu_selector.set("Importação")  # seleciona inicialmente

        self.menu_selector.pack(pady=20)
        self.menu_selector.set("Importação")  # seleciona inicialmente

        # Separador visual
        ctk.CTkLabel(self, text="-" * 900).pack(pady=5)  # substitui st.markdown("---")

        # Área principal de conteúdo
        self.area_conteudo = ctk.CTkLabel(self, text="Importação", font=("Arial", 20))
        self.area_conteudo.pack(pady=50)

    def mudar_secao(self, opcao):
        self.area_conteudo.configure(text=opcao)
        
# ------------------------- janela principal ----------------------------
class AppPrincipal(ctk.CTk):
    def __init__(self, fg_color=None, **kwargs):
        super().__init__(fg_color=fg_color, **kwargs)

        # Define o modo de aparência e tema
        ctk.set_appearance_mode("dark")  # ou "light", "system"
        ctk.set_default_color_theme("blue")  # ou outro: "green", "dark-blue", etc.
        #criar titulo e geometria da janela
        self.title("Departamento Geral")
        self.geometry("1000x600")

        
        #criar uma sidebar
        self.sidebar = ctk.CTkFrame(self, width=250)
        self.sidebar.pack(side="left", fill="y")

        #criar uma container
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="right", fill="both", expand=True)

        # Espaçador antes dos botões
        ctk.CTkLabel(self.sidebar, text="", height=50).pack()  # cria espaço vazio

        #inserir opções de menu
        ctk.CTkButton(self.sidebar, text="DAC - Lojas", anchor="w").pack(pady=5, fill="x")
        ctk.CTkButton(self.sidebar, text="Dep. Facturação", anchor="w", command=lambda: self.carregar(depfactFrame)).pack(pady=5, fill="x")
        ctk.CTkButton(self.sidebar, text="Dep. Gestão Contagem", anchor="w").pack(pady=5, fill="x")
        ctk.CTkButton(self.sidebar, text="Dep. Contratação", anchor="w").pack(pady=5, fill="x")

        #opção de sair do aplicativo
        ctk.CTkButton(self.sidebar, text="Sair", command=self.destroy).pack(side="bottom", pady=10, fill="x")
        

        self.frames = {}

    # Em carregar():
    def carregar(self, FrameClass):
        # Destrói o frame atual, se existir
        for frame in self.frames.values():
            frame.pack_forget()

        # Se o frame ainda não existe, cria
        if FrameClass not in self.frames:
            frame = FrameClass(self)
            self.frames[FrameClass] = frame
        else:
            frame = self.frames[FrameClass]

        # Mostra o frame
        frame.pack(fill="both", expand=True)

    def abrir_depfact(self):
        self.carregar(depfactFrame)

      

if __name__ == "__main__":
    app = AppPrincipal()
    app.mainloop()
