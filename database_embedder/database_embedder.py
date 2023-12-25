from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np
from sklearn.neighbors import BallTree
from joblib import dump, load
import os

class DatabaseEmbedder:
    """
    The class for encoding all paper titles
    """
    def __init__(self, batch_size=2, model=None):
        self.data_dict = {}
        self.model = SentenceTransformer(model) ## define model
        self.batch_size = batch_size ## batch size when encoding
    
    def run(self, data_dir=None, output_dir=None):
        """
        Args: 
            - data_dir: where is the raw data
            - output_dir: where to save data
        Two main steps: encoding all paper titles and indexing with BallTree
        """
        ## Encoding all paper titles
        raw_data = pd.read_csv(data_dir)
        titles = raw_data["paper_title"].to_list()
        embeddings = []
        for i in range(0, len(titles), self.batch_size):
            batch = titles[i:i+self.batch_size]
            emb = self.model.encode(batch)
            embeddings.append(emb)
        embeddings = np.concatenate(embeddings, axis=0) ## Stack embedding batches

        ## Indexing with BallTree
        tree = BallTree(embeddings, leaf_size=2, metric='manhattan')
        
        ## Save result
        np.save(os.path.join(output_dir, "embeddings_raw.npy"), embeddings)
        dump(tree, os.path.join(output_dir, "embeddings_tree.joblib"))


if __name__ == '__main__':
    embedder = DatabaseEmbedder(batch_size=2, model="model/")
    embedder.run(data_dir="data/raw_data.csv", output_dir="database_embedder/")