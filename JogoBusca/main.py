import tkinter as tk
from tkinter import ttk, messagebox, font as tkFont, PhotoImage
import os
import sys
import random

# --- Importações dinâmicas das missões ---
try:
    from missoes_busca.missao1 import Missao1
except ImportError as e:
    Missao1 = None
    print(f"ALERTA DE IMPORTAÇÃO: Missao1 não pôde ser carregada. Erro: {e}")

try:
    from missoes_busca.missao2 import Missao2
except ImportError as e:
    Missao2 = None
    print(f"ALERTA DE IMPORTAÇÃO: Missao2 não pôde ser carregada. Erro: {e}")

try:
    from missoes_busca.missao3 import Missao3
except ImportError as e:
    Missao3 = None
    print(f"ALERTA DE IMPORTAÇÃO: Missao3 não pôde ser carregada. Erro: {e}")

try:
    from missoes_busca.missao4 import Missao4
except ImportError as e:
    Missao4 = None
    print(f"ALERTA DE IMPORTAÇÃO: Missao4 não pôde ser carregada. Erro: {e}")


class GameManager:
    def __init__(self, root_tk):
        self.root = root_tk
        self.root.title("Aliança Rebelde - Arquivos da Rebelião")
        self.root.configure(bg="black")
        self.root.geometry("1024x768") 

        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.img_dir = os.path.join(self.script_dir, "img")

        self.imagens = {}
        self.carregar_imagens()

        self.bg_color_dark = "black"
        self.fg_color_light = "#f0f0f0"
        self.title_color_accent = "#FFD700"
        self.header_font_obj = tkFont.Font(family="Arial", size=20, weight="bold")
        self.narrative_font_obj = tkFont.Font(family="Arial", size=12)
        self.button_font_obj = tkFont.Font(family="Arial", size=11, weight="bold")
        self.small_bold_font_obj = tkFont.Font(family="Arial", size=10, weight="bold")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Black.TFrame", background=self.bg_color_dark)
        style.configure("Accent.Dark.TButton", font=self.button_font_obj, foreground="black", background=self.title_color_accent, padding=10)
        style.map("Accent.Dark.TButton", background=[('active', '#e6c300')])
        style.configure("Dark.TButton", font=self.button_font_obj, foreground="white", background="#333333", padding=5)
        style.map("Dark.TButton", background=[('active', '#444444')])

        self.player_score = 0
        self.current_mission_obj = None
        self.content_frame = None
        
        self.game_state = "MENU_PRINCIPAL"
        self.update_display()
    
    def carregar_imagens(self):
        # Reduzir o fator de subsample para missao1.png para que ela não fique muito pequena
        nomes_imagens = {"Alianca_Rebelde.png": 2, "alianca_simbolo.png": 2, "missao1.png": 1} 
        for nome_img, subsample_factor in nomes_imagens.items():
            try:
                caminho_img = os.path.join(self.img_dir, nome_img)
                if os.path.exists(caminho_img):
                    original_img = PhotoImage(file=caminho_img)
                    self.imagens[nome_img] = original_img.subsample(subsample_factor, subsample_factor)
                    print(f"DEBUG: Imagem '{nome_img}' carregada e redimensionada.")
                else:
                    print(f"AVISO: Imagem '{nome_img}' NÃO ENCONTRADA no caminho: {caminho_img}")
                    self.imagens[nome_img] = None
            except Exception as e_img:
                print(f"AVISO: Erro ao carregar ou redimensionar '{nome_img}': {e_img}")
                self.imagens[nome_img] = None

    def _clear_content_frame(self):
        if self.content_frame: 
            self.content_frame.destroy()
        self.content_frame = ttk.Frame(self.root, padding="20", style="Black.TFrame")
        self.content_frame.pack(fill=tk.BOTH, expand=True)

    def _display_text_screen(self, title_text, narrative_text_lines, button_text, next_state_or_command, button_style="Dark.TButton", image_to_display=None):
        self._clear_content_frame()
        
        title_label = tk.Label(self.content_frame, text=title_text, font=self.header_font_obj, anchor="center", bg=self.bg_color_dark, fg=self.title_color_accent, pady=5)
        title_label.pack(pady=(10, 15), fill=tk.X)
        
        if image_to_display:
            imagem_label = tk.Label(self.content_frame, image=image_to_display, bg=self.bg_color_dark)
            imagem_label.pack(pady=(10, 10))

        narrative_label = tk.Label(self.content_frame, text="\n\n".join(narrative_text_lines), wraplength=700, justify=tk.CENTER, font=self.narrative_font_obj, fg=self.fg_color_light, bg=self.bg_color_dark)
        narrative_label.pack(padx=20, pady=10)

        if isinstance(next_state_or_command, str):
            command_to_run = lambda: self.set_game_state(next_state_or_command)
        else:
            command_to_run = next_state_or_command
            
        button_container = ttk.Frame(self.content_frame, style="Black.TFrame")
        button_container.pack(pady=(20, 10))
        actual_button_style = "Accent.Dark.TButton" if button_style == "Accent.TButton" else "Dark.TButton"
        ttk.Button(button_container, text=button_text, command=command_to_run, style=actual_button_style).pack()

    def update_display(self):
        self._clear_content_frame()
        
        if self.game_state == "MENU_PRINCIPAL":
            self._display_text_screen(
                "Aliança Rebelde - Arquivos da Rebelião",
                [""],
                "Iniciar Desafio",
                "INTRODUCAO",
                image_to_display=self.imagens.get("Alianca_Rebelde.png")
            )
        elif self.game_state == "INTRODUCAO":
            narrativa = [
                "Bem-vindo(a), Analista de Inteligência.",
                "O Império construiu um sistema de arquivos complexo para esconder suas fraquezas.",
                "Sua tarefa é usar os algoritmos mais eficientes para extrair dados vitais e dar à Aliança a vantagem de que precisamos.",
                "Sua jornada começa agora. Que a Força esteja com você."
            ]
            self._display_text_screen(
                "Iniciando Operações",
                narrativa,
                "Iniciar Missão 1",
                "START_MISSION_1",
                button_style="Accent.TButton",
                image_to_display=self.imagens.get("alianca_simbolo.png")
            )
        
        elif self.game_state == "START_MISSION_1":
            if Missao1:
                self._clear_content_frame() 
                self.current_mission_obj = Missao1(self.root, self, self.content_frame)
                self.current_mission_obj.iniciar_missao_contexto(image_to_display=self.imagens.get("missao1.png"))
            else:
                self._display_mission_not_found("Missão 1")
        elif self.game_state == "MISSION_1_SUCCESS":
            self.display_sucesso_missao("Missao1")

        elif self.game_state == "START_MISSION_2":
            if Missao2:
                self._clear_content_frame()
                self.current_mission_obj = Missao2(self.root, self, self.content_frame)
                self.current_mission_obj.iniciar_missao_contexto()
            else:
                self._display_mission_not_found("Missão 2")
        elif self.game_state == "MISSION_2_SUCCESS":
            self.display_sucesso_missao("Missao2")
        
        elif self.game_state == "START_MISSION_3":
            if Missao3:
                self._clear_content_frame()
                self.current_mission_obj = Missao3(self.root, self, self.content_frame)
                self.current_mission_obj.iniciar_missao_contexto()
            else:
                self._display_mission_not_found("Missão 3")
        elif self.game_state == "MISSION_3_SUCCESS":
            self.display_sucesso_missao("Missao3")
        
        elif self.game_state == "START_MISSION_4":
            if Missao4:
                self._clear_content_frame()
                self.current_mission_obj = Missao4(self.root, self, self.content_frame)
                self.current_mission_obj.iniciar_missao_contexto()
            else:
                self._display_mission_not_found("Missão 4")
        
        elif self.game_state == "MISSION_4_SUCCESS":
            self._display_text_screen(
                "Sucesso Final da Operação!",
                ["Parabéns, Comandante! Todas as missões foram concluídas com êxito.", "Sua habilidade analítica provou ser um recurso inestimável para a Aliança Rebelde."],
                "Ver o Epílogo",
                "ALL_MISSIONS_COMPLETED_V3",
                button_style="Accent.TButton",
            )

        elif self.game_state == "ALL_MISSIONS_COMPLETED_V3":
            narrativa = [
                "A rebelião agora possui os dados que precisava. Sua inteligência e sua dedicação foram cruciais para o sucesso da Aliança.",
                "Sua missão está completa, analista. O futuro da galáxia está em boas mãos.",
                "Que a Força esteja com você."
            ]
            self._display_text_screen(
                "Operação Concluída",
                narrativa,
                "Encerrar Jogo",
                self.root.destroy,
                button_style="Accent.TButton",
                image_to_display=self.imagens.get("alianca_simbolo.png")
            )
        
        else:
            self.set_game_state("MENU_PRINCIPAL")

    def _display_mission_not_found(self, mission_name):
        self._clear_content_frame()
        tk.Label(self.content_frame, text=f"{mission_name} não foi encontrada.", font=self.header_font_obj, fg="red", bg=self.bg_color_dark).pack(pady=20)
        tk.Label(self.content_frame, text=f"A classe para a {mission_name} não foi carregada. Por favor, verifique se o arquivo existe e se o nome da classe está correto.", wraplength=700, justify=tk.CENTER, font=self.narrative_font_obj, fg=self.fg_color_light, bg=self.bg_color_dark).pack(padx=20, pady=10)
        ttk.Button(self.content_frame, text="Voltar ao Menu Principal", command=lambda: self.set_game_state("MENU_PRINCIPAL"), style="Accent.Dark.TButton").pack(pady=20)

    def display_sucesso_missao(self, mission_id):
        self._clear_content_frame()
        tk.Label(self.content_frame, text=f"Missão {mission_id.replace('Missao', ' ')} Concluída!", font=self.header_font_obj, fg="green", bg=self.bg_color_dark).pack(pady=20)
        tk.Label(self.content_frame, text="Excelente trabalho, Analista! Os dados foram recuperados com sucesso. Preparando para a próxima missão...", wraplength=700, justify=tk.CENTER, font=self.narrative_font_obj, fg=self.fg_color_light, bg=self.bg_color_dark).pack(padx=20, pady=10)
        
        next_mission_number = int(mission_id.replace("Missao", "")) + 1
        if next_mission_number <= 4:
            next_state = f"START_MISSION_{next_mission_number}"
            button_text = f"Avançar para a Missão {next_mission_number}"
        else:
            next_state = "MISSION_4_SUCCESS"
            button_text = "Continuar..."
            
        ttk.Button(self.content_frame, text=button_text, command=lambda: self.set_game_state(next_state), style="Accent.Dark.TButton").pack(pady=20)
    
    def mission_completed(self, mission_id):
        print(f"GameManager: Missão {mission_id} concluída.")
        self.set_game_state(f"MISSION_{mission_id.replace('Missao', '')}_SUCCESS")

    def add_score(self, points):
        self.player_score += points
        print(f"Score atual: {self.player_score}")

    def mission_failed_options(self, mission_obj, title, message):
        self._clear_content_frame()
        tk.Label(self.content_frame, text="Missão Falhou!", font=self.header_font_obj, fg="red", bg=self.bg_color_dark).pack(pady=20)
        tk.Label(self.content_frame, text=message, wraplength=700, justify=tk.CENTER, font=self.narrative_font_obj, fg=self.fg_color_light, bg=self.bg_color_dark).pack(padx=20, pady=10)

        button_container = ttk.Frame(self.content_frame, style="Black.TFrame")
        button_container.pack(pady=20)
        
        ttk.Button(button_container, text="Tentar Novamente", command=mission_obj.retry_mission, style="Accent.Dark.TButton").pack(side=tk.LEFT, padx=10)
        ttk.Button(button_container, text="Voltar ao Menu Principal", command=lambda: self.set_game_state("MENU_PRINCIPAL"), style="Dark.TButton").pack(side=tk.LEFT, padx=10)

    def set_game_state(self, new_state):
        print(f"Mudando estado de '{self.game_state}' para: {new_state}")
        self.game_state = new_state
        self.root.after_idle(self.update_display)


if __name__ == "__main__":
    root = tk.Tk()
    app = GameManager(root)
    root.mainloop()