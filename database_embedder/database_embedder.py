from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np

class DatabaseEmbedder:
    def __init__(self, batch_size=2, model=None):
        self.data_dict = {}
        self.model = SentenceTransformer(model)
        self.batch_size = batch_size
    
    def run(self, data_dir=None, output_dir=None):
        raw_data = pd.read_csv(data_dir)
        titles = raw_data["paper_title"].to_list()
        embeddings = []
        for i in range(0, len(titles), self.batch_size):
            batch = titles[i:i+self.batch_size]
            emb = self.model.encode(batch)
            embeddings.append(emb)
        embeddings = np.concatenate(embeddings, axis=0) ## Stack embedding batches
        ## Save result
        np.save(output_dir, embeddings)

if __name__ == '__main__':
    embedder = DatabaseEmbedder(batch_size=2, model="model/")
    embedder.run(data_dir="data/raw_data.csv", output_dir="database_embedder/title_embedding.npy")
            # for i, row in raw_data.iterrows():
            # title = row["Paper Title"]
            # num_cited = row["Citation"]
            # authors = row["Author"]
            # print(i, title, authors, num_cited)