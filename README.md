# Searching for Authors in a Research Field Using SentenceTransformers

## Table of Contents
 - [Summary](#summary)
 - [Repository structure](#repository-structure)
 - [Key Implementation Details](#key-implementation-details)
 - [Fine-tuning Details](#fine-tuning-details)
 - [Dataset](#dataset)
 - [Demo](#demo)

## Summary

 In this repo, I demonstrate a possible implementation of using **semantic search** ([sentence_transformers](https://sbert.net/)) to search for a group of experts in a particular research field. My pipeline includes three main steps:

   1. Encode paper titles offline into a searchable format.
   2. Encode queries in real time and compare to the saved title embeddings to find a group of semantically similar papers.
   3. From this group of papers, calculate the total number of citations for each author and return authors with the highest citations.

## Repository Structure

* [data](./data/) is where I store raw data (data from scraping Google Scholar website) and train data (data being transformed into an appropriate format for the training purpose). The scripts used to produce the data are [load_data.py](./data/load_data.py) and [prepare_train_data.py](./data/prepare_train_data.py).
* [model](./model/) is where I save the artifact of the model. The scripts for training is in [train.py](./model/train.py).
* [database_embedder](./database_embedder/) is where I save offline title embeddings. Embedding and indexing scripts are in [database_embedder.py](./database_embedder/database_embedder.py).
* [app](./app/) is where I save the [code](./app/app.py) to demo my model using Gradio.

## Key Implementation Details
1. Offline Encoding of Paper Titles

In this step, I use the Sentence Transformer (more specifically, [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)) to encode all the paper titles into an embedding matrix. Next, I use [BallTree](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.BallTree.html) to index the embedding matrix (which should help to speed up querying). All the script can be found in [database_embedder/database_embedder.py](./database_embedder/database_embedder.py).

> Paper Title => Embedding => Indexing

2. Real Time Semantic Search for Similar Papers

In this step, a user query is taken into the system, embedded using the same model. `Manhattan` distances are computed from it to all of the saved embeddings produced from the 1st step.  The smallest distance entries are returned as semantically similar matches.

> Text Query => Embedding => Compute Distance between Query and Saved Embeddings => Retrieve a Group of Papers in the Same Research Field

3. Retrive Top Authors

In this step, I calculate the total number of citations of the authors in the papers retrived above. The authors with highest number of citations are returned.

> Group of Papers => Total Number of Citations for each Authors => Retrieve Top K Authors with Highest Number of Citations

## Fine-tuning Details
The performance of the app in this demo is highly dependent on the embedding model. Therefore, it could be useful to fine-tune the model so that it can be aware of domain-specific jargons. In this repositary, I include the [train.py](./model/train.py) script to serve this purpose.

Let's have a closer look to the key components in the script:
- Base model: [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- Loss function: Multiple negatives Ranking Loss. The loss is especially suitable for Information Retrieval and Semantic Search tasks. A nice advantage of the loss is that it only requires positive pairs.
- Evaluating score: Accuracy
- Similarity metric: Manhattan distance

However, it is also worth noticing that: without fine-tuning, the pre-trained [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) model is already good enough with 98% of accuracy on the dev set. Therefore, it is actually no need for the fine-tuning step in this demo. 


## Dataset

The dataset used for demonstration in this repositary is scraped from [Google Scholar](https://scholar.google.com/) (script to download the data can be found in [data/load_data.py](./data/load_data.py)). There are 300 papers covering 8 topics (`object detection`, `face recognition`, `biological vision`, `face anti-spoofing`, `object recognition`, `name entity recognition`, `sentiment analysis`, `text summarization`, `machine translation`, `topic modelling`) in this dataset. Below is an example:


| **Paper Title** | **Cite Count** | **Year** | **Publication**   | **Authors** |
| :-------------: | :------------: | :------: |:----------------: | :----------------: |
| Object detection survey| 200   | 2022     | eeexplore.ieee.org| Z Zou |

This dataset is then transformed into a format that can facilitate the `Semantic Textual Similarity` training process, using the [data/prepare_train_data.py](./data/prepare_train_data.py) script. After transforming, the dataset for training looks like as below:

| **Title 1** | **Title 2** | **Label** |
| :---------: | :---------: | :-------: |
| Object detection survey| Imbalance problems in object detection   | 1  |
| Image analysis for face recognition| Nested named entity recognition   | 0 |

## Demo

In this repo, I use [Gradio](https://www.gradio.app/) to create a simple app. You can run the app by clone this repo and run the [app/app.py](./app/app.py) script as below:

```shell
git clone https://github.com/quang-vo-ds/author-search-engine.git
cd author-search-engine
pip install -r requirements. txt
python app/app.py
```
Video demo: https://drive.google.com/file/d/13N6vF8fMqgnrdE3M20CLszEdCp9W8DGo/view?usp=sharing