import pandas as pd
import nltk
import networkx as nx

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

def preprocess_text(text):
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    porter = PorterStemmer()
    stemmed_tokens = [porter.stem(word) for word in filtered_tokens]
    return stemmed_tokens

def create_graph(text):
    terms = preprocess_text(text)
    G = nx.DiGraph()
    for i in range(len(terms)-1):
        G.add_edge(terms[i], terms[i+1])
    return G

data = pd.read_csv('combinesCSV.csv', encoding='latin1')
data = pd.concat([data.iloc[0: 12], data.iloc[15:27], data.iloc[30:42]])

content_column = 0

document_graphs = {}

for index, row in data.iterrows():
    content = row[content_column]
    document_id = index 
    
    # Create graph for the content
    document_graphs[document_id] = create_graph(content)
