# missoes_busca/missao2.py
import tkinter as tk
from tkinter import ttk, messagebox
import random

# ===============================
# Fallback de dados (ordenados)
# ===============================
try:
    from BancoDados.agentes_imperiais import AGENTES_IMPERIAIS_ORDENADOS
except Exception:
    # Gera uma lista estável e ordenada de "agentes" se o módulo não existir
    random.seed(1138)
    base_ids = sorted(random.sample(range(1000, 9999), 80))
    codinomes = [
        "Womp Rat", "Dark Lance", "Nova-7", "Nebula", "Specter", "Night Wind", "Iron Pike",
        "Void-13", "Krennic-Cell", "Rancor", "Echani", "Tarkin-Unit", "Skyrise", "Maw-2",
        "Black Sun", "Crimson Dawn", "Obsidian", "Stygian", "Vanguard", "Dread Star"
    ]
    postos = ["Oficial", "Analista", "Sargento", "Tenente", "Inquisidor", "Agente", "Comissário"]
    AGENTES_IMPERIAIS_ORDENADOS = [
        {
            "id": base_ids[i],
            "nome": f"{random.choice(codinomes)}",
            "posto": random.choice(postos),
            "setor": random.choice(["Kuat", "Scarif", "Eriadu", "Corellia", "Lothal", "Mustafar"])
        }
        for i in range(len(base_ids))
    ]

