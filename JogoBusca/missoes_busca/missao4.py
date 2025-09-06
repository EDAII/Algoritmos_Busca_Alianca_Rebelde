# missoes_busca/missao4.py
import tkinter as tk
from tkinter import ttk, messagebox, font as tkFont
import random
from algoritmos_busca.hashing_busca import *
from BancoDados.dados_naves import BANCO_DE_DADOS_GRANDE, BANCO_DE_DADOS_PEQUENO, gerar_chaves_com_colisao, gerar_especificacoes_nave, gerar_catalogo_naves, encontrar_chaves_em_colisao_no_banco

class Missao4:
    def __init__(self, root, game_manager, content_frame):
        self.root = root
        self.game_manager = game_manager
        self.base_content_frame = content_frame

        self.etapas_info = [
            {"titulo": "Fase 1: Análise do Hash Primário"}
        ]
        self.etapa_atual = 0
        
        self.tamanho_tabela_hash = 101
        self.tamanho_tabela_simulacao = 44
        
        self.chave_alvo = ""
        self.dados_etapa = {}
        
        self.tabela_container = None
        self.tabela_canvas = None
        self.scrollable_frame = None
        self._widgets_tabela = []
        
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
        tk.Label(self.base_content_frame, text="Operação HASH-1138: Decifrando o Catálogo da Frota", font=self.font_titulo, fg=self.cor_titulo, bg=self.cor_fundo).pack(pady=(10, 15))
        contexto = "Fulcrum: Comandante, interceptamos um catálogo da frota Imperial de uma base de suprimentos em Ryloth. Os arquivos não estão em ordem, mas o Império os organiza usando uma técnica de 'hashing' para acesso rápido. Nossa missão é reverter o processo para encontrar as especificações de naves de carga que a Aliança precisa desesperadamente. O droide de protocolo R7-X irá guiar você através dos protocolos Imperiais."
        tk.Label(self.base_content_frame, text=contexto, wraplength=700, justify=tk.LEFT, font=self.font_narrativa, fg=self.cor_texto, bg=self.cor_fundo).pack(pady=10, padx=20)
        ttk.Button(self.base_content_frame, text="Iniciar Análise de Hashing...", command=lambda: self.iniciar_etapa(0), style="Accent.Dark.TButton").pack(pady=20)

    def iniciar_etapa(self, etapa_numero):
        self.etapa_atual = etapa_numero
        
        if self.etapa_atual == 0:
            self._gerar_dados_missao()

        self._limpar_frame()
        etapa_info = self.etapas_info[self.etapa_atual]
        tk.Label(self.base_content_frame, text=etapa_info["titulo"], font=self.font_titulo, fg=self.cor_titulo, bg=self.cor_fundo).pack(pady=(10, 15))

        if etapa_numero == 0:
            self.fase_1_encontrando_bucket()

    def _gerar_dados_missao(self):
        # Encontra chaves que colidem no banco de dados grande
        chaves_exemplo = encontrar_chaves_em_colisao_no_banco(BANCO_DE_DADOS_GRANDE, self.tamanho_tabela_simulacao, num_colisoes=2)
        
        if len(chaves_exemplo) < 2:
            # Fallback caso não encontre colisão no banco grande
            chaves_exemplo = gerar_chaves_com_colisao(self.tamanho_tabela_simulacao, num_colisoes=2)

        self.chave_alvo = random.choice(chaves_exemplo)['chave']
        
        self.dados_etapa['catalogo_pequeno_cheio'] = construir_tabela_hash_encadeamento(BANCO_DE_DADOS_PEQUENO, self.tamanho_tabela_simulacao)
        
        for item in chaves_exemplo:
            indice_colisao = hashing_divisao(item['chave'], self.tamanho_tabela_simulacao)
            self.dados_etapa['catalogo_pequeno_cheio'][indice_colisao].append(item)

    def _criar_visualizacao_tabela_in_frame(self, parent_frame, tabela, on_click_callback=None):
        tabela_canvas = tk.Canvas(parent_frame, bg=self.cor_fundo, highlightthickness=0, width=250, height=400)
        tabela_scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=tabela_canvas.yview)
        scrollable_frame = tk.Frame(tabela_canvas, bg=self.cor_fundo)

        scrollable_frame.bind("<Configure>", lambda e: tabela_canvas.configure(scrollregion=tabela_canvas.bbox("all")))
        tabela_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        tabela_canvas.configure(yscrollcommand=tabela_scrollbar.set)
        
        tabela_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tabela_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._widgets_tabela = []
        for i, bucket in enumerate(tabela):
            if isinstance(bucket, dict):
                item_texto = bucket['chave']
            elif isinstance(bucket, list):
                item_texto = f"Lista ({len(bucket)})"
            elif bucket is None:
                item_texto = "Vazio"
            else:
                item_texto = "Erro!"

            idx_label = tk.Label(scrollable_frame, text=f"[{i}]", font=("Courier New", 10, "bold"), fg=self.cor_texto, bg=self.cor_fundo)
            idx_label.grid(row=i, column=0, padx=5, pady=2, sticky="W")
            
            if on_click_callback:
                btn_bucket = ttk.Button(scrollable_frame, text=item_texto, style="Dark.TButton", command=lambda idx=i: on_click_callback(idx, tabela[idx]))
                btn_bucket.grid(row=i, column=1, padx=5, pady=2, sticky="W")
                self._widgets_tabela.append(btn_bucket)
            else:
                lbl_bucket = tk.Label(scrollable_frame, text=item_texto, font=("Courier New", 10), fg=self.cor_texto, bg="#222")
                lbl_bucket.grid(row=i, column=1, padx=5, pady=2, sticky="W")
                self._widgets_tabela.append(lbl_bucket)
        
        self.tabela_frame = parent_frame

    def _criar_tabela_ascii_na_tela(self, parent_frame):
        tabela_canvas = tk.Canvas(parent_frame, bg=self.cor_fundo, highlightthickness=0, width=250, height=400)
        tabela_scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=tabela_canvas.yview)
        scrollable_frame = tk.Frame(tabela_canvas, bg=self.cor_fundo)

        scrollable_frame.bind("<Configure>", lambda e: tabela_canvas.configure(scrollregion=canvas.bbox("all")))
        tabela_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        tabela_canvas.configure(yscrollcommand=tabela_scrollbar.set)
        
        tabela_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tabela_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(scrollable_frame, text="Caractere | Valor ASCII", font=self.font_subtitulo, fg=self.cor_titulo, bg=self.cor_fundo).pack(fill=tk.X, anchor="w", padx=5)
        
        for i in range(32, 127):
            char = chr(i)
            valor = i
            label_texto = f"   '{char:^4}'   |    {valor:^5}"
            tk.Label(scrollable_frame, text=label_texto, font=("Courier New", 12), fg=self.cor_texto, bg=self.cor_fundo, justify=tk.LEFT).pack(fill=tk.X, anchor="w", padx=5)

    def _mostrar_dica_extra_fase1(self):
        dica = f"R7-X: Lembre-se, o valor ASCII da sua chave `{self.chave_alvo}` é a soma de cada um dos quatro caracteres. Use a Tabela ASCII para encontrar cada valor."
        messagebox.showinfo("Dica Extra de Hashing", dica)
        self.game_manager.add_score(-10)

    def _calcular_modulo_com_passos(self):
        try:
            valores = [int(e.get()) for e in self.entrada_ascii if e.get()]
            if len(valores) != 4:
                messagebox.showerror("Erro de Cálculo", "Por favor, insira 4 valores ASCII.")
                return

            soma = sum(valores)
            resultado = soma % self.tamanho_tabela_simulacao
            
            passos = "Passos do cálculo:\n"
            passos += " + ".join(map(str, valores)) + f" = {soma}\n"
            passos += f"{soma} % {self.tamanho_tabela_simulacao} = {resultado}"
            
            self.resultado_calculo_label.config(text=passos, justify=tk.LEFT)
        except ValueError:
            messagebox.showerror("Erro de Cálculo", "Por favor, insira apenas números inteiros.")

    def validar_fase_1(self, indice_clicado, item_bucket):
        indice_correto = hashing_divisao(self.chave_alvo, self.tamanho_tabela_simulacao)
        if indice_clicado == indice_correto:
            self.game_manager.add_score(100)
            
            if isinstance(item_bucket, list) and len(item_bucket) > 1:
                self.mostrar_lista_colisao(item_bucket)
            else:
                self.finalizar_missao()

        else:
            self.game_manager.add_score(-50)
            messagebox.showerror("Missão Falhou!", "Bucket incorreto! Tente novamente.")

    def mostrar_lista_colisao(self, lista_naves):
        self._limpar_frame()
        tk.Label(self.base_content_frame, text="Colisão Detectada! O arquivo está em uma lista de colisões.", font=self.font_titulo, fg=self.cor_titulo, bg=self.cor_fundo).pack(pady=(10, 15))
        
        narrativa = "R7-X: Conforme os protocolos Imperiais, o arquivo que você procura está 'encadeado' a outros. Encontre o arquivo com o código de registro que buscamos e selecione-o para finalizar a missão!"
        tk.Label(self.base_content_frame, text=narrativa, wraplength=700, justify=tk.LEFT, font=self.font_narrativa, fg=self.cor_texto, bg=self.cor_fundo).pack(pady=10, padx=20)
        
        for nave in lista_naves:
            ttk.Button(self.base_content_frame, text=nave['chave'], command=lambda chave=nave['chave']: self.validar_nave_colisao(chave), style="Accent.Dark.TButton").pack(pady=5)
            
        ttk.Button(self.base_content_frame, text="Voltar", command=self.retry_mission, style="Dark.TButton").pack(pady=20)

    def validar_nave_colisao(self, chave_clicada):
        if chave_clicada == self.chave_alvo:
            self.game_manager.add_score(50)
            messagebox.showinfo("Sucesso!", "Nave correta encontrada! Transmitindo dados...")
            self.finalizar_missao()
        else:
            self.game_manager.add_score(-25)
            messagebox.showerror("Missão Falhou!", "Nave incorreta! Tente novamente.")

    def fase_1_encontrando_bucket(self):
        main_frame = tk.Frame(self.base_content_frame, bg=self.cor_fundo)
        main_frame.pack(expand=True, fill='both')

        tabelas_frame = tk.Frame(main_frame, bg=self.cor_fundo)
        tabelas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        tabela_arquivos_frame = tk.Frame(tabelas_frame, bg=self.cor_fundo)
        tabela_arquivos_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        tk.Label(tabela_arquivos_frame, text="Tabela de Arquivos", font=self.font_subtitulo, fg=self.cor_titulo, bg=self.cor_fundo).pack(pady=(0, 5))
        tabela_visual = self.dados_etapa['catalogo_pequeno_cheio']
        self._criar_visualizacao_tabela_in_frame(tabela_arquivos_frame, tabela_visual, self.validar_fase_1)

        tabela_ascii_frame = tk.Frame(tabelas_frame, bg=self.cor_fundo)
        tabela_ascii_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        tk.Label(tabela_ascii_frame, text="Tabela ASCII de Referência", font=self.font_subtitulo, fg=self.cor_titulo, bg=self.cor_fundo).pack(pady=(0, 5))
        self._criar_tabela_ascii_na_tela(tabela_ascii_frame)

        tools_frame = tk.Frame(main_frame, bg=self.cor_fundo)
        tools_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        narrativa = f"R7-X: O primeiro passo é encontrar a 'entrada' para o arquivo `{self.chave_alvo}`. Para isso, calcule o hash e clique no bucket correto na tabela. O protocolo Imperial usa: `Índice = (Soma ASCII) % {self.tamanho_tabela_simulacao}`."
        tk.Label(tools_frame, text=narrativa, wraplength=350, font=self.font_narrativa, fg=self.cor_texto, bg=self.cor_fundo).pack(pady=(0, 10))

        ttk.Button(tools_frame, text="Dica Extra", command=self._mostrar_dica_extra_fase1, style="Dark.TButton").pack(pady=5)
        
        calc_frame = tk.Frame(tools_frame, bg=self.cor_fundo, bd=2, relief="solid", padx=10, pady=10)
        calc_frame.pack(pady=10)
        tk.Label(calc_frame, text=f"Calculadora de Módulo % {self.tamanho_tabela_simulacao}", font=self.font_subtitulo, fg=self.cor_titulo, bg=self.cor_fundo).pack()
        
        self.entrada_ascii = []
        ascii_input_frame = tk.Frame(calc_frame, bg=self.cor_fundo)
        ascii_input_frame.pack()
        for i in range(4):
            entrada = tk.Entry(ascii_input_frame, width=4, font=("Courier New", 14), bg="black", fg="white", insertbackground="white")
            entrada.pack(side=tk.LEFT, padx=2, pady=5)
            self.entrada_ascii.append(entrada)

        ttk.Button(calc_frame, text="Calcular", command=self._calcular_modulo_com_passos, style="Accent.Dark.TButton").pack(pady=5)
        
        self.resultado_calculo_label = tk.Label(calc_frame, text="", font=("Courier New", 12), fg=self.cor_texto, bg=self.cor_fundo)
        self.resultado_calculo_label.pack()
        
    def finalizar_missao(self):
        # Busque a nave alvo no banco de dados completo para exibir todos os detalhes.
        nave_alvo_info = next((item for item in BANCO_DE_DADOS_GRANDE if item['chave'] == self.chave_alvo), None)

        self._limpar_frame()

        if nave_alvo_info:
            tk.Label(self.base_content_frame, text=f"Missão Concluída!", font=self.font_titulo, fg="green", bg=self.cor_fundo).pack(pady=(10, 15))
            
            titulo_nave = f"Acesso Concedido: {nave_alvo_info['chave']}"
            tk.Label(self.base_content_frame, text=titulo_nave, font=self.font_subtitulo, fg=self.cor_titulo, bg=self.cor_fundo).pack(pady=(5, 10))

            detalhes_frame = tk.Frame(self.base_content_frame, bg=self.cor_fundo)
            detalhes_frame.pack(padx=20, pady=10)
            
            row_count = 0
            for key, value in nave_alvo_info['valor'].items():
                tk.Label(detalhes_frame, text=f"{key}:", font=self.font_narrativa, fg=self.cor_titulo, bg=self.cor_fundo).grid(row=row_count, column=0, sticky="W", padx=5)
                tk.Label(detalhes_frame, text=value, font=self.font_narrativa, fg=self.cor_texto, bg=self.cor_fundo).grid(row=row_count, column=1, sticky="W")
                row_count += 1
                
            narrativa_final = "R7-X: As informações da nave foram transmitidas para a Frota Rebelde. Este conhecimento nos dá uma vantagem crucial. O futuro da Aliança está mais seguro graças à sua dedicação."
            tk.Label(self.base_content_frame, text=narrativa_final, wraplength=700, justify=tk.CENTER, font=self.font_narrativa, fg=self.cor_texto, bg=self.cor_fundo).pack(pady=20)
        else:
            tk.Label(self.base_content_frame, text="Erro interno: A chave da nave alvo não foi encontrada. Missão Concluída.", font=self.font_titulo, fg="red", bg=self.cor_fundo).pack(pady=20)
        
        ttk.Button(self.base_content_frame, text="Concluir Missão", command=lambda: self.game_manager.mission_completed("Missao4"), style="Accent.Dark.TButton").pack(pady=20)
        
    def retry_mission(self):
        self.game_manager.set_game_state("START_MISSION_4")

    def abrir_janela_tabela_ascii(self):
        nova_janela = tk.Toplevel(self.root)
        nova_janela.title("Tabela ASCII de Referência")
        nova_janela.geometry("400x600")
        nova_janela.configure(bg=self.cor_fundo)
        
        frame_scroll = tk.Frame(nova_janela, bg=self.cor_fundo)
        frame_scroll.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(frame_scroll, bg=self.cor_fundo, highlightthickness=0)
        scrollbar = ttk.Scrollbar(nova_janela, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.cor_fundo)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(scrollable_frame, text="Caractere | Valor ASCII", font=self.font_subtitulo, fg=self.cor_titulo, bg=self.cor_fundo).pack(fill=tk.X, anchor="w", padx=5)
        
        for i in range(32, 127):
            char = chr(i)
            valor = i
            label_texto = f"   '{char:^4}'   |    {valor:^5}"
            tk.Label(scrollable_frame, text=label_texto, font=("Courier New", 12), fg=self.cor_texto, bg=self.cor_fundo, justify=tk.LEFT).pack(fill=tk.X, anchor="w", padx=5)