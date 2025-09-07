# missoes_busca/missao1.py
import tkinter as tk
from tkinter import ttk, messagebox, font as tkFont
import random
from BancoDados.dados_hangar import CATALOGO_HANGAR

class Missao1:
    def __init__(self, root, game_manager, content_frame):
        self.root = root
        self.game_manager = game_manager
        self.base_content_frame = content_frame

        self.etapas_info = [
            {"titulo": "Fase 1: O Ponto de Partida", "narrativa": "Fulcrum: Comandante, um informante nos enviou um código de contêiner que contém as coordenadas para uma operação vital. No entanto, o Império misturou o contêiner em um hangar enorme. Você precisará inspecionar o contêiner de carga um por um, na ordem em que eles aparecem, até encontrar o que buscamos. O código de registro que você procura é: ", "alvo_tipo": "id"},
            {"titulo": "Fase 2: A Chave Oculta", "narrativa": "R7-X: O primeiro contêiner não continha as coordenadas diretamente, mas sim um mapa estelar codificado. Use a descrição do mapa para localizar o próximo contêiner na sequência, que é o nosso próximo passo para decifrar as coordenadas. O item que você procura tem a seguinte descrição: ", "alvo_tipo": "conteudo"},
            {"titulo": "Fase 3: A Carga Vital", "narrativa": "R7-X: Os dados do mapa apontam para um último contêiner. Este, de acordo com o informante, guarda o verdadeiro item de contrabando. Prossiga com a busca sequencial e garanta a carga. O código de registro é: ", "alvo_tipo": "id"}
        ]
        self.etapa_atual = 0
        
        self.catalogo_missao = []
        self.alvo_atual = None
        self.indice_busca = 0

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
            "Fulcrum: Comandante, temos um relatório urgente. Suspeitamos que um carregamento ilegal "
            "de detonadores térmicos foi escondido em um dos contêineres do nosso hangar. O Império "
            "costuma camuflar esses itens em grandes remessas. Sua missão é inspecionar cada contêiner, "
            "um por um, até localizar o contrabando. A busca sequencial é a única maneira de garantir que "
            "não perderemos o alvo."
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
            text="Iniciar Inspeção",
            command=self.iniciar_etapa,
            style="Accent.Dark.TButton"
        ).pack(pady=20)

    def iniciar_etapa(self):
        if self.etapa_atual == 0:
            self.catalogo_missao = random.sample(CATALOGO_HANGAR, 15)
            self.alvo_fase_1 = random.choice(self.catalogo_missao)
            self.alvo_fase_2 = {'id': 'S-C-1138', 'conteudo': 'Mapa Estelar Codificado'}
            self.alvo_final = {'id': 'CONTRABANDO-1138', 'conteudo': 'Detonadores Térmicos'}
            
            # Adiciona os alvos no catálogo de forma que a busca sequencial seja necessária
            self.catalogo_missao.append(self.alvo_fase_1)
            self.catalogo_missao.append(self.alvo_fase_2)
            self.catalogo_missao.append(self.alvo_final)

            random.shuffle(self.catalogo_missao)

        self._montar_tela_busca()

    def _montar_tela_busca(self):
        self._limpar_frame()
        etapa = self.etapas_info[self.etapa_atual]
        
        main_frame = tk.Frame(self.base_content_frame, bg=self.cor_fundo)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        info_frame = tk.Frame(main_frame, bg=self.cor_fundo, width=400)
        info_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        info_frame.pack_propagate(False)

        hangar_frame = tk.Frame(main_frame, bg=self.cor_fundo)
        hangar_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(
            info_frame,
            text=etapa["titulo"],
            font=self.font_titulo,
            fg=self.cor_titulo,
            bg=self.cor_fundo
        ).pack(pady=(10, 15))

        if self.etapa_atual == 0:
            self.alvo_atual = self.alvo_fase_1['id']
            narrativa_extra = f"O código de registro que você procura é: `{self.alvo_atual}`."
        elif self.etapa_atual == 1:
            self.alvo_atual = self.alvo_fase_2['conteudo']
            narrativa_extra = f"A descrição que você procura é: `{self.alvo_atual}`."
        elif self.etapa_atual == 2:
            self.alvo_atual = self.alvo_final['id']
            narrativa_extra = f"O código de registro final é: `{self.alvo_atual}`."

        self.label_narrativa = tk.Label(
            info_frame,
            text=etapa["narrativa"] + narrativa_extra,
            wraplength=380,
            justify=tk.LEFT,
            font=self.font_narrativa,
            fg=self.cor_texto,
            bg=self.cor_fundo
        )
        self.label_narrativa.pack(pady=10, padx=10)
        
        ttk.Button(
            info_frame,
            text="Tabela Completa do Hangar",
            command=self._abrir_janela_hangar,
            style="Dark.TButton"
        ).pack(pady=10)

        self.label_feedback = tk.Label(
            info_frame,
            text="",
            font=self.font_narrativa,
            fg="yellow",
            bg=self.cor_fundo
        )
        self.label_feedback.pack(pady=10)
        
        # Cria a área de rolagem para os contêineres
        canvas = tk.Canvas(hangar_frame, bg=self.cor_fundo, highlightthickness=0)
        scrollbar = ttk.Scrollbar(hangar_frame, orient="vertical", command=canvas.yview)
        self.container_frame = tk.Frame(canvas, bg=self.cor_fundo)

        self.container_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.container_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.botoes_contaners = []
        for i, item in enumerate(self.catalogo_missao):
            btn = ttk.Button(
                self.container_frame,
                text=f"Inspecionar Contêiner [{i}]",
                command=lambda idx=i: self._verificar_item(idx),
                style="Dark.TButton"
            )
            btn.pack(side=tk.TOP, padx=5, pady=2, fill=tk.X)
            self.botoes_contaners.append(btn)
    
    def _verificar_item(self, indice_clicado):
        item_inspecionado = self.catalogo_missao[indice_clicado]
        
        # Simula a busca sequencial
        if indice_clicado != self.indice_busca:
            self.game_manager.add_score(-5)
            self.label_feedback.config(text="R7-X: Inspeção fora de ordem! Mantenha a sequência.")
            return

        self.botoes_contaners[indice_clicado].config(state="disabled")
        
        encontrado = False
        if self.etapa_atual == 0:
            if item_inspecionado['id'] == self.alvo_fase_1['id']:
                encontrado = True
        elif self.etapa_atual == 1:
            if item_inspecionado['conteudo'] == self.alvo_fase_2['conteudo']:
                encontrado = True
        elif self.etapa_atual == 2:
            if item_inspecionado['id'] == self.alvo_final['id']:
                encontrado = True

        if encontrado:
            self.game_manager.add_score(50)
            self.label_feedback.config(text=f"R7-X: Item da Fase {self.etapa_atual + 1} encontrado! Avançando para a próxima fase.")
            
            self.etapa_atual += 1
            self.indice_busca = 0
            if self.etapa_atual < len(self.etapas_info):
                self.root.after(2000, self.iniciar_etapa)
            else:
                self.root.after(2000, self._finalizar_missao)
        else:
            self.label_feedback.config(text=f"R7-X: Contêiner [{indice_clicado}] inspecionado. Nenhum item chave. Continue a busca sequencial.")
            self.indice_busca += 1
            if self.indice_busca >= len(self.catalogo_missao):
                self.game_manager.add_score(-100)
                messagebox.showerror("Missão Falhou!", "O item não foi encontrado. Todos os contêineres foram inspecionados sem sucesso.")
                self.retry_mission()

    def _finalizar_missao(self):
        self._limpar_frame()
        tk.Label(
            self.base_content_frame,
            text="Missão Concluída!",
            font=self.font_titulo,
            fg="green",
            bg=self.cor_fundo
        ).pack(pady=(10, 15))

        tk.Label(
            self.base_content_frame,
            text="O contrabando foi interceptado com sucesso! Suas habilidades analíticas salvaram a Aliança de um grande perigo. As coordenadas foram recuperadas e uma nova rota de suprimentos foi estabelecida.",
            wraplength=700,
            justify=tk.CENTER,
            font=self.font_narrativa,
            fg=self.cor_texto,
            bg=self.cor_fundo
        ).pack(pady=10)
        
        ttk.Button(
            self.base_content_frame,
            text="Continuar",
            command=lambda: self.game_manager.mission_completed("Missao1"),
            style="Accent.Dark.TButton"
        ).pack(pady=20)

    def _abrir_janela_hangar(self):
        nova_janela = tk.Toplevel(self.root)
        nova_janela.title("Tabela Completa do Hangar")
        nova_janela.geometry("600x800")
        nova_janela.configure(bg=self.cor_fundo)
        
        frame_scroll = tk.Frame(nova_janela, bg=self.cor_fundo)
        frame_scroll.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(frame_scroll, bg=self.cor_fundo, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.cor_fundo)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(scrollable_frame, text="Índice | ID do Contêiner | Conteúdo", font=self.font_subtitulo, fg=self.cor_titulo, bg=self.cor_fundo).pack(fill=tk.X, anchor="w", padx=5)
        
        for i, item in enumerate(CATALOGO_HANGAR):
            label_texto = f"[{i:^5}]  {item['id']:^15}  {item['conteudo']}"
            tk.Label(scrollable_frame, text=label_texto, font=("Courier New", 12), fg=self.cor_texto, bg=self.cor_fundo, justify=tk.LEFT).pack(fill=tk.X, anchor="w", padx=5)

    def retry_mission(self):
        self.etapa_atual = 0
        self.game_manager.set_game_state("START_MISSION_1")