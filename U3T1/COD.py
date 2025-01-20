import requests
import spacy
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import os
import pickle
from nltk.corpus import stopwords
from collections import Counter
from networkx.algorithms.community import greedy_modularity_communities
import base64

# Configurações iniciais
nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words("english"))
os.makedirs("results", exist_ok=True)
os.makedirs("results/graphs", exist_ok=True)
os.makedirs("results/metrics", exist_ok=True)
os.makedirs("results/gephi", exist_ok=True)
os.makedirs("results/networkx", exist_ok=True)

# Função para baixar e limpar textos
def download_and_clean_text(url, start_line=None, end_line=None):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Erro ao baixar o arquivo: {response.status_code}")
    text = response.text
    lines = text.splitlines()

    if start_line is not None and end_line is not None:
        lines = lines[start_line:end_line]

    cleaned_text = "\n".join(lines).strip()
    return cleaned_text

# Função para pré-processamento do texto
def preprocess_text(text):
    doc = nlp(text)
    tokens = [token.text.lower() for token in doc if token.is_alpha and token.text.lower() not in stop_words]
    return tokens

# Função para criar gráfico de comparação de palavras
def plot_word_comparison(tokens, title, file_name):
    word_freq = Counter(tokens)
    most_common = word_freq.most_common(20)
    words, counts = zip(*most_common)

    plt.figure(figsize=(12, 6))
    plt.bar(words, counts, color="skyblue")
    plt.xticks(rotation=45, ha="right")
    plt.title(title)
    plt.xlabel("Palavras")
    plt.ylabel("Frequência")
    plt.tight_layout()
    plt.savefig(f"results/graphs/{file_name}.png")
    plt.close()

# Função para análise de PoS Tagging e NER
def analyze_text_with_pos_ner(text):
    doc = nlp(text)
    pos_tags = [(token.text, token.pos_) for token in doc if token.pos_ == "PROPN"]
    ner_entities = [(ent.text, ent.label_) for ent in doc.ents if ent.label_ in ["PERSON", "ORG", "GPE"]]

    # Salvar resultados intermediários
    pd.DataFrame(pos_tags, columns=["Token", "PoS"]).to_csv("results/pos_tags.csv", index=False)
    pd.DataFrame(ner_entities, columns=["Entity", "Type"]).to_csv("results/ner_entities.csv", index=False)

    return pos_tags, ner_entities

# Função para criar grafo de co-ocorrência
def create_cooccurrence_graph(tokens, window_size=2):
    edges = []
    for i in range(len(tokens) - window_size + 1):
        window = tokens[i:i + window_size]
        for j in range(len(window)):
            for k in range(j + 1, len(window)):
                edges.append((window[j], window[k]))
    graph = nx.Graph()
    graph.add_edges_from(edges)
    return graph

# Função para calcular métricas do grafo
def analyze_graph(G, graph_name):
    metrics = {
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "density": nx.density(G),
        "average_clustering": nx.average_clustering(G),
        "betweenness_centrality": nx.betweenness_centrality(G),
        "closeness_centrality": nx.closeness_centrality(G),
        "degree_centrality": nx.degree_centrality(G)
    }

    # Salvar métricas
    metrics_df = pd.DataFrame.from_dict(metrics, orient="index", columns=["Value"])
    metrics_df.to_csv(f"results/metrics/{graph_name}_metrics.csv")

    return metrics

# Função para visualizar grafo
def visualize_graph(G, title, file_name):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    degrees = dict(G.degree())
    nx.draw(
        G, pos, with_labels=True, node_size=[v * 100 for v in degrees.values()],
        node_color="lightblue", edge_color="gray", font_size=8, font_weight="bold"
    )
    plt.title(title)
    plt.savefig(f"results/graphs/{file_name}.png")
    plt.close()

# Função para criar e salvar uma rede ego
def create_and_save_ego_network(G, center_node, file_name):
    if center_node not in G:
        print(f"O nó {center_node} não está no grafo. Não foi possível criar a rede ego.")
        return

    ego_net = nx.ego_graph(G, center_node)

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(ego_net)
    degrees = dict(ego_net.degree())
    nx.draw(
        ego_net, pos, with_labels=True,
        node_size=[v * 300 for v in degrees.values()],
        node_color="lightgreen", edge_color="black",
        font_size=8, font_weight="bold"
    )
    plt.title(f"Ego Network - {center_node}")
    output_path = f"results/graphs/{file_name}.png"
    plt.savefig(output_path)
    plt.close()

    print(f"Grafo ego salvo em: {output_path}")

