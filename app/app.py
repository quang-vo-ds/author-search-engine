from sentence_transformers import SentenceTransformer, util
import json
import gradio as gr
import numpy as np
import pandas as pd
from joblib import load

raw_data_file = "data/raw_data.csv"
embedding_tree_file = "database_embedder/embeddings_tree.joblib"
model_dir = "model/"

raw_data = pd.read_csv(raw_data_file)
model = SentenceTransformer(model_dir)
tree = load(embedding_tree_file)

def handler(query, topk):
    query_emb = model.encode(query).reshape(1,-1) ## Encode query
    
    ## Find top similar titles to the query
    _, top_ids = tree.query(query_emb, k=topk)
    print(top_ids)

    ## Calculate total citation for each author of the top relevant papers
    author_rank = {}
    for i, row in raw_data.iloc[top_ids[0]].iterrows():
        if row["authors"] not in author_rank.keys():
            author_rank[row["authors"]] = int(row["cite_count"])
        else:
            author_rank[row["authors"]] += int(row["cite_count"])
    author_rank = [(k,v) for k, v in sorted(author_rank.items(), reverse=True, key=lambda item: item[1])]
    outcome = ""
    for author, citation in author_rank:
        outcome = outcome + f"{author}:{citation}\n"
    return outcome

if __name__ == '__main__':
    demo = gr.Interface(
        fn=handler,
        inputs=[gr.Textbox(), gr.Number()],
        outputs=gr.Textbox()
    )
    demo.launch(share=True)