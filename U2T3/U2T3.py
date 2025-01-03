import osmnx as ox
import networkx as nx
from heapq import heappush, heappop


# ==== Função para preparar o grafo ====
def prepare_graph(graph):
    """
    Prepara o grafo baixado do OSMnx, convertendo para não-direcionado,
    simplificando, e garantindo que todas as arestas tenham o atributo 'length'.
    """
    graph = ox.utils_graph.get_undirected(graph)
    
    if not graph.graph.get("simplified", False):
        graph = ox.simplify_graph(graph)
    
    for u, v, data in graph.edges(data=True):
        if "length" not in data:
            data["length"] = 1.0
    return graph


# ==== Função para Dijkstra com Min-Heap ====
def dijkstra_min_heap(graph, source, target):
    """
    Calcula o menor caminho entre dois nós usando o algoritmo de Dijkstra
    implementado com Min-Heap.
    """
    distances = {node: float('inf') for node in graph.nodes}
    distances[source] = 0
    
    priority_queue = [(0, source)]
    
    while priority_queue:
        current_distance, current_node = heappop(priority_queue)
        
        if current_distance > distances[current_node]:
            continue
        
        for neighbor, data in graph[current_node].items():
            weight = data.get('length', 1)
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heappush(priority_queue, (distance, neighbor))
    
    return distances[target]


# ==== Função para Dijkstra com NetworkX ====
def dijkstra_networkx(graph, source, target):
    """
    Calcula o menor caminho entre dois nós usando o algoritmo de Dijkstra
    implementado com NetworkX.
    """
    return nx.shortest_path_length(graph, source, target, weight='length')


# ==== Função para visualizar caminhos do Dijkstra ====
def visualize_dijkstra_paths(graph, source_name, target_name, points_of_interest):
    """
    Visualiza o menor caminho entre dois locais em Natal-RN usando o algoritmo de Dijkstra.
    """
    source = ox.distance.nearest_nodes(graph, *points_of_interest[source_name][::-1])
    target = ox.distance.nearest_nodes(graph, *points_of_interest[target_name][::-1])
    
    path = nx.shortest_path(graph, source=source, target=target, weight="length")
    
    ox.plot_graph_route(
        graph,
        route=path,
        bgcolor="white",
        node_size=15,
        node_color="blue",
        route_linewidth=2,
        route_color="red",
        edge_linewidth=0.5,
        edge_color="gray",
        figsize=(12, 12)
    )


# ==== Função para visualizar a MST ====
def visualize_kruskal_mst():
    """
    Visualiza a Árvore Geradora Mínima (MST) no grafo de Natal-RN,
    com ajustes para melhorar a legibilidade.
    """
    place_name = "Natal, Brazil"
    graph = ox.graph_from_place(place_name, network_type="drive")
    
    mst = kruskal_mst(graph)
    
    ox.plot_graph(
        mst,
        bgcolor="white",
        node_size=15,
        node_color="blue",
        edge_linewidth=0.5,
        edge_color="gray",
        figsize=(12, 12)
    )


# ==== Função para comparar Dijkstra ====
def compare_dijkstra():
    """
    Compara os caminhos mais curtos calculados pelos algoritmos de Dijkstra 
    (Min-Heap e NetworkX) para 10 pares de locais em Natal-RN.
    """
    place_name = "Natal, Brazil"
    graph = ox.graph_from_place(place_name, network_type="drive")
    graph = prepare_graph(graph)
    
    points_of_interest = {
        "Forte dos Reis Magos": (-5.764155, -35.199711),
        "Praia de Ponta Negra": (-5.872989, -35.177589),
        "Parque das Dunas": (-5.836466, -35.202138),
        "Arena das Dunas": (-5.827541, -35.217955),
        "Shopping Midway Mall": (-5.812790, -35.205965),
        "Barreira do Inferno": (-5.912225, -35.172111),
        "Farol de Mãe Luiza": (-5.790460, -35.191306),
        "Praia dos Artistas": (-5.779432, -35.191689),
        "Museu Câmara Cascudo": (-5.812778, -35.209798),
        "UFRN (Campus Central)": (-5.839170, -35.200964),
    }
    
    pairs = [
        ("Forte dos Reis Magos", "Praia de Ponta Negra"),
        ("Parque das Dunas", "Arena das Dunas"),
        ("Shopping Midway Mall", "Barreira do Inferno"),
        ("Farol de Mãe Luiza", "Praia dos Artistas"),
        ("Museu Câmara Cascudo", "UFRN (Campus Central)"),
    ]
    
    for source_name, target_name in pairs:
        print(f"Visualizando caminho: {source_name} → {target_name}")
        visualize_dijkstra_paths(graph, source_name, target_name, points_of_interest)


# ==== Função para calcular a MST ====
def kruskal_mst(graph):
    """
    Calcula a Árvore Geradora Mínima (MST) usando o algoritmo de Kruskal.
    """
    graph = prepare_graph(graph)
    mst = nx.minimum_spanning_tree(graph, weight='length')
    return mst


# ==== Execução Principal ====
if __name__ == "__main__":
    print("=== Comparando Dijkstra (Min-Heap) com NetworkX ===")
    compare_dijkstra()
    
    print("=== Visualizando MST com Kruskal ===")
    visualize_kruskal_mst()
