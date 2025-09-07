# BancoDados/dados_hangar.py
import random
import string

def gerar_conteudo_aleatorio():
    """Gera um conteúdo de contêiner aleatório."""
    tipos_carga = [
        "Componentes Eletrônicos", "Suprimentos Médicos", "Armamento Leve",
        "Peças de Droid", "Equipamento de Navegação", "Rações Sintéticas",
        "Metais Raros", "Ferramentas de Reparo", "Uniformes Imperiais",
        "Dados Criptografados", "Combustível de Hiperpropulsor"
    ]
    return random.choice(tipos_carga)

def gerar_catalogo_hangar(tamanho_min=400):
    """Gera um catálogo de contêineres com chaves únicas."""
    catalogo = []
    ids_existentes = set()
    
    while len(catalogo) < tamanho_min:
        # Gera um ID único e fácil de ser identificado
        novo_id = f"H-{random.randint(1000, 9999)}"
        if novo_id not in ids_existentes:
            ids_existentes.add(novo_id)
            catalogo.append({'id': novo_id, 'conteudo': gerar_conteudo_aleatorio()})
            
    return catalogo

# Banco de dados da Missão 1
CATALOGO_HANGAR = gerar_catalogo_hangar()