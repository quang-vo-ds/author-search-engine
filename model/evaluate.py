from sentence_transformers import SentenceTransformer, util
import json
import gradio as gr
import numpy as np
import pandas as pd
from joblib import load

## Import all necessary files for this app
raw_data_file = "data/raw_data.csv"
embedding_tree_file = "database_embedder/embeddings_tree.joblib"
model_dir = "model/"
labels_file = "data/labels_dict.json"

raw_data = pd.read_csv(raw_data_file)
model = SentenceTransformer(model_dir)
tree = load(embedding_tree_file)
labels_dict = json.load(open(labels_file, "r"))

## Main function
def predict(query, topk):
    query_emb = model.encode(query).reshape(1,-1) ## Encode query
    _, top_ids = tree.query(query_emb, k=topk) ## Find top similar titles to the query
    return top_ids

def evaluate():
    """
    Calcualate Accuracy metric for the information retrieval tasks
    """
    ## Create a map from data index to labels
    idx_to_labels = {}
    topics = list(labels_dict.keys())
    for t in topics:
        for idx in labels_dict[t]:
            idx_to_labels[idx] = topics.index(t)

    ## Calculate predicted labels and true labels
    pred_ids = [i for t in topics for i in predict(t, 30)[0]]
    true_labels = [idx_to_labels[i] for i in pred_ids] ## true labels are extracted using the idx_to_labels map
    pred_labels = [i for t in topics for i in [topics.index(t)]*30] ## each predicted label is an index of the topic (because it is trying to retrieve data came from the same topic)
    
    return (np.array(true_labels) == np.array(pred_labels)).mean()

if __name__ == '__main__':
    print("Accuracy: ", evaluate())
