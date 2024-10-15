import pandas as pd
import networkx as nx
from itertools import combinations
import matplotlib.pyplot as plt

# Carregar os dados
csv_path = 'DADOS_ABERTOS_MEDICAMENTOS.csv'
dados_medicamentos = pd.read_csv(csv_path, delimiter=';', encoding='latin-1')

# Limpeza e separação dos princípios ativos
dados_medicamentos_limpos = dados_medicamentos.dropna(subset=['PRINCIPIO_ATIVO'])
dados_medicamentos_limpos.loc[:, 'PRINCIPIO_ATIVO'] = dados_medicamentos_limpos['PRINCIPIO_ATIVO'].str.split(' + ')

# Função para criar a Rede 01: Co-ocorrência de princípios ativos entre medicamentos
def criar_rede_coocorrencia_principios_ativos():
    G = nx.Graph()
    
    # Adicionar nós (medicamentos) ao grafo
    for index, row in dados_medicamentos_limpos.iterrows():
        G.add_node(row['NOME_PRODUTO'], categoria=row['CATEGORIA_REGULATORIA'])

    # Criar dicionário para mapear princípios ativos aos medicamentos
    principio_medicamento = {}
    for index, row in dados_medicamentos_limpos.iterrows():
        for ativo in row['PRINCIPIO_ATIVO']:
            if ativo not in principio_medicamento:
                principio_medicamento[ativo] = set()
            principio_medicamento[ativo].add(row['NOME_PRODUTO'])

    # Adicionar arestas entre medicamentos que compartilham princípios ativos
    for medicamentos in principio_medicamento.values():
        for med1, med2 in combinations(medicamentos, 2):
            G.add_edge(med1, med2)

    return G

# Função para criar a Rede 02: Grafo Bipartido de Medicamentos e Princípios Ativos
def criar_rede_bipartida():
    B = nx.Graph()

    # Adicionar nós (medicamentos e princípios ativos)
    for index, row in dados_medicamentos_limpos.iterrows():
        B.add_node(row['NOME_PRODUTO'], bipartite=0)
        for ativo in row['PRINCIPIO_ATIVO']:
            B.add_node(ativo, bipartite=1)
            B.add_edge(row['NOME_PRODUTO'], ativo)
    
    return B

# Função para criar a Rede 03: Co-ocorrência por Empresa ou Classe Terapêutica
def criar_rede_coocorrencia_empresa_classe():
    G = nx.Graph()
    
    # Adicionar nós (medicamentos) ao grafo
    for index, row in dados_medicamentos_limpos.iterrows():
        G.add_node(row['NOME_PRODUTO'], empresa=row['EMPRESA_DETENTORA_REGISTRO'], classe=row['CLASSE_TERAPEUTICA'])
    
    # Adicionar arestas entre medicamentos da mesma empresa ou classe terapêutica
    for index, row in dados_medicamentos_limpos.iterrows():
        medicamentos_mesma_empresa = dados_medicamentos_limpos[dados_medicamentos_limpos['EMPRESA_DETENTORA_REGISTRO'] == row['EMPRESA_DETENTORA_REGISTRO']]
        medicamentos_mesma_classe = dados_medicamentos_limpos[dados_medicamentos_limpos['CLASSE_TERAPEUTICA'] == row['CLASSE_TERAPEUTICA']]
        for _, row2 in medicamentos_mesma_empresa.iterrows():
            if row['NOME_PRODUTO'] != row2['NOME_PRODUTO']:
                G.add_edge(row['NOME_PRODUTO'], row2['NOME_PRODUTO'])
        for _, row3 in medicamentos_mesma_classe.iterrows():
            if row['NOME_PRODUTO'] != row3['NOME_PRODUTO']:
                G.add_edge(row['NOME_PRODUTO'], row3['NOME_PRODUTO'])
    
    return G

# Função para calcular assortatividade e exibir resultados
def calcular_assortatividade(grafo, atributo):
    return nx.attribute_assortativity_coefficient(grafo, atributo)

# Criar as redes
rede_01 = criar_rede_coocorrencia_principios_ativos()
rede_02 = criar_rede_bipartida()
rede_03 = criar_rede_coocorrencia_empresa_classe()

# Calcular a assortatividade
assortatividade_rede_01 = calcular_assortatividade(rede_01, 'categoria')
assortatividade_rede_02 = nx.degree_assortativity_coefficient(rede_02)
assortatividade_rede_03_empresa = calcular_assortatividade(rede_03, 'empresa')
assortatividade_rede_03_classe = calcular_assortatividade(rede_03, 'classe')

# Exibir resultados
print(f"Assortatividade Rede 01 (Categoria Regulatória): {assortatividade_rede_01}")
print(f"Assortatividade Rede 02 (Grau Bipartido): {assortatividade_rede_02}")
print(f"Assortatividade Rede 03 (Empresa): {assortatividade_rede_03_empresa}")
print(f"Assortatividade Rede 03 (Classe Terapêutica): {assortatividade_rede_03_classe}")

# Visualização das redes
def desenhar_grafo(grafo, titulo):
    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(grafo, k=0.1)
    nx.draw(grafo, pos, with_labels=True, node_size=50, font_size=8)
    plt.title(titulo)
    plt.show()

# Desenhar redes
desenhar_grafo(rede_01, "Rede 01: Co-ocorrência de Princípios Ativos")
plt.show()  # Adicionado para garantir que o gráfico seja exibido

desenhar_grafo(rede_02, "Rede 02: Grafo Bipartido de Medicamentos e Princípios Ativos")
plt.show()  # Adicionado para garantir que o gráfico seja exibido

desenhar_grafo(rede_03, "Rede 03: Co-ocorrência por Empresa ou Classe Terapêutica")
plt.show()  # Adicionado para garantir que o gráfico seja exibido


