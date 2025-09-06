# BancoDados/dados_naves.py
import random
import string

def gerar_chave_aleatoria():
    """Gera uma chave alfanumérica aleatória com alta chance de colisão."""
    letras = string.ascii_uppercase
    digitos = string.digits
    return random.choice(letras) + random.choice(letras) + '-' + random.choice(digitos)

def gerar_especificacoes_nave():
    """Gera um dicionário com 5 especificações de nave aleatórias."""
    tipos_naves = ["Caça", "Cargueiro", "Bombardeiro", "Cruzador", "Reconhecimento"]
    motores = ["Hiperpropulsor T-8", "Subluz Mk-IV", "Ion-Drive X-2"]
    
    return {
        "Tipo": random.choice(tipos_naves),
        "Modelo": f"Modelo-{random.randint(1, 100)}",
        "Fabricante": f"Fabrica-{random.randint(1, 10)}",
        "Motorização": random.choice(motores),
        "Armamento": f"Laser {random.randint(1, 3)}"
    }

def gerar_catalogo_naves(tamanho_maximo):
    """Gera uma lista de pares (chave, valor) com o tamanho especificado, garantindo chaves únicas."""
    catalogo = []
    chaves_existentes = set()
    while len(catalogo) < tamanho_maximo:
        chave = gerar_chave_aleatoria() 
        if chave not in chaves_existentes:
            chaves_existentes.add(chave)
            catalogo.append({'chave': chave, 'valor': gerar_especificacoes_nave()})
    return catalogo

def gerar_chaves_com_colisao(tamanho_tabela, num_colisoes=2):
    """
    Gera um conjunto de chaves que colidem para uma dada tabela de hash.
    Retorna uma lista de dicionários.
    """
    colisoes = {}
    while len(colisoes) < num_colisoes:
        chave = gerar_chave_aleatoria()
        soma_ascii = sum(ord(char) for char in chave)
        indice_hash = soma_ascii % tamanho_tabela
        if indice_hash not in colisoes:
            colisoes[indice_hash] = []
        colisoes[indice_hash].append({'chave': chave, 'valor': gerar_especificacoes_nave()})
        if len(colisoes[indice_hash]) > 1:
            return colisoes[indice_hash]
    return []
    
def encontrar_chaves_em_colisao_no_banco(banco_de_dados, tamanho_tabela, num_colisoes=2):
    """
    Encontra um conjunto de chaves que colidem em um banco de dados já existente.
    """
    indices_vistos = set()
    colisoes = {}

    for item in banco_de_dados:
        chave = item['chave']
        soma_ascii = sum(ord(char) for char in chave)
        indice_hash = soma_ascii % tamanho_tabela
        
        if indice_hash not in colisoes:
            colisoes[indice_hash] = []
        
        colisoes[indice_hash].append(item)
        
        if len(colisoes[indice_hash]) >= num_colisoes:
            return colisoes[indice_hash]
    return []

# --- Bancos de Dados para as Missões ---
BANCO_DE_DADOS_GRANDE = gerar_catalogo_naves(198)
BANCO_DE_DADOS_PEQUENO = gerar_catalogo_naves(90)