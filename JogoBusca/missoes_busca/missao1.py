# missoes_busca/missao1.py
import tkinter as tk
from tkinter import ttk, messagebox, font as tkFont

class Missao1:
    def __init__(self, root, game_manager, content_frame):
        self.root = root
        self.game_manager = game_manager
        self.base_content_frame = content_frame
        self._carregar_estilos()

    def _carregar_estilos(self):
        try:
            self.cor_fundo = self.game_manager.bg_color_dark
            self.cor_texto = self.game_manager.fg_color_light
            self.cor_titulo = self.game_manager.title_color_accent
            self.font_titulo = self.game_manager.header_font_obj
            self.font_narrativa = self.game_manager.narrative_font_obj
        except AttributeError:
            self.cor_fundo = "black"
            self.cor_texto = "white"
            self.cor_titulo = "yellow"
            self.font_titulo = ("Arial", 20, "bold")
            self.font_narrativa = ("Arial", 12)

    def _limpar_frame(self):
        for widget in self.base_content_frame.winfo_children():
            widget.destroy()

    def iniciar_missao_contexto(self):
        self._limpar_frame()
        tk.Label(
            self.base_content_frame,
            text="Missão 1: Inspeção no Hangar de Carga",
            font=self.font_titulo,
            fg=self.cor_titulo,
            bg=self.cor_fundo
        ).pack(pady=(10, 15))

        contexto = (
            "Sua missão é encontrar um item de contrabando específico em uma série de contêineres desorganizados. "
            "Você precisará inspecionar cada contêiner um por um, na ordem em que eles aparecem."
        )

        tk.Label(
            self.base_content_frame,
            text=contexto,
            wraplength=700,
            justify=tk.LEFT,
            font=self.font_narrativa,
            fg=self.cor_texto,
            bg=self.cor_fundo
        ).pack(pady=10, padx=20)

        ttk.Button(
            self.base_content_frame,
            text="Concluir Missão 1",
            command=lambda: self.game_manager.mission_completed("Missao1"),
            style="Accent.Dark.TButton"
        ).pack(pady=20)

    def retry_mission(self):
        print("Missão 1: retry_mission chamada.")
        self.game_manager.set_game_state("START_MISSION_1")