# Função para identificar comunidades no grafo
def analyze_communities(G, graph_name):
    communities = list(greedy_modularity_communities(G))
    community_sizes = [len(c) for c in communities]

    with open(f"results/metrics/{graph_name}_communities.txt", "w") as f:
        f.write(f"Número de comunidades: {len(communities)}\n")
        f.write(f"Tamanhos das três maiores comunidades: {community_sizes[:3]}\n")

    community_map = {node: idx for idx, community in enumerate(communities) for node in community}
    nx.set_node_attributes(G, community_map, "community")

    return communities

# Função para exportar o grafo para uso no Gephi
def export_graph_to_gephi(G, graph_name):
    nx.write_gexf(G, f"results/gephi/{graph_name}.gexf")

# Função para exportar o grafo para formatos NetworkX
def export_graph_networkx_formats(G, graph_name):
    with open(f"results/networkx/{graph_name}.pkl", "wb") as f:
        pickle.dump(G, f)
    nx.write_graphml(G, f"results/networkx/{graph_name}.graphml")

# URLs e configurações dos textos
books = {
    "Pride and Prejudice": {
        "url": "https://www.gutenberg.org/files/1342/1342-0.txt",
        "start_line": 0,
        "end_line": 3000
    },
    "Moby Dick": {
        "url": "https://www.gutenberg.org/files/2701/2701-0.txt",
        "start_line": 0,
        "end_line": 3000
    }
}

# Processar cada texto
book_graphs = {}
for book_name, config in books.items():
    try:
        print(f"\nProcessando {book_name}...")
        raw_text = download_and_clean_text(config["url"], config["start_line"], config["end_line"])
        tokens = preprocess_text(raw_text)
        pos_tags, ner_entities = analyze_text_with_pos_ner(raw_text)

        # Criar e salvar o gráfico de comparação de palavras
        word_comparison_file = f"{book_name}_word_comparison.png"
        plot_word_comparison(tokens, title=f"Word Frequency - {book_name}", file_name=f"{book_name}_word_comparison")

        graph = create_cooccurrence_graph(tokens[:2000], window_size=3)
        cooccurrence_file = f"{book_name}_graph.png"
        visualize_graph(graph, title=f"Co-occurrence Graph - {book_name}", file_name=f"{book_name}_graph")
        analyze_graph(graph, book_name)

        communities = analyze_communities(graph, book_name)

        if communities:
            node = list(communities[0])[0]
            create_and_save_ego_network(graph, node, f"{book_name}_ego_network")

        export_graph_to_gephi(graph, book_name)
        export_graph_networkx_formats(graph, book_name)

        # Adicionar informações dos gráficos ao dicionário
        book_graphs[book_name] = {
            "word_comparison": word_comparison_file,
            "cooccurrence": cooccurrence_file
        }

    except Exception as e:
        print(f"Erro ao processar {book_name}: {e}")

# Gerar HTML com gráficos incorporados como Base64
def generate_html_with_base64(book_graphs):
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Book Analysis Graphs</title>
</head>
<body>
    <h1>Book Analysis Graphs</h1>
"""

    for book_name, graphs in book_graphs.items():
        html_content += f"<h2>{book_name}</h2>\n"

        for graph_type, file_path in graphs.items():
            with open(f"results/graphs/{file_path}", "rb") as img_file:
                base64_string = base64.b64encode(img_file.read()).decode('utf-8')
                html_content += f"<h3>{graph_type.replace('_', ' ').title()}</h3>\n"
                html_content += f"<img src='data:image/png;base64,{base64_string}' alt='{graph_type} - {book_name}'/><br>\n"

    html_content += """
    <footer>
        <p>&copy; 2025 Book Analysis | Generated with Python</p>
    </footer>
</body>
</html>
"""

    with open("results/index_with_base64.html", "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

# Gerar HTML com gráficos incorporados
generate_html_with_base64(book_graphs)
