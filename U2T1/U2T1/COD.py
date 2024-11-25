import networkx as nx
import matplotlib.pyplot as plt
import community as community_louvain

# Função para carregar a base de dados em formato GEXF
def load_graph(filepath):
    return nx.read_gexf(filepath)

# Função para plotar os gráficos com melhorias na clareza e salvar as figuras
def plot_graph(graph, pos, sizes, colors, title, cmap, colorbar_label, filename):
    plt.figure(figsize=(16, 14))  # Aumentar o tamanho da figura para mais clareza
    
    # Desenhar o grafo com ajustes de estilo
    nodes = nx.draw_networkx_nodes(
        graph, pos, node_size=sizes, node_color=colors, cmap=cmap, alpha=0.8
    )
    nx.draw_networkx_edges(graph, pos, alpha=0.5, width=1.5)
    
    # Adicionar barra de cores
    cbar = plt.colorbar(nodes)
    cbar.set_label(colorbar_label, size=14)
    cbar.ax.tick_params(labelsize=12)

    # Melhorar o título e formato do gráfico
    plt.title(title, size=18)
    plt.axis("off")
    plt.tight_layout(pad=4.0)  # Aumentar o espaçamento
    
    # Salvar e mostrar o gráfico
    plt.savefig(filename)
    plt.show()

# Caminho para o arquivo da rede
file_path = "BSD.gexf"  # Certifique-se de que o arquivo está no mesmo diretório do script
graph = load_graph(file_path)

# Remover self-loops (arestas que conectam um nó a ele mesmo)
graph.remove_edges_from(nx.selfloop_edges(graph))

# Calcular métricas básicas
degree = dict(graph.degree())
closeness = nx.closeness_centrality(graph)
betweenness = nx.betweenness_centrality(graph)
eigenvector = nx.eigenvector_centrality(graph)

# Layout padrão para todas as visualizações (Ajuste de semente para layout consistente)
# Aumento de k (para maior separação) e mais iterações
pos = nx.spring_layout(graph, seed=42, k=2.0, iterations=300)  # Muito mais espaço entre os nós

# Requisito #01: Tamanho do vértice proporcional ao grau, cor pelo closeness
sizes_r1 = [min(500, degree[n] * 25) for n in graph.nodes]  # Limitar o tamanho máximo
colors_r1 = [closeness[n] for n in graph.nodes]
plot_graph(
    graph, pos, sizes_r1, colors_r1,
    "Requisito #01: Grau e Closeness Centrality",
    plt.cm.viridis, "Closeness Centrality", "requisito_01.png"
)

# Requisito #02: Destacar K-Core e K-Shell
k_shell = nx.core_number(graph)
sizes_r2 = [min(500, k_shell[n] * 25) for n in graph.nodes]  # Limitar o tamanho máximo
colors_r2 = [k_shell[n] for n in graph.nodes]
plot_graph(
    graph, pos, sizes_r2, colors_r2,
    "Requisito #02: K-Core e K-Shell",
    plt.cm.plasma, "K-Shell Value", "requisito_02.png"
)

# Requisito #03: Comunidades na rede, tamanho livre (exemplo: grau)
partition = community_louvain.best_partition(graph)
sizes_r3 = [min(500, degree[n] * 25) for n in graph.nodes]  # Limitar o tamanho máximo
colors_r3 = [partition[n] for n in graph.nodes]
plot_graph(
    graph, pos, sizes_r3, colors_r3,
    "Requisito #03: Comunidades Detectadas",
    plt.cm.tab10, "Comunidade", "requisito_03.png"
)

# Informações extras sobre as métricas utilizadas
print("Métricas:")
print("- Grau (degree):", degree)
print("- Closeness Centrality:", closeness)
print("- Betweenness Centrality:", betweenness)
print("- Eigenvector Centrality:", eigenvector)
print("- K-Shell:", k_shell)
