import os
import docx
import networkx as nx
from nltk.stem import PorterStemmer

# Initialize Porter Stemmer
stemmer = PorterStemmer()

# Function to construct graph from processed text
def construct_graph(processed_text):
    G = nx.DiGraph()
    for i in range(len(processed_text)-1):
        current_node = processed_text[i]
        next_node = processed_text[i+1]
        G.add_edge(current_node, next_node)
    return G

# Function to process .docx files in a directory, construct graphs, and save them
def process_files(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Process each .docx file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.docx'):  
            input_path = os.path.join(input_folder, filename)

            # Open the .docx file
            doc = docx.Document(input_path)

            # Extract text from the document
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"

            # Tokenize the text
            word_tokens = text.split()

            # Perform stemming
            stemmed_text = [stemmer.stem(word) for word in word_tokens]

            # Construct graph
            graph = construct_graph(stemmed_text)

            # Save the graph
            output_path = os.path.join(output_folder, filename.split('.')[0] + '.graphml')
            nx.write_graphml(graph, output_path)

# Specify input and output folders
input_folder = 'ProcessLifeStyle&Hobbies'  # Relative path from the current working directory
output_folder = 'GraphsProcessedCLifeStyle&Hobbies'  # Relative path from the current working directory

# Get the absolute paths
current_directory = os.path.dirname(os.path.abspath(__file__))
input_folder = os.path.join(current_directory, input_folder)
output_folder = os.path.join(current_directory, output_folder)

# Process files and save graphs
process_files(input_folder,output_folder)