class Missao2:
    """
    Missão 2 — Busca Binária
    Fase 1: Encontrar o infiltrado por ID (básico)
    Fase 2: Registros duplicados — encontrar a PRIMEIRA ocorrência (lower_bound)
    Fase 3: Consulta por faixa — confirmar se existe ID no intervalo (busca binária dupla)
    """
    def __init__(self, root, game_manager, content_frame):
        self.root = root
        self.game_manager = game_manager
        self.base_content_frame = content_frame

        # Estados comuns
        self.etapas_info = [
            {
                "titulo": "Fase 1: O ID do Infiltrado",
                "narrativa": (
                    "Fulcrum: \"Temos um agente Imperial infiltrado. A lista está ORDENADA por ID. "
                    "Use a busca binária para localizar o registro preciso (ID exato).\""
                )
            },
            {
                "titulo": "Fase 2: Registros Duplicados",
                "narrativa": (
                    "R7-X: \"Interceptamos múltiplos registros com o MESMO ID (duplicatas). "
                    "Sua tarefa: encontrar a PRIMEIRA ocorrência (menor índice) com aquele ID. "
                    "Dica: ajuste low/high quando igual para ir em direção ao início.\""
                )
            },
            {
                "titulo": "Fase 3: Sintonizando o Setor",
                "narrativa": (
                    "Fulcrum: \"Precisamos saber se há ALGUM agente com ID dentro de um INTERVALO. "
                    "Use duas buscas binárias (lower/upper) para confirmar rapidamente se existe "
                    "pelo menos um ID na faixa especificada.\""
                )
            }
        ]
        self.etapa_atual = 0

        self.lista_agentes = list(AGENTES_IMPERIAIS_ORDENADOS)  # copia
        self.low = 0
        self.high = len(self.lista_agentes) - 1
        self.mid = None

        # Alvos por fase
        self.target_id = None         # Fase 1 — alvo exato
        self.target_id_dup = None     # Fase 2 — ID com duplicatas
        self.range_min = None         # Fase 3 — limite inferior
        self.range_max = None         # Fase 3 — limite superior

        # UI refs
        self.label_intervalo = None
        self.label_feedback = None
        self.entry_id = None
        self.entry_min = None
        self.entry_max = None
        self.btn_low = None
        self.btn_mid = None
        self.btn_high = None
        self.btn_esquerda = None
        self.btn_direita = None
        self.btn_encontrado = None

        self._carregar_estilos()

    def _carregar_estilos(self):
        try:
            self.cor_fundo = self.game_manager.bg_color_dark
            self.cor_texto = self.game_manager.fg_color_light
            self.cor_titulo = self.game_manager.title_color_accent
            self.font_titulo = self.game_manager.header_font_obj
            self.font_narrativa = self.game_manager.narrative_font_obj
            self.font_sub = self.game_manager.small_bold_font_obj
        except AttributeError:
            self.cor_fundo = "black"
            self.cor_texto = "white"
            self.cor_titulo = "yellow"
            self.font_titulo = ("Arial", 20, "bold")
            self.font_narrativa = ("Arial", 12)
            self.font_sub = ("Arial", 10, "bold")

    def _limpar_frame(self):
        for w in self.base_content_frame.winfo_children():
            w.destroy()

    # ===========================
    # Entrada da Missão (Contexto)
    # ===========================
    def iniciar_missao_contexto(self, image_to_display=None):
        self._limpar_frame()

        tk.Label(
            self.base_content_frame,
            text="Missão 2: Localizando um Infiltrado (Busca Binária)",
            font=self.font_titulo,
            fg=self.cor_titulo,
            bg=self.cor_fundo
        ).pack(pady=(10, 10))

        if image_to_display:
            tk.Label(self.base_content_frame, image=image_to_display, bg=self.cor_fundo).pack(pady=(4, 10))

        contexto = (
            "Fulcrum: \"A Aliança tem um catálogo de agentes Imperiais ordenado por ID. "
            "Sua missão é dominar a BUSCA BINÁRIA para encontrar um infiltrado específico, lidar com duplicatas, "
            "e confirmar rapidamente a existência de agentes em um intervalo de IDs.\""
        )
        tk.Label(
            self.base_content_frame,
            text=contexto,
            wraplength=740,
            justify=tk.LEFT,
            font=self.font_narrativa,
            fg=self.cor_texto,
            bg=self.cor_fundo
        ).pack(pady=8, padx=20)

        ttk.Button(
            self.base_content_frame,
            text="Iniciar Fase 1",
            command=self._iniciar_fase,
            style="Accent.Dark.TButton"
        ).pack(pady=18)

    # ===========================
    # Controle de Fases
    # ===========================
    def _iniciar_fase(self):
        self.low, self.high = 0, len(self.lista_agentes) - 1
        self.mid = None

        if self.etapa_atual == 0:
            # Fase 1: alvo exato
            alvo = random.choice(self.lista_agentes)
            self.target_id = alvo["id"]
            self._montar_tela_busca_binaria(
                titulo=self.etapas_info[0]["titulo"],
                narrativa=self.etapas_info[0]["narrativa"],
                modo="exato"
            )

        elif self.etapa_atual == 1:
            # Fase 2: cria duplicatas artificiais de um ID para exercitar "primeira ocorrência"
            # Pegamos um ID e inserimos cópias consecutivas
            idx = random.randint(10, len(self.lista_agentes) - 10)
            self.target_id_dup = self.lista_agentes[idx]["id"]
            # Duplica o ID (3 ocorrências) mantendo lista ordenada
            bloco = [
                {**self.lista_agentes[idx], "nome": self.lista_agentes[idx]["nome"] + " (dup)"} for _ in range(2)
            ]
            self.lista_agentes = (
                self.lista_agentes[:idx] + bloco + self.lista_agentes[idx:]
            )
            # Reordena por precaução (IDs iguais mantém estabilidade)
            self.lista_agentes = sorted(self.lista_agentes, key=lambda a: a["id"])

            self.low, self.high = 0, len(self.lista_agentes) - 1
            self._montar_tela_busca_binaria(
                titulo=self.etapas_info[1]["titulo"],
                narrativa=self.etapas_info[1]["narrativa"],
                modo="primeira_ocorrencia"
            )

        elif self.etapa_atual == 2:
            # Fase 3: intervalo
            # Definimos um range que com alta chance de existir
            ids = [a["id"] for a in self.lista_agentes]
            pivot = random.choice(ids)
            delta = random.randint(10, 150)
            self.range_min = max(min(ids), pivot - delta)
            self.range_max = min(max(ids), pivot + delta)
            self.low, self.high = 0, len(self.lista_agentes) - 1
            self._montar_tela_busca_intervalo(
                titulo=self.etapas_info[2]["titulo"],
                narrativa=self.etapas_info[2]["narrativa"]
            )

    # ===========================
    # UI das Fases (Busca Binária)
    # ===========================
    def _montar_tela_busca_binaria(self, titulo, narrativa, modo="exato"):
        self._limpar_frame()

        topo = tk.Frame(self.base_content_frame, bg=self.cor_fundo)
        topo.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)

        # Coluna Esquerda: narrativa e controles
        col_esq = tk.Frame(topo, bg=self.cor_fundo, width=720)
        col_esq.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))
        col_esq.pack_propagate(False)

        tk.Label(col_esq, text=titulo, font=self.font_titulo, fg=self.cor_titulo, bg=self.cor_fundo).pack(pady=(4, 8))

        nar = narrativa
        if modo == "exato":
            nar += f"\n\nAlvo (ID): `{self.target_id}`"
        elif modo == "primeira_ocorrencia":
            nar += f"\n\nAlvo (ID duplicado): `{self.target_id_dup}`\nTarefa: retornar o *menor índice* com esse ID."

        tk.Label(
            col_esq, text=nar, wraplength=400, justify=tk.LEFT,
            font=self.font_narrativa, fg=self.cor_texto, bg=self.cor_fundo
        ).pack(pady=8)

        # Painel de intervalo e feedback
        self.label_intervalo = tk.Label(
            col_esq, text="", font=self.font_sub, fg=self.cor_titulo, bg=self.cor_fundo, justify=tk.LEFT
        )
        self.label_intervalo.pack(pady=(6, 2), anchor="w")

        self.label_feedback = tk.Label(
            col_esq, text="", font=self.font_narrativa, fg="yellow", bg=self.cor_fundo, justify=tk.LEFT
        )
        self.label_feedback.pack(pady=(2, 8), anchor="w")

        # Controles de passo da busca
        controls = tk.Frame(col_esq, bg=self.cor_fundo)
        controls.pack(pady=6, anchor="w")

        self.btn_low = ttk.Button(controls, text="Mover HIGH → mid-1", style="Dark.TButton",
                                  command=lambda: self._ajustar_intervalo("esquerda", modo))
        self.btn_direita = ttk.Button(controls, text="Mover LOW → mid+1", style="Dark.TButton",
                                      command=lambda: self._ajustar_intervalo("direita", modo))
        self.btn_encontrado = ttk.Button(controls, text="ENCONTREI (mid == alvo)", style="Accent.Dark.TButton",
                                         command=lambda: self._checar_encontrado(modo))

        # Monta ordem dos botões com espaçamento
        self.btn_low.grid(row=0, column=0, padx=(0, 6), pady=4, sticky="w")
        self.btn_direita.grid(row=0, column=1, padx=(0, 6), pady=4, sticky="w")
        self.btn_encontrado.grid(row=0, column=2, padx=(0, 6), pady=4, sticky="w")

        # Coluna Direita: tabela de IDs com highlight de low/mid/high
        col_dir = tk.Frame(topo, bg=self.cor_fundo)
        col_dir.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scroll
        canvas = tk.Canvas(col_dir, bg=self.cor_fundo, highlightthickness=0)
        scroll = ttk.Scrollbar(col_dir, orient="vertical", command=canvas.yview)
        wrap = tk.Frame(canvas, bg=self.cor_fundo)

        wrap.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=wrap, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)

        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Cabeçalho
        tk.Label(
            wrap, text="Índice | ID | Nome | Posto | Setor",
            font=self.font_sub, fg=self.cor_titulo, bg=self.cor_fundo
        ).pack(anchor="w", padx=6, pady=(0, 4))

        self.labels_linhas = []
        for i, ag in enumerate(self.lista_agentes):
            txt = f"[{i:>3}]  {ag['id']:>6}  | {ag['nome']:<16} | {ag['posto']:<11} | {ag['setor']}"
            lb = tk.Label(wrap, text=txt, font=("Courier New", 12), fg=self.cor_texto, bg=self.cor_fundo, justify=tk.LEFT)
            lb.pack(anchor="w", padx=6)
            self.labels_linhas.append(lb)

        # Botão para avançar automaticamente os passos (calcular mid e mostrar dica)
        ttk.Button(
            col_esq, text="Calcular mid e Dica", style="Dark.TButton",
            command=lambda: self._calcular_mid_e_dica(modo)
        ).pack(pady=(8, 2), anchor="w")

        # Estado inicial
        self._atualizar_intervalo_e_highlight()

    def _montar_tela_busca_intervalo(self, titulo, narrativa):
        self._limpar_frame()

        topo = tk.Frame(self.base_content_frame, bg=self.cor_fundo)
        topo.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)

        col_esq = tk.Frame(topo, bg=self.cor_fundo, width=420)
        col_esq.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))
        col_esq.pack_propagate(False)

        tk.Label(col_esq, text=titulo, font=self.font_titulo, fg=self.cor_titulo, bg=self.cor_fundo).pack(pady=(4, 8))
        nar = f"{narrativa}\n\nIntervalo sugerido: [{self.range_min}, {self.range_max}]"
        tk.Label(
            col_esq, text=nar, wraplength=400, justify=tk.LEFT,
            font=self.font_narrativa, fg=self.cor_texto, bg=self.cor_fundo
        ).pack(pady=8)

        frm = tk.Frame(col_esq, bg=self.cor_fundo)
        frm.pack(pady=(4, 6), anchor="w")
        tk.Label(frm, text="Mín:", font=self.font_sub, fg=self.cor_titulo, bg=self.cor_fundo).grid(row=0, column=0, sticky="w", padx=(0, 6))
        self.entry_min = ttk.Entry(frm, width=12)
        self.entry_min.grid(row=0, column=1, sticky="w", padx=(0, 8))
        self.entry_min.insert(0, str(self.range_min))

        tk.Label(frm, text="Máx:", font=self.font_sub, fg=self.cor_titulo, bg=self.cor_fundo).grid(row=0, column=2, sticky="w", padx=(0, 6))
        self.entry_max = ttk.Entry(frm, width=12)
        self.entry_max.grid(row=0, column=3, sticky="w")
        self.entry_max.insert(0, str(self.range_max))

        self.label_feedback = tk.Label(
            col_esq, text="", font=self.font_narrativa, fg="yellow", bg=self.cor_fundo, justify=tk.LEFT
        )
        self.label_feedback.pack(pady=(6, 8), anchor="w")

        ttk.Button(
            col_esq, text="Verificar Existência no Intervalo", style="Accent.Dark.TButton",
            command=self._verificar_intervalo
        ).pack(pady=6, anchor="w")

        ttk.Button(
            col_esq, text="Tabela Completa", style="Dark.TButton",
            command=self._abrir_tabela_completa
        ).pack(pady=(6, 2), anchor="w")

        # Direita — resumo rápido
        col_dir = tk.Frame(topo, bg=self.cor_fundo)
        col_dir.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tk.Label(
            col_dir, text="Dica:\nUse duas buscas binárias para encontrar:\n"
                          "- lower_bound (primeiro >= min)\n"
                          "- upper_bound (primeiro > max)\n"
                          "Existe ID no intervalo se lower < upper.",
            justify=tk.LEFT, fg=self.cor_texto, bg=self.cor_fundo, font=self.font_narrativa
        ).pack(anchor="w", padx=6, pady=6)

    # ===========================
    # Lógica de Busca Binária (F1/F2)
    # ===========================
    def _calcular_mid_e_dica(self, modo):
        if self.low > self.high:
            self.label_feedback.config(text="R7-X: Intervalo esgotado! Reinicie a fase.")
            self.game_manager.add_score(-20)
            return

        self.mid = (self.low + self.high) // 2
        mid_id = self.lista_agentes[self.mid]["id"]

        if modo == "exato":
            alvo = self.target_id
            if mid_id == alvo:
                dica = "mid == alvo ➜ clique em ENCONTREI."
            elif mid_id > alvo:
                dica = "mid > alvo ➜ ajuste para ESQUERDA (high = mid - 1)."
            else:
                dica = "mid < alvo ➜ ajuste para DIREITA (low = mid + 1)."

        elif modo == "primeira_ocorrencia":
            alvo = self.target_id_dup
            if mid_id >= alvo:
                dica = (
                    "mid_id >= alvo ➜ para achar a PRIMEIRA ocorrência, "
                    "mova para a ESQUERDA (high = mid - 1). "
                    "Quando mid == alvo, só finalize se confirmar que é o primeiro."
                )
            else:
                dica = "mid_id < alvo ➜ mova para a DIREITA (low = mid + 1)."

        else:
            dica = "Modo desconhecido."

        self.game_manager.add_score(+2)  # pequeno incentivo por passo correto
        self.label_feedback.config(text=f"Dica (mid={self.mid}, id={mid_id}): {dica}")
        self._atualizar_intervalo_e_highlight()

    def _ajustar_intervalo(self, direcao, modo):
        if self.mid is None:
            self.label_feedback.config(text="R7-X: Calcule o mid primeiro (botão 'Calcular mid e Dica').")
            return

        mid_id = self.lista_agentes[self.mid]["id"]

        if direcao == "esquerda":
            # high = mid - 1
            self.high = self.mid - 1
            self.game_manager.add_score(+1)
            self.label_feedback.config(text=f"R7-X: Ajuste para ESQUERDA (high ← {self.high}).")
        elif direcao == "direita":
            # low = mid + 1
            self.low = self.mid + 1
            self.game_manager.add_score(+1)
            self.label_feedback.config(text=f"R7-X: Ajuste para DIREITA (low → {self.low}).")
        else:
            return

        self.mid = None
        self._atualizar_intervalo_e_highlight()

    def _checar_encontrado(self, modo):
        if self.mid is None:
            self.label_feedback.config(text="R7-X: Calcule o mid primeiro antes de confirmar.")
            return

        mid_id = self.lista_agentes[self.mid]["id"]

        if modo == "exato":
            if mid_id == self.target_id:
                self.game_manager.add_score(+40)
                self._finalizar_ou_proxima_fase(sucesso=True, msg=(
                    f"Registro encontrado! ID={mid_id}. Avançando."
                ))
            else:
                self.game_manager.add_score(-10)
                self.label_feedback.config(text=f"R7-X: mid ({mid_id}) != alvo ({self.target_id}). Continue a busca.")
        elif modo == "primeira_ocorrencia":
            alvo = self.target_id_dup
            if mid_id == alvo:
                # Validar se é a primeira ocorrência (menor índice com esse ID)
                is_primeiro = (self.mid == 0) or (self.lista_agentes[self.mid - 1]["id"] < alvo)
                if is_primeiro:
                    self.game_manager.add_score(+50)
                    self._finalizar_ou_proxima_fase(
                        sucesso=True,
                        msg=f"Primeira ocorrência confirmada em índice {self.mid} (ID={alvo})."
                    )
                else:
                    self.game_manager.add_score(-8)
                    self.label_feedback.config(
                        text="R7-X: Esse não é o primeiro. Há o mesmo ID antes. Ajuste para ESQUERDA."
                    )
            else:
                self.game_manager.add_score(-10)
                self.label_feedback.config(
                    text=f"R7-X: mid ({mid_id}) != alvo ({alvo}). Ajuste conforme a dica."
                )

    def _atualizar_intervalo_e_highlight(self):
        # Atualiza label de intervalo
        self.label_intervalo.config(text=f"[low={self.low}  high={self.high}]")

        # Apaga destaques
        for i, lb in enumerate(getattr(self, "labels_linhas", [])):
            lb.config(bg=self.cor_fundo)

        # Destaca low, high e mid
        if hasattr(self, "labels_linhas"):
            if 0 <= self.low < len(self.labels_linhas):
                self.labels_linhas[self.low].config(bg="#203040")
            if 0 <= self.high < len(self.labels_linhas):
                self.labels_linhas[self.high].config(bg="#402030")
            if self.mid is not None and 0 <= self.mid < len(self.labels_linhas):
                self.labels_linhas[self.mid].config(bg="#2A402A")

        # Checa exaustão
        if self.low > self.high:
            self.game_manager.add_score(-25)
            messagebox.showerror("Intervalo esgotado", "Busca fracassou. O intervalo ficou inválido (low > high).")
            self.retry_mission()

    # ===========================
    # Lógica Fase 3 (Intervalo)
    # ===========================
    def _verificar_intervalo(self):
        try:
            a = int(self.entry_min.get().strip())
            b = int(self.entry_max.get().strip())
        except Exception:
            self.label_feedback.config(text="R7-X: Intervalo inválido. Use inteiros.")
            return

        if a > b:
            a, b = b, a

        ids = [ag["id"] for ag in self.lista_agentes]

        def lower_bound(arr, x):
            lo, hi = 0, len(arr)
            while lo < hi:
                mid = (lo + hi) // 2
                if arr[mid] < x:
                    lo = mid + 1
                else:
                    hi = mid
            return lo

        def upper_bound(arr, x):
            lo, hi = 0, len(arr)
            while lo < hi:
                mid = (lo + hi) // 2
                if arr[mid] <= x:
                    lo = mid + 1
                else:
                    hi = mid
            return lo

        lb = lower_bound(ids, a)
        ub = upper_bound(ids, b)
        existe = lb < ub

        if existe:
            self.game_manager.add_score(+40)
            self._finalizar_ou_proxima_fase(
                sucesso=True,
                msg=f"Há agentes com ID no intervalo [{a}, {b}]. Exemplos próximos: índice {lb} (ID={ids[lb]})."
            )
        else:
            self.game_manager.add_score(-10)
            self.label_feedback.config(text=f"Nenhum ID no intervalo [{a}, {b}]. Tente outro intervalo.")

    # ===========================
    # Fluxo de Finalização/Retry
    # ===========================
    def _finalizar_ou_proxima_fase(self, sucesso, msg=""):
        if msg:
            self.label_feedback.config(text=msg)

        self.etapa_atual += 1
        if self.etapa_atual < len(self.etapas_info):
            # Avança para próxima fase
            self.root.after(1500, self._iniciar_fase)
        else:
            # Missão concluída
            self.root.after(1200, self._finalizar_missao)

    def _finalizar_missao(self):
        self._limpar_frame()
        tk.Label(
            self.base_content_frame,
            text="Missão 2 Concluída!",
            font=self.font_titulo,
            fg="green",
            bg=self.cor_fundo
        ).pack(pady=(10, 12))

        resumo = (
            "Você localizou o infiltrado com busca binária, confirmou a PRIMEIRA ocorrência em listas com duplicatas "
            "e validou a existência de IDs dentro de um intervalo usando limites inferiores e superiores.\n"
            "A Aliança está um passo à frente graças à sua precisão."
        )
        tk.Label(
            self.base_content_frame, text=resumo, wraplength=740, justify=tk.CENTER,
            font=self.font_narrativa, fg=self.cor_texto, bg=self.cor_fundo
        ).pack(pady=10, padx=20)

        ttk.Button(
            self.base_content_frame,
            text="Continuar",
            command=lambda: self.game_manager.mission_completed("Missao2"),
            style="Accent.Dark.TButton"
        ).pack(pady=18)

        ttk.Button(
            self.base_content_frame,
            text="Tabela Completa de Agentes",
            command=self._abrir_tabela_completa,
            style="Dark.TButton"
        ).pack()

    def _abrir_tabela_completa(self):
        top = tk.Toplevel(self.root)
        top.title("Catálogo Completo — Agentes Imperiais (Ordenado por ID)")
        top.geometry("740x720")
        top.configure(bg=self.cor_fundo)

        frame = tk.Frame(top, bg=self.cor_fundo)
        frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(frame, bg=self.cor_fundo, highlightthickness=0)
        scroll = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        wrap = tk.Frame(canvas, bg=self.cor_fundo)

        wrap.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=wrap, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)

        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(
            wrap, text="Índice | ID | Nome | Posto | Setor",
            font=self.font_sub, fg=self.cor_titulo, bg=self.cor_fundo
        ).pack(anchor="w", padx=6, pady=(4, 6))

        for i, ag in enumerate(self.lista_agentes):
            txt = f"[{i:>3}]  {ag['id']:>6}  | {ag['nome']:<16} | {ag['posto']:<11} | {ag['setor']}"
            tk.Label(wrap, text=txt, font=("Courier New", 12), fg=self.cor_texto, bg=self.cor_fundo, justify=tk.LEFT)\
                .pack(anchor="w", padx=6)

    def retry_mission(self):
        # Reinicia para a fase atual (ou recomeça do zero, se preferir)
        self.low, self.high, self.mid = 0, len(self.lista_agentes) - 1, None
        self.game_manager.set_game_state("START_MISSION_2")
