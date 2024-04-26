import csv
import networkx as nx
import os

# Function to construct directed graph from text content
def construct_graph(content):
    G = nx.DiGraph()
    terms = content.split()  # Split content into terms (words)
    for i in range(len(terms) - 1):
        current_term = terms[i]
        next_term = terms[i + 1]
        if not G.has_edge(current_term, next_term):
            G.add_edge(current_term, next_term, weight=1)  # Add edge between consecutive terms
        else:
            G[current_term][next_term]['weight'] += 1  # Increment edge weight if edge already exists
    return G

# Function to read CSV file and construct graphs
def read_csv_and_construct_graphs(csv_file):
    graphs = []
    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            content = row['Content']
            type_ = row['Type']  # Read the 'Type' column
            graph = construct_graph(content)
            graphs.append((type_, graph))  # Append both content and type to the list of graphs
    return graphs

# Function to save graph to CSV file
def save_graph_to_csv(graph, output_folder, graph_id, type_):
    output_file = os.path.join(output_folder, f"graph_{graph_id}_{type_}.csv")
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Source', 'Target', 'Weight'])
        for edge in graph.edges(data=True):
            source = edge[0]
            target = edge[1]
            weight = edge[2]['weight']
            writer.writerow([source, target, weight])

# Function to extract common subgraph features
def graph_distance(graph1, graph2):
    edges1 = set(graph1.edges())
    edges2 = set(graph2.edges())
    common_edges = edges1.intersection(edges2)
    mcs_graph = nx.Graph(list(common_edges))
    return -len(mcs_graph.edges())

# Main function
def main():
    # Path to the CSV file
    csv_file = 'combinesCSV.csv'
    # Path to the output folder to store CSV files for each graph
    output_folder = 'output_graphs'

    # Read CSV file and construct graphs
    graphs = read_csv_and_construct_graphs(csv_file)

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save each graph to a separate CSV file
    for i, (type_, graph) in enumerate(graphs, start=1):
        save_graph_to_csv(graph, output_folder, i, type_)  # Pass type information to save function
        print(f"Graph {i} saved to CSV.")

    # Extract features using common subgraph distance
    feature_file = 'graph_features.csv'
    with open(feature_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Content', 'Type', 'Feature'])
        for i, (type_, graph) in enumerate(graphs, start=1):
            for j, (type_other, graph_other) in enumerate(graphs, start=1):
                if j > i:
                    distance = graph_distance(graph, graph_other)
                    writer.writerow([f"Graph {i} ({type_})", f"Graph {j} ({type_other})", distance])

    print("Features extracted and saved to graph_features.csv")

if __name__ == "__main__":
    main()
