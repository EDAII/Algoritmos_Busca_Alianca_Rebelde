# algoritmos_busca/busca_sequencial.py

def busca_sequencial(lista, chave, campo='id'):

    for i in range(len(lista)):
        if lista[i].get(campo) == chave:
            return i
    return -1

def busca_sequencial_com_sentinela(lista, chave, campo='id'):
   
    tamanho_original = len(lista)
    
    # Cria o sentinela e o adiciona ao final da lista
    sentinela = {campo: chave}
    lista.append(sentinela)

    i = 0
    while lista[i].get(campo) != chave:
        i += 1

    lista.pop() # Remove o sentinela para restaurar a lista original

    if i < tamanho_original:
        return i
    else:
        return -1