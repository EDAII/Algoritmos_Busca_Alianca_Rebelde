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
            {"titulo": "Fase 1: A Chave Principal", "narrativa": "Fulcrum: Comandante, um informante nos enviou um código de contêiner que contém as coordenadas para uma operação vital. No entanto, o Império misturou o contêiner em um hangar enorme. Você precisará inspecionar o contêiner de carga um por um, na ordem em que eles aparecem, até encontrar o que buscamos. O código de registro que você procura é: ", "alvo_tipo": "id"},
            {"titulo": "Fase 2: Otimizando a Lista", "narrativa": "R7-X: A busca foi bem-sucedida, mas poderíamos ter sido mais rápidos. Agora, prevemos que uma nova mensagem vital esteja em um contêiner recém-adicionado. Para economizar tempo, reorganizaremos os dados. Qual método você prefere?", "alvo_tipo": "id"},
            {"titulo": "Fase 3: Busca Indexada", "narrativa": "R7-X: Agora estamos lidando com um catálogo massivo de contêineres. Fazer uma busca sequencial completa seria ineficiente. A Aliança preparou uma tabela de índices para agilizar o processo. Encontre o índice correto para o bloco de contêineres, e então comece sua busca."}
        ]
        self.etapa_atual = 0
        
        self.catalogo_missao = []
        self.tabela_indices = []
        self.alvo_atual = None
        self.indice_busca = 0
        self.alvo_fase_1 = None
        self.alvo_fase_2 = None
        self.alvo_final = None
        
        self.index_size = 10 # Tamanho do índice para a Fase 3

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

    def iniciar_missao_contexto(self, image_to_display=None):
        self._limpar_frame()
        tk.Label(
            self.base_content_frame,
            text="Missão 1: Inspeção no Hangar de Carga",
            font=self.font_titulo,
            fg=self.cor_titulo,
            bg=self.cor_fundo
        ).pack(pady=(10, 15))
        
        if image_to_display:
            imagem_label = tk.Label(self.base_content_frame, image=image_to_display, bg=self.cor_fundo)
            imagem_label.pack(pady=(10, 10))

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
        self.indice_busca = 0
        
        if self.etapa_atual == 0:
            self.catalogo_missao = random.sample(CATALOGO_HANGAR, 20)
            self.alvo_fase_1 = random.choice(self.catalogo_missao)
            self.alvo_fase_2 = {'id': 'S-C-1138', 'conteudo': 'Mapa Estelar Codificado'}
            self.alvo_final = {'id': 'CONTRABANDO-1138', 'conteudo': 'Detonadores Térmicos'}
            
            # Garante que os alvos estão na lista
            if self.alvo_fase_1 not in self.catalogo_missao:
                self.catalogo_missao.append(self.alvo_fase_1)
            if self.alvo_fase_2 not in self.catalogo_missao:
                self.catalogo_missao.append(self.alvo_fase_2)
            if self.alvo_final not in self.catalogo_missao:
                self.catalogo_missao.append(self.alvo_final)
            
            random.shuffle(self.catalogo_missao)
            self.alvo_atual = self.alvo_fase_1['id']
            self._montar_tela_busca()
        
        elif self.etapa_atual == 1:
            self.alvo_atual = self.alvo_fase_2['conteudo']
            self._montar_tela_busca()

        elif self.etapa_atual == 2:
            self.catalogo_missao = sorted(random.sample(CATALOGO_HANGAR, 400), key=lambda x: x['id'])
            
            # Cria a tabela de índices
            self.tabela_indices = self._criar_tabela_indices()
            
            # Garante que o alvo final esteja em uma posição conhecida
            indice_pista = random.randint(0, self.index_size - 1)
            posicao_inicial = self.tabela_indices[indice_pista]['posicao']
            posicao_alvo = posicao_inicial + 8
            if posicao_alvo >= len(self.catalogo_missao):
                posicao_alvo = len(self.catalogo_missao) - 1
                
            self.alvo_final = self.catalogo_missao[posicao_alvo]
            
            self.alvo_atual = self.alvo_final['id']
            self._montar_tela_busca(pista_id=self.tabela_indices[indice_pista]['id'])

    def _criar_tabela_indices(self):
        tabela = []
        passo = len(self.catalogo_missao) // self.index_size
        for i in range(self.index_size):
            indice = i * passo
            tabela.append({'id': self.catalogo_missao[indice]['id'], 'posicao': indice})
        return tabela

    def _montar_tela_busca(self, pista_id=None):
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

        narrativa_principal = etapa["narrativa"]
        narrativa_extra = ""
        
        if self.etapa_atual == 0:
            narrativa_extra = f"\n\nO código de registro que você procura é: `{self.alvo_fase_1['id']}`."
        elif self.etapa_atual == 1:
            narrativa_extra = f"\n\nA descrição que você procura é: `{self.alvo_fase_2['conteudo']}`."
            ttk.Button(info_frame, text="Mover-para-Frente", command=self._reorganizar_mover_frente, style="Accent.Dark.TButton").pack(pady=5)
            ttk.Button(info_frame, text="Transposição", command=self._reorganizar_transposicao, style="Accent.Dark.TButton").pack(pady=5)
        elif self.etapa_atual == 2:
            narrativa_extra = f"\n\nO código de registro final é: `{self.alvo_final['id']}`."
            
            if pista_id:
                narrativa_extra += f"\n\nR7-X: Com base nas últimas interceptações, a chave que você procura deve estar em um bloco de contêineres que começa com o ID `{pista_id}`. Clique no índice correspondente para iniciar sua busca."
            
            tk.Label(info_frame, text="Tabela de Índices:", font=self.font_subtitulo, fg=self.cor_titulo, bg=self.cor_fundo).pack(pady=(10, 5))
            for i, indice in enumerate(self.tabela_indices):
                ttk.Button(info_frame, text=f"Índice {i}: {indice['id']}", command=lambda pos=indice['posicao']: self._iniciar_busca_indexada(pos), style="Dark.TButton").pack(pady=2, fill=tk.X)


        self.label_narrativa = tk.Label(
            info_frame,
            text=narrativa_principal + narrativa_extra,
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

    def _reorganizar_mover_frente(self):
        # Mover para frente (não implementado, apenas para simulação)
        pass
        messagebox.showinfo("Método Mover-para-Frente", "A lista de contêineres foi reorganizada! Continue a busca.")
        self.iniciar_etapa()

    def _reorganizar_transposicao(self):
        # Transposição (não implementado, apenas para simulação)
        pass
        messagebox.showinfo("Método de Transposição", "A lista de contêineres foi reorganizada! Continue a busca.")
        self.iniciar_etapa()
    
    def _iniciar_busca_indexada(self, inicio_busca):
        self.indice_busca = inicio_busca
        messagebox.showinfo("Busca Indexada", f"Iniciando busca a partir do índice {inicio_busca}. Agora use a busca sequencial.")

    def _verificar_item(self, indice_clicado):
        item_inspecionado = self.catalogo_missao[indice_clicado]
        
        # Valida a busca sequencial
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