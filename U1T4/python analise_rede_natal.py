# Importar as bibliotecas necessárias
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

# Definir a cidade para análise
cidade = "Natal, Rio Grande do Norte, Brazil"

# Baixar os dados da rede de ruas da cidade
print("Baixando dados da rede de ruas...")
G = ox.graph_from_place(cidade, network_type='drive')

# Converter o Multigraph em um Graph simples (removendo múltiplas arestas)
# OSMnx já oferece a função get_undirected() que lida com isso.
print("Convertendo o Multigraph para Graph simples...")
G_simple = ox.utils_graph.get_undirected(G)  # Obtém um grafo simples sem múltiplas arestas

# Plotar e salvar o gráfico da rede de ruas
print("Plotando a rede de ruas e salvando a imagem...")
fig, ax = ox.plot_graph(G_simple, node_size=5, node_color='blue', edge_color='gray', save=True, filepath='natal_rede_viaria.png', show=True)

# === 1. Quais possíveis rotas para dar a volta na cidade? ===
print("Identificando ciclos que dão a volta na cidade...")
cycles = list(nx.cycle_basis(G_simple))
print(f"Número de ciclos identificados: {len(cycles)}")

# Plotar um ciclo (subgrafo) para visualização de uma rota que dá a volta na cidade
if cycles:
    cycle_subgraph = G_simple.subgraph(cycles[0])  # Pegar o primeiro ciclo para exibir
    fig, ax = ox.plot_graph(cycle_subgraph, node_size=5, node_color='red', edge_color='blue', show=True)
    print("Exemplo de ciclo plotado (uma possível rota que dá a volta).")
else:
    print("Nenhum ciclo foi encontrado.")

# === 2. Quais pontos mais afastados e os pontos mais perto? ===

# Pontos mais afastados (baseado no diâmetro da rede)
print("Calculando os pontos mais afastados (diâmetro)...")
try:
    largest_component = max(nx.connected_components(G_simple), key=len)
    subgraph = G_simple.subgraph(largest_component).copy()
    diameter = nx.diameter(subgraph)
    print(f"Diâmetro (maior distância entre dois pontos): {diameter}")
except nx.NetworkXError:
    print("O grafo não é conexo, não foi possível calcular o diâmetro.")

# Identificar os pontos mais próximos com base na distância mais curta
print("Calculando os pontos mais próximos...")
min_path_length = float('inf')
min_path = None
for node1 in subgraph:
    for node2 in subgraph:
        if node1 != node2:
            try:
                length = nx.shortest_path_length(subgraph, node1, node2, weight='length')
                if length < min_path_length:
                    min_path_length = length
                    min_path = (node1, node2)
            except nx.NetworkXNoPath:
                pass

if min_path:
    print(f"Pontos mais próximos: {min_path} com uma distância de {min_path_length} metros")
    closest_subgraph = subgraph.subgraph(min_path)
    fig, ax = ox.plot_graph(closest_subgraph, node_size=10, node_color='green', edge_color='gray', show=True)
else:
    print("Nenhum caminho mínimo foi encontrado.")

# === 3. Quais pontos se cruzam? ===
print("Identificando pontos de cruzamento (nós com grau maior que 2)...")
crossing_points = [node for node, degree in dict(G_simple.degree()).items() if degree > 2]
print(f"Número de pontos de cruzamento identificados: {len(crossing_points)}")

# Plotar os pontos de cruzamento
if crossing_points:
    crossing_subgraph = G_simple.subgraph(crossing_points)
    fig, ax = ox.plot_graph(crossing_subgraph, node_size=50, node_color='yellow', edge_color='gray', show=True)
    print("Exemplo de pontos de cruzamento plotado.")
else:
    print("Nenhum ponto de cruzamento foi encontrado.")

# === 4. Qual rota para ir direto para a costa? ===
# Supondo que tenhamos um conjunto de nós que representam a costa (geograficamente próximos)
# Aqui usamos apenas um exemplo de um nó na costa com base na latitude
coast_nodes = [n for n in G.nodes if G.nodes[n].get('y') < -5.85]  # Exemplo: nós com latitude menor que -5.85 (próximos à costa)

# Encontrar a rota mais curta para a costa
print("Calculando a rota mais curta para a costa...")
start_node = list(G_simple.nodes())[0]  # Selecionando um nó inicial arbitrário (pode ser modificado)
if coast_nodes:
    closest_coast_node = coast_nodes[0]
    shortest_path_to_coast = nx.shortest_path(G_simple, source=start_node, target=closest_coast_node, weight='length')
    
    # Plotar o caminho até a costa
    coast_path_subgraph = G_simple.subgraph(shortest_path_to_coast)
    fig, ax = ox.plot_graph(coast_path_subgraph, node_size=10, node_color='blue', edge_color='green', show=True)
    print("Rota para a costa plotada.")
else:
    print("Nenhum nó costeiro foi encontrado.")

# === Exibir as principais métricas calculadas ===
print("\n===== Principais Métricas Calculadas =====")
print(f"1. Número de Ciclos: {len(cycles)}")
print(f"2. Diâmetro da Rede (distância mais longa): {diameter if 'diameter' in locals() else 'Não disponível'}")
print(f"3. Distância mínima entre dois pontos: {min_path_length if min_path else 'Não disponível'}")
print(f"4. Número de Pontos de Cruzamento: {len(crossing_points)}")
print("==========================================")
