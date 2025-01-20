Book Text Analysis with Graphs
This Python project performs text analysis on books using various NLP techniques, graph theory, and visualizations. The main goal is to analyze and visualize co-occurrence relationships between words in two classic books: Pride and Prejudice and Moby Dick. Additionally, it extracts key insights such as named entity recognition (NER) and part-of-speech (PoS) tagging, computes network metrics, and detects communities within the word co-occurrence graph.

Features
Text Downloading and Cleaning: Downloads books from Project Gutenberg and cleans them.
Text Preprocessing: Tokenizes and removes stopwords from the text.
Visualization: Creates graphs for word frequencies, co-occurrence, and community structures.
Network Metrics: Calculates metrics like density, betweenness centrality, and clustering coefficient for the co-occurrence graph.
Community Detection: Identifies communities within the graph using modularity optimization.
Ego Network: Generates ego networks around selected nodes.
Exporting: Exports graphs in multiple formats for further analysis, including Gephi (.gexf) and NetworkX formats.
Requirements
requests
spacy
networkx
matplotlib
pandas
nltk
base64
Install dependencies:

pip install requests spacy networkx matplotlib pandas nltk
python -m spacy download en_core_web_sm
Running the Script
Download the books and clean the text.
Process the text and create graphs for co-occurrence, word frequencies, and communities.
Save the results in CSV and image formats in the results directory.
Generate an HTML report with embedded Base64 images.
Directory Structure
bash

results/
    ├── graphs/           # Graph images
    ├── metrics/          # CSV files with graph metrics
    ├── gephi/            # Gephi export files
    ├── networkx/         # NetworkX export files
index_with_base64.html  # Final HTML report
