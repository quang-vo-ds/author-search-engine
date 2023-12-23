from sentence_transformers import SentenceTransformer, util
import json
import numpy as np

embedding_file = "database_embedder/title_embedding.npy"
model_dir = 'model/'

model = SentenceTransformer('model/')
title_embedding = np.load(embedding_file)

def lambda_handler(event, context):
    query = json.dumps(event["data"])
    topk = json.dumps(event["topk"])
    query_emb = model.encode(query) ## Encode query
    
    ## Find top similar titles to the query
    scores = []
    for i in range(title_embedding.shape[0]):
        scores.append(util.cos_sim(query_emb, title_embedding[i,:]))
    top_idx = sorted(range(len(scores)), reverse=True, key=scores.__getitem__)[:topk]

    ## 


if __name__ == '__main__':
    event = {
        "data": "A",
        "topk": 3
    }
    result = lambda_handler(event, "")

# #Compute cosine similarity between all pairs
# cos_sim = util.cos_sim(embeddings, embeddings)

# #Add all pairs to a list with their cosine similarity score
# all_sentence_combinations = []
# for i in range(len(cos_sim)-1):
#     for j in range(i+1, len(cos_sim)):
#         all_sentence_combinations.append([cos_sim[i][j], i, j])

# #Sort list by the highest cosine similarity score
# all_sentence_combinations = sorted(all_sentence_combinations, key=lambda x: x[0], reverse=True)

# print("Top-5 most similar pairs:")
# for score, i, j in all_sentence_combinations[0:5]:
#     print("{} \t {} \t {:.4f}".format(sentences[i], sentences[j], cos_sim[i][j]))