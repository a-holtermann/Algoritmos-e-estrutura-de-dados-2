import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# Configuração inicial para obter a rede no entorno da UFRN
place = "Universidade Federal do Rio Grande do Norte, Natal, Brazil"
G = ox.graph_from_place(place, network_type='all')

# Converte o MultiGraph para Graph para remover arestas duplicadas
G = nx.Graph(G)

# Configuração do estilo para os gráficos
sns.set(style="whitegrid")

# Requisito 1: Calcular métricas de centralidade
# Degree Centrality
degree_centrality = nx.degree_centrality(G)
# Closeness Centrality
closeness_centrality = nx.closeness_centrality(G)
# Betweenness Centrality
betweenness_centrality = nx.betweenness_centrality(G, normalized=True, endpoints=True)
# Eigenvector Centrality
eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=1000)

# Adiciona centralidades aos nós para visualização
for node in G.nodes():
    G.nodes[node]['degree_centrality'] = degree_centrality[node]
    G.nodes[node]['closeness_centrality'] = closeness_centrality[node]
    G.nodes[node]['betweenness_centrality'] = betweenness_centrality[node]
    G.nodes[node]['eigenvector_centrality'] = eigenvector_centrality[node]

# Identificação dos principais nós (Alta Degree e Betweenness Centrality)
top_degree_nodes = sorted(degree_centrality, key=degree_centrality.get, reverse=True)[:5]
top_betweenness_nodes = sorted(betweenness_centrality, key=betweenness_centrality.get, reverse=True)[:5]

# Obtenha dados de localização dos principais nós para verificar os bairros
gdf_nodes = ox.graph_to_gdfs(G, edges=False)

# Verifica quais colunas estão presentes em gdf_nodes
print("Colunas disponíveis em gdf_nodes:", gdf_nodes.columns)

# Atualiza o código de acordo com as colunas disponíveis
if 'osmid' in gdf_nodes.columns:
    top_degree_locations = gdf_nodes.loc[top_degree_nodes]
    top_betweenness_locations = gdf_nodes.loc[top_betweenness_nodes]

    print("Possíveis bairros para análise com alta centralidade:")
    print(top_degree_locations[['osmid', 'geometry']])

    print("Possíveis locais para dock-stations com alta intermediação (Betweenness Centrality):")
    print(top_betweenness_locations[['osmid', 'geometry']])
else:
    # Caso 'osmid' não esteja presente, usamos apenas a geometria
    top_degree_locations = gdf_nodes.loc[top_degree_nodes]
    top_betweenness_locations = gdf_nodes.loc[top_betweenness_nodes]

    print("Possíveis bairros para análise com alta centralidade (sem 'osmid'):")
    print(top_degree_locations[['geometry']])

    print("Possíveis locais para dock-stations com alta intermediação (Betweenness Centrality) (sem 'osmid'):")
    print(top_betweenness_locations[['geometry']])

# Função para desenhar a rede com centralidade destacada usando nx.draw()
def plot_centrality(G, centrality, title, pos, ax):
    node_color = [centrality[node] for node in G.nodes()]
    nodes = nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_color, 
                                   cmap='viridis', node_size=50, alpha=0.8)
    edges = nx.draw_networkx_edges(G, pos, ax=ax, edge_color='grey', width=0.3, alpha=0.5)
    ax.set_title(title, fontsize=14)
    plt.colorbar(nodes, ax=ax, orientation='horizontal', fraction=0.046, pad=0.04)

# Definir layout com espaçamento para visualizações consistentes
pos = nx.spring_layout(G, seed=42, k=0.15)

# Visualização das redes destacando cada métrica de centralidade
fig, axs = plt.subplots(2, 2, figsize=(15, 15))
fig.suptitle('Métricas de Centralidade da Rede no Entorno da UFRN', fontsize=18)

plot_centrality(G, degree_centrality, "Degree Centrality", pos, axs[0, 0])
plot_centrality(G, closeness_centrality, "Closeness Centrality", pos, axs[0, 1])
plot_centrality(G, betweenness_centrality, "Betweenness Centrality", pos, axs[1, 0])
plot_centrality(G, eigenvector_centrality, "Eigenvector Centrality", pos, axs[1, 1])

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

# Requisito 2: Análise CDF e PDF dos graus dos nós
degree_values = [val for (node, val) in G.degree()]
degree_counts = pd.Series(degree_values).value_counts().sort_index()

# CDF e PDF
fig, ax = plt.subplots(1, 2, figsize=(14, 5))

# PDF
sns.histplot(degree_values, kde=True, stat="density", ax=ax[0], color='blue')
ax[0].set_title('PDF dos Graus dos Nós')
ax[0].set_xlabel('Grau')
ax[0].set_ylabel('Densidade')

# CDF
degree_values_sorted = np.sort(degree_values)
cdf = np.arange(1, len(degree_values_sorted) + 1) / len(degree_values_sorted)
ax[1].plot(degree_values_sorted, cdf, marker=".", linestyle="none", color='blue')
ax[1].set_title('CDF dos Graus dos Nós')
ax[1].set_xlabel('Grau')
ax[1].set_ylabel('CDF')

plt.suptitle('Análise PDF e CDF dos Graus dos Nós', fontsize=16)
plt.show()

# Requisito 3: Análise multivariada das métricas de centralidade
# Criação de DataFrame para análise
centrality_df = pd.DataFrame({
    'degree_centrality': list(degree_centrality.values()),
    'closeness_centrality': list(closeness_centrality.values()),
    'betweenness_centrality': list(betweenness_centrality.values()),
    'eigenvector_centrality': list(eigenvector_centrality.values())
})

# Matriz de scatterplot e KDE
g = sns.PairGrid(centrality_df)
g.map_upper(sns.scatterplot, color='blue')
g.map_lower(sns.kdeplot, cmap="Reds")
g.map_diag(sns.kdeplot, lw=2, legend=False, color='blue')
plt.suptitle('Análise Multivariada das Métricas de Centralidade', y=1.02, fontsize=16)
plt.show()

# Requisito 4: Identificação do core/shell da rede
core_numbers = nx.core_number(G)
max_core = max(core_numbers.values())
core_nodes = [node for node, core in core_numbers.items() if core == max_core]
unique_cores = set(core_numbers.values())

# Visualização dos k-cores usando nx.draw(), destacando o core mais alto
fig, ax = plt.subplots(figsize=(12, 10))
node_color = [core_numbers[node] for node in G.nodes()]
nodes = nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_color, cmap='viridis', node_size=50, alpha=0.8)
edges = nx.draw_networkx_edges(G, pos, ax=ax, edge_color='grey', width=0.3, alpha=0.5)

# Destaque visual dos nós pertencentes ao core mais alto
nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=core_nodes, node_color='red', node_size=80, label=f'Core {max_core}', edgecolors='black')
ax.set_title("Core/Shell da Rede com o Núcleo Mais Alto Destacado", fontsize=16)
plt.colorbar(nodes, ax=ax, orientation='horizontal', fraction=0.046, pad=0.04)
plt.legend(scatterpoints=1, loc='upper left')
plt.show()

print(f"O core mais alto é o core {max_core} e contém {len(core_nodes)} nós.")
print("Valores únicos de k-core na rede:", unique_cores)

