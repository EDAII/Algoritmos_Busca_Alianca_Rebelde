# algoritmos_busca/hashing_busca.py
import string
import random

# Funções de Hash e Rehash
def hashing_divisao(chave, tamanho_tabela):
    soma_ascii = sum(ord(char) for char in chave)
    return soma_ascii % tamanho_tabela

def sondagem_linear(indice_inicial, i, tamanho_tabela):

    return (indice_inicial + i) % tamanho_tabela

def hashing_duplo_passo(chave, tamanho_tabela):
    soma_ascii = sum(ord(char) for char in chave)
    # Garante que o passo não seja 0
    return 1 + (soma_ascii % (tamanho_tabela - 1))

def sondagem_dupla(indice_inicial, i, passo_duplo, tamanho_tabela):
    return (indice_inicial + i * passo_duplo) % tamanho_tabela

# Funções para Construção e Busca em Tabelas
def construir_tabela_hash_encadeamento(dados, tamanho_tabela):
    tabela = [[] for _ in range(tamanho_tabela)]
    for item in dados:
        chave = item['chave']
        indice = hashing_divisao(chave, tamanho_tabela)
        tabela[indice].append(item)
    return tabela

def construir_tabela_hash_fechada(dados, tamanho_tabela):
    tabela = [None] * tamanho_tabela
    for item in dados:
        chave = item['chave']
        indice = hashing_divisao(chave, tamanho_tabela)
        
        # Simula uma inserção simples, para gerar colisões
        if tabela[indice] is None:
            tabela[indice] = item
    return tabela

def simular_caminho_sondagem(chave, tabela, tipo_sondagem="linear"):
    valor_numerico = sum(ord(char) for char in chave)
    tamanho_tabela = len(tabela)
    indice_inicial = hashing_divisao(chave, tamanho_tabela)
    caminho = [indice_inicial]

    if tabela[indice_inicial] is None or (isinstance(tabela[indice_inicial], dict) and tabela[indice_inicial]['chave'] == chave):
        return caminho

    i = 1
    if tipo_sondagem == "linear":
        while i < tamanho_tabela:
            proximo_indice = sondagem_linear(indice_inicial, i, tamanho_tabela)
            caminho.append(proximo_indice)
            if tabela[proximo_indice] is None or (isinstance(tabela[proximo_indice], dict) and tabela[proximo_indice]['chave'] == chave):
                return caminho
            i += 1
    elif tipo_sondagem == "dupla":
        passo_duplo = hashing_duplo_passo(chave, tamanho_tabela)
        while i < tamanho_tabela:
            proximo_indice = sondagem_dupla(indice_inicial, i, passo_duplo, tamanho_tabela)
            caminho.append(proximo_indice)
            if tabela[proximo_indice] is None or (isinstance(tabela[proximo_indice], dict) and tabela[proximo_indice]['chave'] == chave):
                return caminho
            i += 1
    return caminho

def encontrar_item_em_encadeamento(tabela, chave_alvo):

    indice_bucket = hashing_divisao(chave_alvo, len(tabela))
    bucket = tabela[indice_bucket]
    for i, item in enumerate(bucket):
        if item['chave'] == chave_alvo:
            return indice_bucket, i
    return None, None