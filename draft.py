from sentence_transformers import SentenceTransformer, util
import json
import numpy as np
import pandas as pd
from sklearn.neighbors import BallTree

raw_data_file = "data/raw_data.csv"
embedding_file = "database_embedder/embeddings_raw.npy"
model_dir = "model/"

raw_data = pd.read_csv(raw_data_file)
model = SentenceTransformer(model_dir)
title_embedding = np.load(embedding_file)
tree = BallTree(title_embedding, leaf_size=2, metric='manhattan') 

query = "object detection"
query_emb = model.encode(query).reshape(1,-1) ## Encode query
dist, ind = tree.query(query_emb, k=20)
print(ind)

