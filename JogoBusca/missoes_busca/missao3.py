# missoes_busca/missao3.py

import tkinter as tk
from tkinter import ttk, messagebox, font as tkFont
import random
from algoritmos_busca.busca_interpolar import interpolation_search  # ajuste o caminho se necessário

class Missao3:
    def __init__(self, root, game_manager, content_frame):
        self.root = root
        self.game_manager = game_manager
        self.base_content_frame = content_frame

        self.etapas_info = [
            {"titulo": "Fase 1: Sintonizando a Frequência Secreta"}
        ]
        self.etapa_atual = 0

        # Parâmetros do espectro de canais (uniforme)
        self.tamanho_espectro = 44
        self.base_freq = None
        self.passo_freq = None
        self.spectrum = []          # lista ordenada de frequências
        self.alvo_freq = None       # frequência alvo (valor)
        self.alvo_index = None      # índice alvo (posição na lista)

        # Estado da simulação
        self.steps = []             # lista de estados capturados pelo on_step
        self.step_ptr = -1          # ponteiro do passo atual
        self.resultado_busca = None # (index, steps_count)

        # UI helpers
        self._widgets_lista = []
        self._painel_labels = {}

        self._carregar_estilos()

    def _carregar_estilos(self):
        try:
            self.cor_fundo = self.game_manager.bg_color_dark
            self.cor_texto = self.game_manager.fg_color_light
            self.cor_titulo = self.game_manager.title_color_accent
            self.font_titulo = self.game_manager.header_font_obj
            self.font_narrativa = self.game_manager.narrative_font_obj
            self.font_subtitulo = self.game_manager.small_bold_font_obj
        except AttributeError:
            self.cor_fundo = "black"
            self.cor_texto = "white"
            self.cor_titulo = "yellow"
            self.font_titulo = ("Arial", 20, "bold")
            self.font_narrativa = ("Arial", 12)
            self.font_subtitulo = ("Arial", 10, "bold")

    def _limpar_frame(self):
        for widget in self.base_content_frame.winfo_children():
            widget.destroy()

    # ========= Contexto / narrativa =========
    def iniciar_missao_contexto(self, image_to_display=None):
        self._limpar_frame()
        tk.Label(
            self.base_content_frame,
            text="Operação S3: Sintonizando a Frequência Secreta",
            font=self.font_titulo, fg=self.cor_titulo, bg=self.cor_fundo
        ).pack(pady=(10, 15))

        if image_to_display:
            tk.Label(self.base_content_frame, image=image_to_display, bg=self.cor_fundo)\
                .pack(pady=(10, 10))

        contexto = (
            "Fulcrum: Comandante, uma transmissão codificada da Aliança está perdida em um espectro "
            "de canais discretos, distribuídos quase uniformemente. Para localizá-la rapidamente, "
            "vamos usar a Busca por Interpolação. O droide de protocolo R7-X mostrará, passo a passo, "
            "como estimar a posição correta no espectro sem escanear tudo."
        )
        tk.Label(
            self.base_content_frame, text=contexto, wraplength=700, justify=tk.LEFT,
            font=self.font_narrativa, fg=self.cor_texto, bg=self.cor_fundo
        ).pack(pady=10, padx=20)

        ttk.Button(
            self.base_content_frame, text="Iniciar Sintonização...",
            command=lambda: self.iniciar_etapa(0), style="Accent.Dark.TButton"
        ).pack(pady=20)

    # ========= Fases =========
    def iniciar_etapa(self, etapa_numero):
        self.etapa_atual = etapa_numero
        if self.etapa_atual == 0:
            self._gerar_espectro_e_alvo()

        self._limpar_frame()
        etapa_info = self.etapas_info[self.etapa_atual]
        tk.Label(
            self.base_content_frame, text=etapa_info["titulo"],
            font=self.font_titulo, fg=self.cor_titulo, bg=self.cor_fundo
        ).pack(pady=(10, 15))

        if etapa_numero == 0:
            self.fase_1_interpolation_search()

    # ========= Dados da missão =========
    def _gerar_espectro_e_alvo(self):
        # Gera um espectro uniforme de frequências (ex.: kHz)
        self.base_freq = random.randint(9000, 15000)   # base em kHz
        self.passo_freq = random.choice([2, 5, 10, 25])  # passo em kHz
        self.spectrum = [self.base_freq + i * self.passo_freq for i in range(self.tamanho_espectro)]

        # Escolhe uma frequência alvo dentro do espectro
        self.alvo_index = random.randrange(self.tamanho_espectro)
        self.alvo_freq = self.spectrum[self.alvo_index]

        # Reseta a simulação
        self.steps = []
        self.step_ptr = -1
        self.resultado_busca = None

    # ========= UI: Lista do espectro =========
    def _criar_lista_espectro(self, parent_frame):
        canvas = tk.Canvas(parent_frame, bg=self.cor_fundo, highlightthickness=0, width=300, height=400)
        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg=self.cor_fundo)

        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(
            scrollable, text="Canais (kHz) – Distribuição Uniforme",
            font=self.font_subtitulo, fg=self.cor_titulo, bg=self.cor_fundo
        ).grid(row=0, column=0, columnspan=3, sticky="w", padx=5, pady=(0, 6))

        self._widgets_lista = []
        for i, f in enumerate(self.spectrum, start=1):
            lbl_idx = tk.Label(scrollable, text=f"[{i-1:02d}]", font=("Courier New", 10, "bold"),
                               fg=self.cor_texto, bg=self.cor_fundo)
            lbl_idx.grid(row=i, column=0, padx=5, pady=2, sticky="w")

            lbl_freq = tk.Label(scrollable, text=f"{f} kHz", font=("Courier New", 10),
                                fg=self.cor_texto, bg="#222")
            lbl_freq.grid(row=i, column=1, padx=5, pady=2, sticky="w")

            btn = ttk.Button(
                scrollable, text="Sintonizar aqui",
                style="Dark.TButton",
                command=lambda idx=i-1: self._validar_escolha_manual(idx)
            )
            btn.grid(row=i, column=2, padx=5, pady=2, sticky="w")
            self._widgets_lista.append((lbl_idx, lbl_freq, btn))

    # ========= UI: Painel de estado da busca =========
    def _criar_painel_estado(self, parent_frame):
        frame = tk.Frame(parent_frame, bg=self.cor_fundo, bd=2, relief="solid", padx=10, pady=10)
        frame.pack(fill=tk.X, pady=8)

        tk.Label(frame, text="Painel da Sonda (Interpolação)", font=self.font_subtitulo,
                 fg=self.cor_titulo, bg=self.cor_fundo).grid(row=0, column=0, columnspan=2, sticky="w")

        rows = [
            ("Alvo (kHz):", "alvo"),
            ("Passo atual:", "passo_idx"),
            ("low (índice):", "low"),
            ("high (índice):", "high"),
            ("pos (estimado):", "pos"),
            ("arr[low] (kHz):", "arr_low"),
            ("arr[high] (kHz):", "arr_high"),
            ("arr[pos] (kHz):", "pos_val"),
            ("Comparação:", "cmp"),
        ]

        self._painel_labels = {}
        for r, (txt, key) in enumerate(rows, start=1):
            tk.Label(frame, text=txt, font=self.font_narrativa, fg=self.cor_titulo, bg=self.cor_fundo)\
                .grid(row=r, column=0, sticky="w", padx=4, pady=2)
            val = tk.Label(frame, text="-", font=self.font_narrativa, fg=self.cor_texto, bg=self.cor_fundo)
            val.grid(row=r, column=1, sticky="w", padx=4, pady=2)
            self._painel_labels[key] = val

        # Inicializa com alvo
        self._painel_labels["alvo"].config(text=f"{self.alvo_freq} kHz")

    def _atualizar_painel(self, step_dict):
        # step_dict tem chaves: low, high, pos, arr_low, arr_high, pos_val, cmp
        mapping = {
            "passo_idx": str(self.step_ptr + 1),
            "low": str(step_dict.get("low")),
            "high": str(step_dict.get("high")),
            "pos": str(step_dict.get("pos")),
            "arr_low": "-" if step_dict.get("arr_low") is None else f"{step_dict['arr_low']} kHz",
            "arr_high": "-" if step_dict.get("arr_high") is None else f"{step_dict['arr_high']} kHz",
            "pos_val": "-" if step_dict.get("pos_val") is None else f"{step_dict['pos_val']} kHz",
            "cmp": str(step_dict.get("cmp")),
        }
        for k, v in mapping.items():
            if k in self._painel_labels:
                self._painel_labels[k].config(text=v)

    # ========= Fluxo da fase =========
    def fase_1_interpolation_search(self):
        main = tk.Frame(self.base_content_frame, bg=self.cor_fundo)
        main.pack(expand=True, fill="both")

        # Esquerda: Espectro
        left = tk.Frame(main, bg=self.cor_fundo)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self._criar_lista_espectro(left)

        # Direita: Narrativa + Controles + Painel
        right = tk.Frame(main, bg=self.cor_fundo)
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        narrativa = (
            "R7-X: O espectro é quase uniforme. A Busca por Interpolação estima a posição do alvo "
            "considerando seu valor relativo entre os limites atuais (low/high). "
            "Use a simulação para ver cada passo e entender como convergimos rapidamente."
        )
        tk.Label(
            right, text=narrativa, wraplength=350, font=self.font_narrativa,
            fg=self.cor_texto, bg=self.cor_fundo
        ).pack(pady=(0, 10))

        # Painel de estado
        self._criar_painel_estado(right)

        # Controles da simulação
        ctrl = tk.Frame(right, bg=self.cor_fundo)
        ctrl.pack(pady=8)

        ttk.Button(ctrl, text="Simular Interpolação (gerar passos)",
                   style="Accent.Dark.TButton", command=self._rodar_simulacao)\
            .grid(row=0, column=0, padx=4, pady=4, sticky="w")

        self.btn_prev = ttk.Button(ctrl, text="◀ Passo anterior", style="Dark.TButton",
                                   command=self._passo_anterior, state="disabled")
        self.btn_prev.grid(row=0, column=1, padx=4, pady=4, sticky="w")

        self.btn_next = ttk.Button(ctrl, text="Próximo passo ▶", style="Dark.TButton",
                                   command=self._proximo_passo, state="disabled")
        self.btn_next.grid(row=0, column=2, padx=4, pady=4, sticky="w")

        ttk.Button(right, text="Reiniciar Missão", style="Dark.TButton",
                   command=self.retry_mission).pack(pady=(12, 0))

        # Dica
        ttk.Button(right, text="Dica Rápida",
                   style="Dark.TButton", command=self._mostrar_dica)\
            .pack(pady=(6, 0))

    # ========= Simulação (coleta dos passos) =========
    def _rodar_simulacao(self):
        # Se já rodou, apenas habilita a navegação
        if self.steps:
            self.step_ptr = -1
            self._habilitar_nav(True)
            messagebox.showinfo("Simulação", "Passos já gerados. Use os botões para navegar.")
            return

        def on_step(state):
            # Captura o estado de cada iteração
            self.steps.append(state)

        # Executa a busca (gera os passos via callback)
        idx, steps_count = interpolation_search(self.spectrum, self.alvo_freq, on_step=on_step)
        self.resultado_busca = (idx, steps_count)

        if not self.steps:
            messagebox.showwarning("Simulação", "Nenhum passo coletado (lista vazia?).")
            return

        # Prepara navegação
        self.step_ptr = -1
        self._habilitar_nav(True)
        self.game_manager.add_score(10)  # bônus por explorar a simulação
        messagebox.showinfo(
            "Simulação pronta",
            "Os passos foram gerados! Avance para ver como a interpolação converge."
        )

    def _habilitar_nav(self, enable: bool):
        state = "normal" if enable else "disabled"
        self.btn_prev.config(state=state)
        self.btn_next.config(state=state)

    def _proximo_passo(self):
        if not self.steps:
            return
        if self.step_ptr + 1 >= len(self.steps):
            return
        self.step_ptr += 1
        step = self.steps[self.step_ptr]
        self._atualizar_painel(step)

        # Se encontrou (cmp == "eq"), finalizar
        if step.get("cmp") == "eq":
            self._concluir_por_simulacao()

    def _passo_anterior(self):
        if not self.steps or self.step_ptr <= 0:
            return
        self.step_ptr -= 1
        step = self.steps[self.step_ptr]
        self._atualizar_painel(step)

    # ========= Ações do jogador =========
    def _validar_escolha_manual(self, idx_clicado: int):
        # Jogador tenta “sintonizar” diretamente por palpíte
        if idx_clicado == self.alvo_index:
            self.game_manager.add_score(120)  # acerto direto
            messagebox.showinfo("Sinal Encontrado!", "Frequência correta sintonizada!")
            self.finalizar_missao(steps_usados=None, via="manual")
        else:
            self.game_manager.add_score(-25)
            messagebox.showerror("Sem Sinal", "Canal incorreto! Tente novamente ou rode a simulação.")

    def _concluir_por_simulacao(self):
        # Usa resultado da busca para pontuar
        idx, steps_count = self.resultado_busca if self.resultado_busca else (-1, len(self.steps))
        if idx == self.alvo_index:
            # Pontuação decrescente com passos (mínimo 50)
            pontos = max(50, 160 - 5 * steps_count)
            self.game_manager.add_score(pontos)
            messagebox.showinfo("Sinal Bloqueado!", f"Alvo encontrado em {steps_count} passos.")
            self.finalizar_missao(steps_usados=steps_count, via="simulação")
        else:
            self.game_manager.add_score(-40)
            messagebox.showerror("Falha na Sintonização", "A simulação não convergiu para o canal correto.")

    # ========= Finalização =========
    def finalizar_missao(self, steps_usados=None, via="simulação"):
        self._limpar_frame()

        tk.Label(self.base_content_frame, text="Missão Concluída!",
                 font=self.font_titulo, fg="green", bg=self.cor_fundo)\
            .pack(pady=(10, 15))

        subtitulo = f"Frequência Secreta Sintonizada: {self.alvo_freq} kHz (canal {self.alvo_index})"
        tk.Label(self.base_content_frame, text=subtitulo,
                 font=self.font_subtitulo, fg=self.cor_titulo, bg=self.cor_fundo)\
            .pack(pady=(5, 10))

        detalhes = tk.Frame(self.base_content_frame, bg=self.cor_fundo)
        detalhes.pack(padx=20, pady=10)

        row = 0
        info = {
            "Base do espectro (kHz)": self.base_freq,
            "Passo entre canais (kHz)": self.passo_freq,
            "Tamanho do espectro": self.tamanho_espectro,
            "Método de localização": "Palpite manual" if via == "manual" else "Busca por Interpolação",
            "Passos usados": "-" if steps_usados is None else steps_usados,
        }
        for k, v in info.items():
            tk.Label(detalhes, text=f"{k}:", font=self.font_narrativa,
                     fg=self.cor_titulo, bg=self.cor_fundo)\
                .grid(row=row, column=0, sticky="w", padx=5, pady=2)
            tk.Label(detalhes, text=str(v), font=self.font_narrativa,
                     fg=self.cor_texto, bg=self.cor_fundo)\
                .grid(row=row, column=1, sticky="w", padx=5, pady=2)
            row += 1

        narrativa_final = (
            "R7-X: Excelente trabalho, Comandante. Com a frequência segura sintonizada, "
            "a transmissão da Aliança está novamente ao alcance. A frota pode prosseguir."
        )
        tk.Label(
            self.base_content_frame, text=narrativa_final, wraplength=700, justify=tk.CENTER,
            font=self.font_narrativa, fg=self.cor_texto, bg=self.cor_fundo
        ).pack(pady=20)

        ttk.Button(
            self.base_content_frame, text="Concluir Missão",
            command=lambda: self.game_manager.mission_completed("Missao3"),
            style="Accent.Dark.TButton"
        ).pack(pady=20)

    # ========= Utilidades =========
    def retry_mission(self):
        self.game_manager.set_game_state("START_MISSION_3")

    def _mostrar_dica(self):
        dica = (
            "R7-X: Se o espectro é quase uniforme, a posição estimada é:\n\n"
            "pos = low + ((alvo - arr[low]) * (high - low)) / (arr[high] - arr[low])\n\n"
            "Depois, comparamos arr[pos] ao alvo para reduzir o intervalo rapidamente."
        )
        messagebox.showinfo("Dica de Interpolação", dica)
        self.game_manager.add_score(-5)
    def retry_mission(self):
        # Reinicia para a fase atual (ou recomeça do zero, se preferir)
        self.low, self.high, self.mid = 0, len(self.lista_agentes) - 1, None
        self.game_manager.set_game_state("START_MISSION_3")